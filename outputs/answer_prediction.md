[calling run_lasso on data/startups.csv -> next_round_valuation_musd]
**Short answer:** The model predicts next-round valuation reasonably well. On startups it hadn't seen, it explained about 65% of the differences in valuation. It leaned most on revenue growth, ARR and top-tier VC backing.

**How well it predicts**
- The test R² is 0.65. R² is the share of the differences in valuation that the model predicts on held-out startups. 1 is perfect, and 0 is no better than always guessing the average.
- The model was fitted on 320 startups and tested on 80 it had not seen (an 80/20 split).
- About a third of the variation is still unexplained, so individual predictions will often be off.

**What the model used**
- The chosen alpha was 0.267. Alpha is the penalty strength, and a larger value gives a simpler model. It was picked by cross-validation: the value that predicted best on startups left out during fitting, tried across 5 rounds.
- The variables were standardized, so each number below is the change in predicted valuation, in $M, for a one-standard-deviation change in that variable. A standard deviation is a typical spread in the data. The other kept variables are held fixed.
- **Kept variables, largest first:**
  - Revenue growth %: 13.8
  - ARR: 10.8
  - Top-tier VC lead: 7.6
  - Founder prior exits: 5.9
  - Net revenue retention %: 3.9
  - Founder years of experience: 3.2
  - Customer retention %: 2.8
  - Monthly burn: 1.2
  - Media mentions: 1.0
  - Gross margin %: 0.8
- **Dropped variables:** team size, number of investors and HQ in a major hub. Lasso did not need these for prediction.
- Top-tier VC lead is a 0/1 variable, so its 7.6 is not the gap between startups with and without a top-tier lead.

**What this does and doesn't tell you**
- Lasso is built to predict well, not to measure the effect of each variable. Many of these variables move together: ARR and team size, growth and retention, VC backing and media coverage. When they do, Lasso can keep one and drop another almost arbitrarily. A different sample might give a different list with similar predictions. So "kept" means the model used it for prediction. It doesn't mean the variable drives valuation. "Dropped" doesn't mean it has no effect.
- The results can help you rank a pipeline by likely valuation. They can't tell you what would happen if you changed something, such as landing a top-tier VC or moving to a hub. For that you would need a causal method, such as double/debiased machine learning.

**Caveat**
- The 0.65 describes new startups only if they come from the same process as this data: similar companies, a similar funding market and the same way of measuring each variable. A boom or downturn could lower it.
- The data are simulated, so treat this as an illustration of the method rather than a finding about real markets.
