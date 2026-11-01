# Contributing to KarmaSky

Based on the coding rules in [docs/onboarding/03_GETTING_STARTED.md](docs/onboarding/03_GETTING_STARTED.md), Section 5.

## Branches and pull requests

- Never commit directly to `main`. Work on a branch named `memberN/feature`, for example `member2/ppo` or `member3/ledger`.
- Open a pull request into `main`. At least **one other member reviews and approves** before merging. The folder owner (see `.github/CODEOWNERS`) reviews changes to their folder.
- Review pull requests within 48 hours (weekly rhythm in `04_TEAM_ROLES_AND_TASKS.md`).
- **`main` must always run.** Before merging, `pytest` passes and the smoke test imports every module.

## Run rules

1. **Settings live in configs, not in code.** Every number goes in a YAML file under `configs/`. Save the config used next to each result.
2. **Seed every run.** Every script takes `--seed`. We run 3 seeds per setup.
3. **Log raw data.** Save per-step and per-flight logs (CSV or Parquet). Compute metrics afterwards so new metrics do not need reruns.
4. **Test small first.** Every new feature runs with 2 drones per company and 10 episodes before any full run.
5. **Update the experiment log.** Every run goes in the shared sheet: date, who, config, seed, git commit, result folder, notes.

## Tests

At least (03, Section 5, rule 6):
- the shield never allows an action that breaks 100 m in a hand-made test;
- the ledger never goes negative and respects the 60% cap;
- metrics match a hand-calculated example.

## Writing and numbers

- Tag claims as in the docs: [FROM PAPER] (with citation), [PROPOSED], [OPEN], [FOR REVIEW].
- No invented numbers. If we do not know, write "to be measured" or TODO.
- Results, checkpoints and research PDFs do not go in Git (see `.gitignore`); keep them on the shared drive.
