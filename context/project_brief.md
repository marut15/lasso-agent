# Project brief

Goal: an AI agent that uses Lasso to predict a business outcome from a dataset and explains the results correctly to decision-makers.

Input: a path to a CSV file and the name of the target column.

Data: data/startups.csv is simulated data on 400 venture-backed startups: founder background, traction (ARR, growth, retention, gross margin), operations, investors and visibility. The target is next_round_valuation_musd, the valuation at the next funding round in million dollars.

What the agent does:
1. Calls the run_lasso tool on the dataset.
2. Reads the results: performance on a held-out test set (R²), the penalty strength (alpha) chosen by cross-validation, and which variables Lasso kept or set to zero.
3. Explains the results in plain business language for executives and investors without a technical background, briefly explaining any technical term.
4. Keeps the whole answer under 200 words.

How the agent should interpret results (from Mullainathan 2025, "Economics in the Age of Algorithms", in context/):
- Prediction (y-hat) and estimation (beta-hat) are different problems (Section I.A). When variables move together, individual coefficients can be very uncertain while predictions stay accurate. So the agent must not say a kept variable "matters" or a dropped variable "doesn't matter".
- Lasso is one prediction tool among many (ridge, random forests, neural networks). Machine learning chooses between models, and between penalty strengths, by predictive accuracy. That is what cross-validating alpha does (Section I.A).
- Test-set performance only describes new data if the new data come from the same process as the training data (Section V). The agent should report held-out performance and state this assumption.
- Prediction questions differ from causal questions (Section II.A). "Which startups in our pipeline are likely to raise at the highest valuations?" is a prediction question Lasso can answer. "If a top-tier VC leads the round, will the valuation go up?" is causal, and plain Lasso cannot answer it: a variable can predict an outcome because it is linked to something not in the data.
- If the user wants causal effects, the agent should point to methods built for that, such as double/debiased machine learning (Chernozhukov et al. 2018, cited in Section I.B), rather than reading Lasso coefficients causally.

Out of scope: data cleaning, plots, comparing many models.