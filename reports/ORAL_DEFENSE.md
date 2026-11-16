# Oral defense notes

ESILV A4 DIA3 — suggested 10-minute presentation sequence.
These are speaker notes and a demonstration plan; they are not a slide deck.

## 0:00–1:00 — Research question

Explain the difference between classifying current survey diabetes status and
forecasting future disease. Introduce the comparison of nine lifestyle/demographic
variables with twenty-one enriched variables. State that the synthetic experiment
asks a separate question: can a model recover an equation whose truth is known?

## 1:00–2:00 — Data and split

Show the CDC notebook's provenance and development EDA. Name the exact UCI export,
253,680 observations, 13.93% positives and the exclusion of ID. Explain why repeated
answers do not necessarily represent duplicate people. State the 80/20 split and
five development folds before showing any performance result.

## 2:00–3:00 — Models and leakage prevention

Show the development comparison figure. Describe the majority baseline, logistic
regression, random forest and gradient boosting, then MI/RFE/L1 selection. Explain
that every learned transformation is fitted inside a training fold. The budget
is 28 configurations, and AP selects the primary model.

## 3:00–4:30 — Real-data findings

Show the report's comparison table and test curves. Enriched gradient boosting
has test AP 0.4247 versus 0.2763 for lifestyle gradient boosting. RFE retains ten
variables with AP 0.3928 compared with 0.3942 for full logistic regression.
Do not claim statistical equivalence from those two point estimates.

Show the threshold table: the development-selected threshold increases recall
from 16.16% to 61.11% while precision decreases from 55.73% to 38.01%.
Emphasize the false-positive cost. Contrast with the majority model's 86.07%
accuracy and zero recall.

## 4:30–5:30 — Known synthetic truth

Show the generating equation and coefficient plot. Explain the unchanged generator,
three cohorts, 50,000 rows each, and approximately 19% positive outcomes. The
coefficients are assumptions. Explain why standardized fitted coefficients must
be converted back and why the raw intercept is −7.40.

## 5:30–7:00 — Noise experiments

Show the robustness figure. Describe measurement errors, irrelevant questions,
label flips and combined conditions. Test outcomes stay clean; noisy development
labels are also the labels used for validation. Explain the formula
`r + (1−2r)p`: symmetric label noise can preserve ranking while damaging probability
accuracy. Use the Brier change from 0.1281 to 0.1495 in the combined condition.

## 7:00–8:00 — Variable recovery

Show the L1 support plot: 2, 2 and 19 irrelevant questions retained out of 20.
Explain why selecting C for predictive AP is not the same as selecting the exact
true variable set. Name Sex as a known null variable in the simulator. Do not
promise that every noise feature should have exactly zero fitted weight.

## 8:00–9:00 — Limits

Cover self-reporting, current-diagnosis indicators, absent survey weights, one CDC
split, ordinal encoding and limited tuning. The simulator is intentionally
logistic and its errors are stylized. Three synthetic seeds give descriptive SD,
not a reliable significance test. Different prevalence prevents direct AP ranking
across the real and synthetic phases.

## 9:00–10:00 — Demonstration and close

Open the executed notebooks and point to a result CSV and the frozen-protocol
file. Show the README reproduction commands. State the measured conclusion:
health indicators add information in CDC; controlled noise separates ranking,
probability accuracy and feature recovery. Invite questions about the method.

## Likely questions

**Why AP rather than accuracy?** The majority model is 86% accurate and has no
positive recall. AP summarizes positive-class precision across recall levels;
ROC-AUC, Brier and threshold metrics answer complementary questions.

**Where is threshold leakage prevented?** Thresholds use development out-of-fold
predictions. A freeze is written before any test scoring. F1 is an experimental
criterion, not a medically validated objective.

**Why is the original synthetic 14% claim absent?** The preserved equation yields
about 19% in actual runs. Reporting measured prevalence avoids changing the
provided generator to fit an unsupported claim.

**Can a fitted model beat the oracle?** A finite random test sample can give a
slightly higher realized AP to a fitted model. The oracle remains the true latent
probability, with zero latent-probability MSE.

**Do negative alcohol coefficients mean protection?** No. CDC coefficients are
observational associations; the simulator's coefficient is a stipulated assumption.
Neither supports a recommendation or a causal interpretation.

**Why did L1 keep noise?** C was selected for AP. Several configurations can rank
similarly, and weaker penalties retain sample noise. Prediction and support
recovery are distinct objectives.

**What would improve the study next?** External or profile-grouped validation,
nonlinear synthetic truth, smaller cohorts, asymmetric label noise and a
predeclared decision-cost objective. These remain extensions, not current results.
