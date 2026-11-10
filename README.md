# KarmaSky

Contribution-earned priority for fair shared learning between competing drone delivery operators (SDG 9 semester project).
Several delivery companies fly drones in the same city airspace and improve their collision-avoidance AI together through federated multi-agent reinforcement learning, without sharing raw flight data. A neutral referee scores each company's contribution, companies earn non-tradable karma credits to spend on priority at busy crossings, and a hard safety shield always overrides credits. Everything runs in simulation (BlueSky); no physical drones.

**Status:** design stage. The Member 4 evaluation modules (metrics, statistics and plots) are implemented; the simulator, training and federation pipeline remain in development.

## Start here

- New to the project: [docs/onboarding/00_START_HERE.md](docs/onboarding/00_START_HERE.md)
- Whole-project plan, tiers, phases and gates: [docs/plan/MASTER_PLAN.md](docs/plan/MASTER_PLAN.md)
- Literature survey and overlap check: [research/README.md](research/README.md)

## Quick setup

From [03_GETTING_STARTED.md](docs/onboarding/03_GETTING_STARTED.md), Section 2. Use Python 3.10 or 3.11 (check BlueSky's supported versions first).

```
# with conda (recommended)
conda create -n karmasky python=3.11 -y
conda activate karmasky

# or with venv
python3.11 -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

pip install -r requirements.txt  # for GPU torch, pick the CUDA build from pytorch.org

# check it works
python -c "import bluesky, torch; print('bluesky ok, torch', torch.__version__, 'cuda', torch.cuda.is_available())"
pytest tests/test_smoke.py

# once it works, save exact versions
pip freeze > requirements-lock.txt
```

The evaluation tests and sample-only demo can be run from the repository root:

```bash
pytest tests/test_member4_eval.py -q
python examples/run_demo.py
```

The demo writes generated files to the ignored `examples/demo_results/` directory. Its CSV inputs and statistical arrays are illustrative fixtures, not experimental results.

Pandas is optional; it is only needed when passing a pandas DataFrame to `plot_credit_balances`. Iterable rows such as dictionaries work without Pandas.

## Repository map

```
configs/            scenario_frisco.yaml, train_default.yaml, experiments/ (one yaml per setup in 09)
karmasky/
  interfaces.py     typed contracts between modules (agree in Week 1)
  env/              Member 1: scenario, BlueSky wrapper, observations, rewards, helicopter
  agents/           Member 2: summarizer (shared), decider (private), PPO, buffer
  federation/       Member 3: referee, aggregation F1/F2/F3, Shapley, exam suite, integrity
  karma/            Member 3: ledger, bidding
  safety/           Member 4: shield
  attacks/          Member 4: free riding, exam gaming
  eval/             Member 4: metrics, statistics, plots
scripts/            train.py, evaluate.py, run_solo.py
tests/              smoke test and unit tests
results/            not in Git; results live on the shared drive
docs/
  onboarding/       00 to 09 onboarding files
  plan/             MASTER_PLAN.md
  design/           project brief, architecture
  presentations/    Phase-1 slides
research/           survey summaries (PDFs are not in Git)
```

## Team

| Member | Name | Owns |
|---|---|---|
| 1 | | Simulator, scenario, environment wrapper, solo runs, helicopter (`env/`, `scripts/run_solo.py`) |
| 2 | | AI brain, PPO training, baseline reproduction (`agents/`, `scripts/train.py`) |
| 3 | | Referee, federation rules, Shapley scoring, karma credits (`federation/`, `karma/`) |
| 4 | | Metrics, statistics, plots, safety shield, attacks and defenses (`eval/`, `safety/`, `attacks/`) |
| Team lead | | Mentor contact, experiment log, report assembly, integration (`docs/`, `configs/experiments/`) |

Mentor:

## Five rules for the whole team

From [00_START_HERE.md](docs/onboarding/00_START_HERE.md):

1. **Simulation only.** Everything runs in the BlueSky simulator. Never claim real-world results.
2. **Never call borrowed work ours.** The 5 building blocks (MARL base, federated RL, karma credits, Shapley scoring, safety shields) are other people's work. Our contribution is combining them for competing operators and the fairness questions we answer.
3. **No invented numbers.** Every number in the report comes from our runs or a cited paper. If we do not know, we write "to be measured".
4. **Safety beats everything.** In code and in the report: manned aircraft first, then shield, then credits, then the AI's choice. Credits never enter the reward.
5. **Reproduce before you add.** We first reproduce the Sharifi baseline. Nothing new is added until the baseline works.

See [CONTRIBUTING.md](CONTRIBUTING.md) for branches, pull requests and run rules. License: [MIT](LICENSE).
