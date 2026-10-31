[calling run_lasso on data/startups.csv -> next_round_valuation_musd]
**Short answer:** This analysis can't tell you whether a top-tier VC leading the round will raise a startup's valuation. Lasso finds patterns that help predict valuation. It can't separate a variable's own effect from everything that travels with it.

**How well it predicts**
- The test R² is 0.65. R² is the share of the differences in valuations that the model predicts, where 0 is no better than guessing the average and 1 is perfect. The test set is startups held out from fitting.
- The model was fitted on 320 startups and tested on 80 others.

**What the model used**
- Alpha was 0.267. Alpha is the penalty strength, and it was chosen by cross-validation, which means picking the value that predicted best on startups left out during fitting.
- Variables Lasso kept, largest coefficient first. Each coefficient is the change in predicted valuation, in $M, for a one-standard-deviation change in that variable. A standard deviation is a typical spread in the data.
  - revenue_growth_pct: 13.8
  - arr_musd: 10.8
  - top_tier_vc_lead: 7.6
  - founder_prior_exits: 5.9
  - net_revenue_retention_pct: 3.9
  - founder_years_experience: 3.2
  - customer_retention_pct: 2.8
  - monthly_burn_musd: 1.2
  - media_mentions: 1.0
  - gross_margin_pct: 0.8
- Variables it did not need: team_size, num_investors, hq_in_major_hub.

**What this does and does not tell you**
- Lasso used `top_tier_vc_lead` for prediction. That is not the same as saying a top-tier lead raises valuation. The 7.6 is not the gap between startups with and without a top-tier lead, because this is a yes/no variable and one standard deviation isn't "yes versus no".
- Top-tier VCs may pick startups that were already stronger. The same quality signals could also attract both the VC and a higher price. The coefficient mixes the VC's own effect with all of that.
- Lasso can also keep one of several overlapping variables and drop another almost at random. Examples are VC backing and media coverage, or growth and retention. A slightly different sample could change which ones are kept without hurting predictions. So don't read the kept or dropped lists as what matters.
- For the causal question, you need a method built for it, such as double/debiased machine learning (Chernozhukov et al. 2018). It uses machine learning for the prediction steps inside a causal design. It still depends on the data capturing why some startups got a top-tier lead, and that is a judgment call the software can't check.
- Lasso can help with a prediction question. One example is which startups in your pipeline are likely to raise at higher valuations.

**Caveat:** The 0.65 applies to new startups only if they come from the same process as this data. That means similar companies, a similar funding market, and the same way of measuring each variable. A funding boom or downturn could lower it. The dataset is also simulated.
