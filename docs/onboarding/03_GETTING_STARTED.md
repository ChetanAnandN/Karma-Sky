# Getting Started: Setup, Repo, First Week

This is the practical file. Follow it in order.

---

## 1. What you need

| Item | Notes |
|---|---|
| Laptop | Any. Development and short tests run on CPU |
| GPU machine | Needed for full training. Estimated about 300 GPU-hours for the core experiments (rough estimate from Sharifi's >7 h per run on an RTX 3090 × ~42 runs). **[OPEN]**: confirm access (college lab, Colab Pro, Kaggle, cloud credits) |
| Python | Use 3.10 or 3.11. Check BlueSky's GitHub for the currently supported versions before installing |
| Git and GitHub | One shared repo, see Section 3 |
| Shared drive | For papers, notes and result files too large for Git |

---

## 2. Install

### Step 1: create an environment
```bash
# with conda (recommended)
conda create -n karmasky python=3.11 -y
conda activate karmasky

# or with venv
python3.11 -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
```

### Step 2: install packages
```bash
pip install bluesky-simulator    # BlueSky air traffic simulator (PyPI latest checked Oct 2026: 1.1.1)
pip install bluesky-gym          # RL environments on top of BlueSky (latest checked: 0.2.0)
pip install torch                # pick the right CUDA build from pytorch.org for GPU machines
pip install gymnasium pettingzoo numpy scipy matplotlib pyyaml tensorboard pytest
```

Pandas is optional and is only needed when passing a DataFrame to the evaluation credit-balance plot.

Save the exact versions once it works:
```bash
pip freeze > requirements-lock.txt
```

### Step 3: check it works
```bash
python -c "import bluesky, torch; print('bluesky ok, torch', torch.__version__, 'cuda', torch.cuda.is_available())"
```

Then open the BlueSky GUI once to see the simulator (`bluesky` in a terminal) and run one of BlueSky-Gym's example environments following its README.

**Things to verify yourself in Week 1 (we have not confirmed these):**
- Whether BlueSky-Gym has any multi-agent environment. If not, we write our own multi-agent wrapper (planned anyway).
- How to run BlueSky headless (no GUI) from Python. BlueSky-Gym's source shows how it initializes the simulator; copy that pattern.
- Whether Brittain and Wei's code is public (search GitHub user `marcbrittain`).

### Useful links
- BlueSky: https://github.com/TUDelft-CNS-ATM/bluesky
- BlueSky-Gym: https://github.com/TUDelft-CNS-ATM/bluesky-gym
- Chen et al. code (federated MARL reference): https://github.com/Cirrick/Multi_UAV_Data_Harvesting
- PettingZoo (multi-agent environment standard): https://pettingzoo.farama.org
- PPO explained (Spinning Up): https://spinningup.openai.com/en/latest/algorithms/ppo.html
- CleanRL PPO (single-file reference implementation): https://github.com/vwxyzjn/cleanrl

---

## 3. Repository structure [PROPOSED]

```
karmasky/
├── README.md
├── requirements.txt
├── configs/
│   ├── scenario_frisco.yaml      # routes, waypoints, fleet specs
│   ├── train_default.yaml        # PPO settings from Sharifi
│   └── experiments/              # one yaml per experiment (B1, F1, K2, ...)
├── karmasky/
│   ├── env/                      # Member 1
│   │   ├── scenario.py           # routes, merges, intersection, spawning
│   │   ├── bluesky_wrapper.py    # multi-agent wrapper around BlueSky
│   │   ├── observations.py       # build own-state and neighbor features
│   │   ├── rewards.py
│   │   └── helicopter.py         # manned aircraft (stretch or core, OPEN)
│   ├── agents/                   # Member 2
│   │   ├── summarizer.py         # shared encoder + attention + intent head
│   │   ├── decider.py            # private policy and value heads
│   │   ├── ppo.py
│   │   └── buffer.py             # the diary
│   ├── federation/               # Member 3
│   │   ├── referee.py
│   │   ├── aggregation.py        # F1, F2, F3
│   │   ├── shapley.py
│   │   ├── exam_suite.py         # secret hard-crossing scenarios
│   │   └── integrity.py          # cosine checks, shadow exam
│   ├── karma/                    # Member 3
│   │   ├── ledger.py             # balances, pool, giveback, cap
│   │   └── bidding.py            # contest detection and bid rules
│   ├── safety/                   # Member 4
│   │   └── shield.py
│   ├── attacks/                  # Member 4
│   │   ├── free_rider.py
│   │   └── exam_gaming.py
│   └── eval/                     # Member 4
│       ├── metrics.py            # NMAC, LoWC, delay, normalized delay, Ft
│       ├── stats.py              # Mann-Whitney U, Holm correction, effect sizes
│       └── plots.py
├── scripts/
│   ├── train.py                  # python scripts/train.py --config configs/experiments/B1.yaml
│   ├── evaluate.py
│   └── run_solo.py               # each fleet flying alone, for normalized delay
├── tests/
├── results/                      # gitignored, keep on shared drive
└── docs/                         # project docs; these onboarding files are in docs/onboarding/
```

Rule: **each folder has one owner**, but anyone can open a pull request. The owner reviews.

---

## 4. Interfaces between modules (agree on these in Week 1)

These are the "contracts" so four people can work in parallel. Write them down as Python type hints in a file `karmasky/interfaces.py` in Week 1.

| From | To | What is passed |
|---|---|---|
| env | agents | `obs[drone_id] = {"own": array(d_own), "neighbors": array(n, d_nb), "mask": array(n)}` |
| agents | env | `action[drone_id] in {0: slow, 1: hold, 2: speed up}` plus `scores[drone_id]` (3 numbers) |
| env | safety | positions, velocities, max speed and acceleration of every aircraft |
| safety | agents/env | `allowed[drone_id] = [bool, bool, bool]` |
| karma | env | `priority[drone_id] in {"go", "yield", None}` for each open contest |
| agents | federation | `summarizer.state_dict()` changes since last round |
| federation | agents | merged summarizer weights |
| federation | karma | contribution score per company → credits minted |
| env | eval | per-step log: time, positions, actions, distances, flags; per-flight: start, end, solo time |

Dimensions (`d_own`, `d_nb`) follow Sharifi and Brittain and Wei. Member 2 reads the papers and fills them in.

---

## 5. Coding rules

1. **Configs, not hard-coded numbers.** Every setting lives in a YAML file. The config used is saved next to each result.
2. **Seeds.** Every run takes a `--seed`. We run 3 seeds per setup.
3. **Log everything raw.** Save per-step and per-flight logs (CSV or Parquet). Metrics are computed afterwards, so we can add metrics without rerunning.
4. **Small first.** Every new feature is tested with 2 drones per company and 10 episodes before a full run.
5. **Branches and pull requests.** `main` always runs. Work in branches like `member2/ppo`. Another member reviews.
6. **Tests.** At least: the shield never allows an action that breaks 100 m in a hand-made test; the ledger never goes negative and respects the 60% cap; metrics match a hand-calculated example.
7. **Experiment log.** A shared sheet: date, who, config, seed, git commit, result folder, notes. Every run goes in.

---

## 6. Week 1 checklist (everyone)

- [ ] Read `00` to `02` and `06` in this folder
- [ ] Install everything (Section 2), run the check command
- [ ] Open BlueSky GUI, create two aircraft by hand, watch them fly
- [ ] Run one BlueSky-Gym example environment
- [ ] Read the 3 core papers (see `05_READING_LIST.md`)
- [ ] Create the GitHub repo with the folder structure above (team lead)
- [ ] Team meeting: agree on `interfaces.py`, the experiment-log sheet, and meeting schedule
- [ ] Two people read arXiv 2511.11616 and 2605.20625 and report any overlap with our idea
- [ ] Confirm GPU access

Your role-specific tasks are in `04_TEAM_ROLES_AND_TASKS.md`.

---

## 7. First milestone: "the baseline works"

Before any federation, credits or shields, we must have:
1. The Frisco scenario running in BlueSky with 2 companies × 10 drones.
2. Independent PPO training (setup B1) that learns to avoid near misses.
3. Solo runs (each fleet alone) for normalized delay.
4. The unfairness Sharifi reported shows up in our runs (the weaker company is delayed more).

If step 4 does not appear, stop and discuss with the mentor before building further, since the whole project depends on it.
