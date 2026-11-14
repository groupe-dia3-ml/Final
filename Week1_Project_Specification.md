# Project Specification: Diabetes Risk Estimation from Lifestyle and Clinical Indicators

Machine Learning Course — ESILV A4, Group DIA 3  
Academic Year 2026–2027  
Milestone: Week 1 Project Specification (15%)

---

## 1. Project Title
Estimating Diabetes and Prediabetes Risk from Self-Reported Lifestyle and Clinical Indicators: A Comparative Benchmark and Synthetic Noise Resilience Analysis.

---

## 2. Team Members
- Louis Le Forestier (Lead, Benchmark & Pipeline Architecture)
- Team Member 2 (Exploratory Data Analysis & Feature Engineering)
- Team Member 3 (Synthetic Data Generation & Noise Protocols)
- Team Member 4 (Model Evaluation & Calibration Analysis)

*GitHub Organization:* [https://github.com/groupe-dia3-ml](https://github.com/groupe-dia3-ml)

---

## 3. Context and Motivation
Type 2 diabetes represents a major public health challenge worldwide, affecting hundreds of millions of individuals and generating substantial clinical and economic burdens through cardiovascular, renal, and neurological complications. A critical factor in managing diabetes is early screening: prediabetes and early-stage diabetes are frequently asymptomatic and remain undiagnosed for years.

Traditional clinical screening relies on invasive venous blood tests, such as fasting plasma glucose or glycated hemoglobin (HbA1c). Developing reliable, non-invasive screening tools based on accessible lifestyle questionnaires (diet, physical activity, smoking, alcohol) and basic physical indicators (age, BMI, self-reported blood pressure) offers significant potential for preliminary risk stratification in outpatient and digital health settings.

---

## 4. Problem Statement and Research Questions
The core problem addressed in this project is twofold:

1. **Phase 1 (Empirical Benchmark):** To what extent can a concise set of self-reported lifestyle and clinical indicators reliably classify diabetes/prediabetes status in a large population survey? Specifically, how much predictive power is gained by adding clinical indicators (BMI, hypertension, cholesterol) over pure lifestyle habits (diet, activity, smoking)?
2. **Phase 2 (Synthetic Noise Resilience):** When survey data is contaminated by realistic reporting errors (such as systemic under-reporting of body weight or lifestyle habits) and uninformative noise questions, can simple, transparent machine learning models accurately recover the true underlying risk parameters?

*Primary Research Question:* How well can simple, interpretable classifiers predict calibrated diabetes risk probabilities from survey responses, and how resilient are these models to self-reporting bias and noise?

---

## 5. Project Objectives
The measurable objectives of this 4-week project are:
- Establish a rigorous, leak-free benchmark pipeline on the 253,680 records of the CDC Diabetes Health Indicators dataset.
- Formulate the model output as a continuous, calibrated risk probability P(Y = 1 | X) rather than an arbitrary binary label, allowing threshold customization for clinical screening.
- Compare feature subsets: a 9-feature lifestyle/demographic model vs. the full 21-feature enriched clinical model.
- Restrict candidate models strictly to simple, interpretable families: Standardized Logistic Regression, shallow Decision Trees (depth <= 5), Gaussian Naive Bayes, and k-Nearest Neighbors.
- Design a controlled synthetic dataset where true biological risk weights are mathematically known, injecting realistic reporting noise to benchmark parameter recovery.
- Produce an end-to-end, reproducible open-source codebase structured across dedicated repositories on GitHub.

---

## 6. Dataset Description
The empirical investigation uses the **CDC Diabetes Health Indicators** dataset, available on the UCI Machine Learning Repository (Dataset ID: 891).

- **Data Source:** Behavioral Risk Factor Surveillance System (BRFSS), administered by the U.S. Centers for Disease Control and Prevention (CDC).
- **Scale:** 253,680 survey respondents.
- **Predictors:** 21 discrete, binary, and ordinal features grouped into four categories:
  - *Lifestyle (5 features):* PhysActivity, Fruits, Veggies, Smoker, HvyAlcoholConsump.
  - *Demographics (4 features):* Sex, Age (13 ordered bands), Education (6 levels), Income (8 levels).
  - *Clinical Indicators (10 features):* BMI, HighBP, HighChol, CholCheck, Stroke, HeartDiseaseorAttack, GenHlth (1 to 5), MentHlth (0 to 30 days), PhysHlth (0 to 30 days), DiffWalk.
  - *Healthcare Access (2 features):* AnyHealthcare, NoDocbcCost.
- **Target Variable:** `Diabetes_binary`:
  - `0`: No diabetes reported (218,334 respondents, 86.07%).
  - `1`: Prediabetes or confirmed diabetes reported (35,346 respondents, 13.93%).
- **Integrity Check:** The official CSV export has an exact SHA-256 checksum of `9f71fda9d4ae5f4878c99b9233b6a16accfa9a17c194116a6b78100540934964`, with zero missing values across all 253k entries.
- **Dataset Limitations:** The dataset is cross-sectional and relies entirely on self-reported survey answers rather than direct clinical measurements. Consequently, it reflects association at survey time rather than causal progression.

---

## 7. Machine Learning Task
The task is formulated as **probabilistic binary classification**:
Given a feature vector X in R^d representing survey answers, the model outputs an estimated risk probability:
P_hat = P(Diabetes = 1 | X) in [0, 1]

Clinical screening requires probability outputs rather than rigid 0/1 predictions, as decision thresholds can be tuned based on health priorities (e.g. lowering the decision threshold to 0.20 to achieve high recall/sensitivity and avoid missing potential cases).

---

## 8. Baseline Strategy
- **Trivial Baseline:** A majority-class dummy classifier (predicting 0 for all cases) to establish that raw accuracy (86.07%) is a misleading metric under class imbalance.
- **Primary Methodological Baseline:** Standardized Logistic Regression:
  Pipeline([('scaler', StandardScaler()), ('clf', LogisticRegression(max_iter=1000, random_state=42))])
- **Justification:**
  - Standard, medically accepted standard for epidemiological risk scoring.
  - Highly interpretable: exponentiated model weights exp(w_j) directly provide odds ratios for each habit.
  - Sigmoid activation outputs naturally calibrated posterior probabilities.
  - Computationally efficient on 253,680 samples.

---

## 9. Evaluation Strategy

### Data Partitioning and Leakage Prevention
- **Held-Out Test Set:** A stratified 20% split (50,736 samples) reserved strictly for final testing, untouched during model tuning and feature selection.
- **Cross-Validation:** 5-fold stratified cross-validation on the 80% development split (202,944 samples) using fixed random seed 42.
- **Leakage Prevention:** All preprocessing (StandardScaler) and any feature selection (Lasso L1 or SelectKBest) are fitted strictly inside each cross-validation fold.

### Metrics Suite
Because raw classification accuracy obscures false negatives in imbalanced medical targets, the evaluation uses:
- **Average Precision (PR-AUC):** Primary metric, summarizing the Precision-Recall curve without sensitivity to class skew.
- **ROC-AUC:** Measures ranking discrimination across all possible decision thresholds.
- **Brier Score Loss:** Measures probability calibration quality (mean squared error between predicted probability and actual binary outcome).
- **Calibration Curves:** 10-bin reliability diagrams comparing predicted risks against observed empirical frequencies.
- **Recall (Sensitivity) and Precision at Tuned Thresholds (0.15, 0.20, 0.30, 0.50).**

---

## 10. Initial Work Plan and Task Distribution

The project follows a 4-week roadmap aligned with the course milestones:

| Week | Milestone & Objectives | Deliverables | Member Assignments |
|---|---|---|---|
| **Week 1** | Project definition, dataset verification, repository setup, and specification document. | - Week 1 Specification Document<br>- GitHub organization layout<br>- Starter notebooks | **All:** Scope & specification<br>**Louis:** Ingestion & GitHub org |
| **Week 2** | Data preprocessing, exploratory data analysis, and baseline model implementation. | - Clean data pipeline<br>- 5-fold CV baseline results<br>- Initial calibration curves | **Member 2:** EDA & distributions<br>**Louis:** Stratified CV pipeline<br>**Member 4:** Baseline odds ratios |
| **Week 3** | Simple model comparisons, feature selection (lifestyle vs. enriched), and synthetic generation. | - Simple models benchmark table<br>- Synthetic cohort generator<br>- Noise injection protocols | **Member 3:** Synthetic generator & noise<br>**Member 2:** Feature selection (mRMR, L1)<br>**Member 4:** Model comparisons |
| **Week 4** | Test set evaluation, parameter recovery analysis, and final synthesis. | - Final report<br>- Polished notebooks<br>- Oral presentation slides | **Louis:** Synthesis & test evaluation<br>**All:** Final report & defense |

---

## Reference
CDC Diabetes Health Indicators [Dataset]. (2017). UCI Machine Learning Repository.  
DOI: [https://doi.org/10.24432/C53919](https://doi.org/10.24432/C53919)
