# Project conventions

This project classifies the survey diabetes status defined in README.md and
compares lifestyle/demographic features with an enriched health-indicator model.
Keep project deliverables in English and distinguish plans from measured results.

## Build, run and verification

The repository currently contains documentation only. There are no build,
training, type-check or test commands yet. Check Markdown and run
`git diff --check` before committing documentation. When implementation is added,
record the actual setup, execution and verification commands here.

## Data and evaluation constraints

- Use the exact UCI binary export linked in README.md and record its checksum.
- Check target definitions before switching to another dataset variant.
- Exclude the target and ID from predictors. Age is a band, not an exact age.
- Keep preprocessing and feature selection inside training folds.
- Never tune models or thresholds against the reserved test labels.
- Do not equate repeated predictor profiles with duplicate participants.
- Keep raw downloads out of version control; preserve source acknowledgements.
- Report associations rather than causal effects or future disease onset.

## Contributions

Use short feature/fix/refactor branches and conventional commits. Submit changes
through a pull request to main. Document evidence for performance claims, and
update these instructions when runnable code or new verification tools are added.
