## What this changes

<!-- One or two sentences. Link the issue: Closes #... -->

## Checklist

- [ ] Branch is named `memberN/feature` and targets `main`
- [ ] `pytest` passes locally; `main` still runs after this merge
- [ ] New settings are in `configs/`, not hard-coded
- [ ] Scripts take `--seed`
- [ ] Tested small first (2 drones per company, 10 episodes) if this touches training
- [ ] Raw logs are written, metrics computed afterwards
- [ ] Experiment log updated (if runs were made)
- [ ] No invented numbers; claims tagged [FROM PAPER] / [PROPOSED] / [OPEN] / [FOR REVIEW]
- [ ] No PDFs, results, checkpoints or large files added

## How it was tested

<!-- Commands and what you saw. -->
