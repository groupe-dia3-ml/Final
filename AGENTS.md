# Project conventions

This project classifies the survey diabetes status defined in README.md and
compares lifestyle/demographic features with an enriched health-indicator model.
Keep project deliverables in English and distinguish plans from measured results.

## Build, run and verification

This repository contains the specification, final report, oral defense notes and
an evidence snapshot. It has no Python application to build. Check Markdown links,
verify reports/evidence/SHA256.json and run `git diff --check` before commits.

The companion cdc-benchmark and synthetic-data repositories contain runnable code.
Each uses Python 3.14, `requirements-dev.txt`, `python -m src.experiment` and
`python scripts/execute_notebook.py`. Their own AGENTS.md files give lint/type/test
commands. Keep report numbers synchronized with their saved results and hashes.
The original README work plan is historical; measured findings are in the report.

## Data and evaluation constraints

- Use the exact UCI binary export linked in README.md and record its checksum.
- Check target definitions before switching to another dataset variant.
- Exclude the target and ID from predictors. Age is a band, not an exact age.
- Keep preprocessing and feature selection inside training folds.
- Never tune models or thresholds against the reserved test labels.
- Do not equate repeated predictor profiles with duplicate participants.
- Keep raw downloads out of version control; preserve source acknowledgements.
- Report associations rather than causal effects or future disease onset.
- Preserve the synthetic starter generator; measured prevalence is about 19%.
- Synthetic coefficients are assumptions. Never use oracle probabilities as inputs.
- Different prevalence prevents direct AP ranking across the two phases.
- Do not claim individual team contributions without verified information.

## Contributions

Use short feature/fix/refactor branches and conventional commits. Submit changes
through a pull request to main. Document evidence for performance claims, and
update these instructions when runnable code or new verification tools are added.
