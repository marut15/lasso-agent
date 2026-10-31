"""The agent loop: ask Claude a question and let it call run_lasso.

Usage (from the project folder):
    .venv/bin/python src/agent.py "Using data/startups.csv, predict next_round_valuation_musd."

How the loop works:
1. Send the question to Claude, along with a description of the run_lasso tool.
2. If Claude asks to use the tool, run it here in Python and send back the result.
3. Repeat until Claude gives a final answer, then print it.
"""

import json
import sys
from pathlib import Path

import anthropic

from tools import run_lasso

MODEL = "claude-sonnet-5-5"
MAX_ROUNDS = 10  # safety limit so the loop can never run forever

# Describe the tool to Claude: its name, what it does, and its inputs.
TOOLS = [
    {
        "name": "run_lasso",
        "description": (
            "Fit a Lasso regression on a CSV file. Splits the data 80/20 into "
            "train and test sets, chooses the penalty (alpha) by 5-fold "
            "cross-validation on the training set, and returns the test R², the "
            "chosen alpha, and which variables were kept or set to zero."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "csv_path": {
                    "type": "string",
                    "description": "Path to the CSV file, e.g. data/startups.csv",
                },
                "target": {
                    "type": "string",
                    "description": "Name of the column to predict",
                },
                "random_state": {
                    "type": "integer",
                    "description": "Seed for the train/test split (default 42)",
                },
            },
            "required": ["csv_path", "target"],
        },
    }
]


def load_system_prompt():
    """Read the agent's instructions from system_prompt.md (next to this file)."""
    return (Path(__file__).parent / "system_prompt.md").read_text()


def run_tool(name, tool_input):
    """Run the tool Claude asked for. Returns (result_text, is_error)."""
    if name != "run_lasso":
        return f"Unknown tool: {name}", True
    try:
        result = run_lasso(**tool_input)
        return json.dumps(result), False
    except Exception as error:
        # Send the error back to Claude so it can explain it to the user.
        return f"{type(error).__name__}: {error}", True


def ask(question):
    """Run the agent loop for one question and return Claude's final answer."""
    client = anthropic.Anthropic()  # reads ANTHROPIC_API_KEY from the environment
    system_prompt = load_system_prompt()
    messages = [{"role": "user", "content": question}]

    for _ in range(MAX_ROUNDS):
        response = client.messages.create(
            model=MODEL,
            max_tokens=16000,
            system=system_prompt,
            tools=TOOLS,
            messages=messages,
        )

        # Claude is finished: return its text.
        if response.stop_reason == "end_turn":
            return "\n".join(b.text for b in response.content if b.type == "text")

        # Claude wants to use a tool.
        if response.stop_reason == "tool_use":
            # Keep Claude's full turn (including the tool request) in the history.
            messages.append({"role": "assistant", "content": response.content})

            # Run every tool Claude asked for and collect the results.
            tool_results = []
            for block in response.content:
                if block.type == "tool_use":
                    print(
                        f"[calling {block.name} on {block.input.get('csv_path')} "
                        f"-> {block.input.get('target')}]"
                    )
                    result_text, is_error = run_tool(block.name, block.input)
                    tool_results.append(
                        {
                            "type": "tool_result",
                            "tool_use_id": block.id,  # links the result to the request
                            "content": result_text,
                            "is_error": is_error,
                        }
                    )

            # Send all results back together in one message, then loop again.
            messages.append({"role": "user", "content": tool_results})
            continue

        # Anything else means the answer was cut short.
        if response.stop_reason == "refusal":
            return "Claude declined to answer this request."
        if response.stop_reason == "max_tokens":
            return "The answer was too long and got cut off. Try a narrower question."
        return f"Stopped unexpectedly (stop_reason: {response.stop_reason})."

    return f"Stopped after {MAX_ROUNDS} rounds without a final answer."


def main():
    question = " ".join(sys.argv[1:])
    if not question:
        print('Usage: .venv/bin/python src/agent.py "your question"')
        sys.exit(1)
    print(ask(question))


if __name__ == "__main__":
    main()
