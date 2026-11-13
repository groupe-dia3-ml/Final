# Diabetes Status Classification Using Lifestyle and Health Indicators

Machine Learning final project — ESILV, group DIA3.

This project studies how lifestyle habits, demographics and self-reported health
indicators help classify diabetes status. It compares simple, reproducible models
and investigates whether feature selection preserves predictive performance.

**Status:** project definition. Model implementation and experimental results are
not available yet. All project deliverables and presentations are in English.

## Research question

How well can lifestyle and demographic information identify respondents reporting
diabetes or prediabetes, and how much do additional health indicators improve
classification?

The target describes status at the time of the survey. This is not a forecast of
future diabetes onset. Associations and feature importance will not be interpreted
as evidence that a particular habit causes or prevents diabetes.

## Objectives

- Establish a reproducible baseline and an untouched test set.
- Compare lifestyle-based prediction with an enriched health-indicator model.
- Compare logistic regression, random forest and gradient boosting.
- Evaluate whether fewer variables preserve useful predictive performance.
- Analyze false negatives, false positives and variation across demographic groups.

## Dataset

The selected source is **CDC Diabetes Health Indicators**, UCI dataset **891**.

| Property | Selected UCI export |
| --- | --- |
| Observations | 253,680 survey respondents |
| Predictors | 21 categorical or numerical variables |
| Target | `Diabetes_binary` |
| Identifier | `ID`, excluded from model inputs |
| Target counts | 218,334 zeros and 35,346 ones (approximately 13.9% positive) |
| Missing values | None reported by UCI; ingestion will check the downloaded file |

The schema, row count, target counts and health-day ranges were checked against
the UCI CSV on 13 November 2026. This is the full export, not a balanced subset.

- [Dataset page and variable definitions](https://archive.ics.uci.edu/dataset/891/cdc+diabetes+health+indicators)
- [Download the selected CSV](https://archive.ics.uci.edu/static/public/891/data.csv)
- [Machine-readable metadata](https://archive.ics.uci.edu/api/dataset?id=891)
- [Original dataset collection on Kaggle](https://www.kaggle.com/datasets/alexteboul/diabetes-health-indicators-dataset)

### Target

According to the UCI variable dictionary:

- `0`: no diabetes.
- `1`: prediabetes or diabetes.

The UCI page mixes a general three-class description with a binary export; this
project explicitly uses the binary CSV linked above and its documented coding.
The original collection contains alternative files, which must not be substituted
without checking their target definitions and population. Ingestion will record
the exact source, retrieval date and file checksum.

### Predictors

For binary indicators, `0` means no and `1` means yes unless stated otherwise.

| Group | Variable | Meaning or coding |
| --- | --- | --- |
| Lifestyle | `PhysActivity` | Physical activity in the past 30 days, excluding work |
| Lifestyle | `Fruits` | Fruit consumption at least once per day |
| Lifestyle | `Veggies` | Vegetable consumption at least once per day |
| Lifestyle | `Smoker` | At least 100 cigarettes smoked over the lifetime |
| Lifestyle | `HvyAlcoholConsump` | More than 14 drinks/week for men or 7 for women, as defined in the survey |
| Demographics | `Sex` | Recorded sex: 0 = female, 1 = male |
| Demographics | `Age` | 13 age bands, from 18–24 to 80 or older; not exact age |
| Demographics | `Education` | Six ordered education categories |
| Demographics | `Income` | Eight ordered household income categories |
| Health | `BMI` | Body mass index |
| Health | `HighBP` | Reported high blood pressure |
| Health | `HighChol` | Reported high cholesterol, not a blood concentration |
| Health | `CholCheck` | Cholesterol checked within the past five years |
| Health | `Stroke` | History of stroke |
| Health | `HeartDiseaseorAttack` | Coronary heart disease or myocardial infarction |
| Health | `GenHlth` | General health: 1 = excellent through 5 = poor |
| Health | `MentHlth` | Days of poor mental health during the past 30 days, 0–30 |
| Health | `PhysHlth` | Days of poor physical health during the past 30 days, 0–30 |
| Health | `DiffWalk` | Serious difficulty walking or climbing stairs |
| Care access | `AnyHealthcare` | Any healthcare coverage |
| Care access | `NoDocbcCost` | Unable to see a doctor due to cost within the past year |

### Feature-set comparison

1. **Lifestyle and demographics:** the five lifestyle and four demographic variables
   listed above, for nine predictors.
2. **Enriched model:** all 21 predictors, adding the ten health indicators and two
   care-access variables.
3. **Selected subsets:** mutual-information filtering, RFE and L1 selection applied
   to the enriched set, with selection fitted inside cross-validation.

Each comparison will use identical splits so that changes in performance can be
attributed more clearly to the information or method being evaluated.

## Experimental protocol

### Data preparation

Validate the schema, target values, category ranges and missingness before fitting.
Inspect repeated predictor profiles: identical survey responses do not necessarily
represent the same person, so duplicates will not be removed automatically.
Exclude `ID` and the target from predictors, and document all preprocessing choices.

Keep raw downloaded data outside version control. Record data provenance and
provide reproducible acquisition instructions when implementation begins.

### Baselines and candidate models

- **Trivial baseline:** a majority-class classifier, to expose why accuracy alone
  is misleading with an imbalanced target.
- **Main baseline:** logistic regression with appropriate preprocessing.
- **Candidates:** random forest and gradient boosting, followed by feature-selection
  comparisons. Model complexity and search budgets will remain manageable.

### Validation and leakage prevention

- Reserve a stratified **20% test set** and use the remaining **80%** for development.
- Use **five-fold stratified cross-validation** on development data, with seed **42**.
- Fit imputation, scaling, encoding and feature selection inside each training fold.
- If class weighting or resampling is tested, choose it using development data;
  resampling must occur inside the training folds only.
- Select hyperparameters and any decision threshold without consulting test labels.
- Freeze the chosen configurations before final test evaluation and do not retune
  from the test results. Report development and test performance separately.

### Evaluation

The primary selection metric is **average precision**, a summary of the
precision–recall curve suitable for emphasizing the positive class. Also report
precision, recall, F1, ROC-AUC, accuracy and the confusion matrix at a documented
threshold. Average precision must not be silently replaced by trapezoidal PR-AUC.

Report cross-validation variability, final test uncertainty, selected feature
counts and computation time. Compare errors across age and sex groups where sample
sizes permit. A higher recall must be discussed alongside the associated false
positive rate and precision.

## Four-week work plan

| Week | Work | Deliverable |
| --- | --- | --- |
| 1 | Confirm scope, team responsibilities, data provenance and exploratory analysis | Project specification and dataset description |
| 2 | Implement preprocessing, fixed splits and baselines | Reproducible baseline notebook and initial results |
| 3 | Compare models, feature sets and selection methods | Cross-validation comparison and error analysis |
| 4 | Freeze configurations, evaluate on test data and discuss limitations | Final notebook/code, report and presentation |

Team members and individual task ownership will be recorded before implementation;
no allocation is assumed in this initial specification.

## Reproducibility and current repository status

This repository currently contains the project specification only. There are no
training commands, dependency files, tests or model results yet. Implementation
will add a documented environment, data acquisition, executable experiments and
verification commands. All randomness and library versions will be recorded.

Contributions use a branch and a pull request targeting `main`. Experimental
claims must be backed by saved outputs from reproducible runs.

## Limitations

The survey is observational and relies on reported information. Some health
indicators may reflect an existing diagnosis or its consequences, which limits
interpretation as early detection. Performance on this dataset does not establish
clinical usefulness or transfer to another country or population. The supplied
export is not a substitute for a survey-weighted population prevalence analysis.

## Reference and data terms

CDC Diabetes Health Indicators [Dataset]. (2017). UCI Machine Learning Repository.
[DOI: 10.24432/C53919](https://doi.org/10.24432/C53919).

The year above follows the UCI citation and is not a claim about the survey year.
UCI directs users to the original dataset for usage terms and acknowledgements;
those terms must be retained when sharing derived data or results.
