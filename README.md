# Lasso Agent

A minimal AI agent that predicts a startup's next-round valuation with Lasso and explains the results in plain business language.

You give the agent a question about a CSV file. The agent (Claude, through the Anthropic API) decides to call a Python tool that fits a Lasso regression, reads the results, and explains them. Its instructions are based on Mullainathan (2025), "Economics in the Age of Algorithms": prediction is not causation, so the agent answers prediction questions and explains why it can't answer causal ones.

The project was built step by step with [Claude Code](https://code.claude.com/docs). The prompts used are listed below, so you can rebuild it yourself.

## What's in the repo

```
lasso-agent/
├── CLAUDE.md                # rules Claude Code follows in this project (read automatically)
├── context/
│   └── project_brief.md     # what the agent does and how it interprets results
├── data/
│   └── startups.csv         # simulated data on 400 venture-backed startups
├── src/
│   ├── tools.py             # run_lasso(): the tool the agent can call
│   ├── system_prompt.md     # the agent's instructions
│   └── agent.py             # the agent loop that talks to the Claude API
├── outputs/                 # the agent's saved answers
└── requirements.txt
```

The paper is not included because it is copyrighted. See [The paper](#the-paper) below.

## Setup

Please run the following instructions in the terminal of your VSCode. You need Python 3.11 or newer (tested with 3.12) and an Anthropic API key.

**1. Get the code**

```
git clone https://github.com/YOUR-USERNAME/lasso-agent.git
cd lasso-agent
```

**2. Create the environment and install the libraries**

```
python3 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

**3. Add your API key**

Create a key at [console.anthropic.com](https://console.anthropic.com) and add some credit. Then save it as an environment variable. On a Mac, open your shell settings:

```
open -e ~/.zshrc
```

and add this line at the bottom, with your own key:

```
export ANTHROPIC_API_KEY="sk-ant-..."
```

Save, close, and open a new terminal. If you use Claude Code, add the same line to `~/.zshenv` too: Claude Code's shell doesn't read `~/.zshrc`. Then quit and reopen VS Code.

Never put the key in a file inside this project.

## Run the agent

From the project folder, with the environment active (`(.venv)` at the start of the prompt):

**A prediction question**, which Lasso can answer:

```
python src/agent.py "Using data/startups.csv, how well can we predict next_round_valuation_musd, and what does the model rely on?"
```

**A causal question**, which Lasso can't answer:

```
python src/agent.py "Using data/startups.csv with target next_round_valuation_musd: if a top-tier VC leads the round, will the startup's valuation go up?"
```

The first line of the output, `[calling run_lasso on data/startups.csv -> next_round_valuation_musd]`, is the tool call: Claude decided to run the model and chose its inputs from your question.

To save an answer as a file you can open formatted in VS Code (Cmd + Shift + V), add `> outputs/answer.md` at the end of the command.

**Run the tool on its own** (no API call, no cost):

```
python src/tools.py
```

You should see a test R² of about 0.65.

## Rebuild it yourself with Claude Code

This is the workflow the project was built with: prepare the context, plan, then build and test one file at a time.

**Start** from a copy of this repo with only `CLAUDE.md`, `context/`, `data/` and `src/make_data.py`. Delete `src/tools.py`, `src/system_prompt.md` and `src/agent.py`. Open the folder in VS Code and start a new Claude Code session.

**1. Plan.** Switch Claude Code to plan mode (Shift + Tab, or the mode button) and paste:

```
Read the files in context/ and plan a simple agent that runs Lasso on a dataset and explains the results. Use three files:

- src/tools.py: run_lasso(csv_path, target, random_state=42). Split the data into train and test sets, fit Lasso with alpha chosen by cross-validation, and return the test R², the chosen alpha, and which variables were kept or set to zero.
- src/system_prompt.md: the agent's instructions, based on the project brief.
- src/agent.py: the agent loop, using the Anthropic Python SDK's tool use. It takes a question from the command line, lets Claude call run_lasso, and prints the final answer.

Say how we'll test each file. Build one file at a time and stop after each so I can review.
```

Claude Code may ask questions before planning. We chose to return names and coefficients (not names only), and to leave out the refusal fallback. Read the plan, then approve it with manual approval of edits.

**2. Build the tool.** Claude Code writes and tests `src/tools.py`. Review it, then:

```
Let's move on to step 2
```

**3. Write the agent's instructions.** Claude Code writes `src/system_prompt.md` from the brief. Review it, then:

```
Let's move on to step 3
```

**4. Build the agent loop.** Claude Code writes `src/agent.py` and tests it against the API.

**5. Ask the two questions.** In Claude Code:

```
Run the agent with this question and save its output, exactly as printed, to outputs/answer_prediction.md: "Using data/startups.csv, how well can we predict next_round_valuation_musd, and what does the model rely on?"
```

```
Run the agent with this question and save its output, exactly as printed, to outputs/answer_causal.md: "Using data/startups.csv with target next_round_valuation_musd: if a top-tier VC leads the round, will the startup's valuation go up?"
```

**6. Bonus: see how unstable Lasso's choices are.**

```
Run run_lasso with random_state=7 and compare the dropped variables with random_state=42.
```

Claude Code's code and wording will differ a little from run to run. The numbers should not.

## The dataset

`data/startups.csv` has 400 simulated venture-backed startups. The target is `next_round_valuation_musd`, the valuation at the next funding round in million dollars. The 13 predictors cover founders (experience, prior exits), traction (ARR, revenue growth, net revenue retention, customer retention, gross margin), operations (team size, monthly burn), investors and visibility (number of investors, whether a top-tier VC led the round, media mentions) and location (major startup hub or not).

## The paper

The agent's interpretation rules come from Sendhil Mullainathan, "Economics in the Age of Algorithms", *AEA Papers and Proceedings* 115 (2025): [doi.org/10.1257/pandp.20251118](https://doi.org/10.1257/pandp.20251118).

To use it as context, download the PDF into `context/` as `mullainathan_2025_algorithms.pdf` and ask Claude Code:

```
Convert context/mullainathan_2025_algorithms.pdf into a clean Markdown file in the same folder, keeping headings and section structure.
```

The project brief already summarizes the ideas the agent uses, with section references, so the agent works without the paper too.

## Notes

- The agent uses the model `claude-sonnet-5-5`, set in `src/agent.py`.
- Each question costs a small amount of API credit; a handful of runs costs a few cents.
- The agent only does prediction with Lasso. Data cleaning, plots and comparing models are out of scope.
