# Team Roles and Tasks

All roles and dates are **[PROPOSED]**. Swap roles to fit people's strengths. Names to be filled in.

| Member | Name | Owns | Folders |
|---|---|---|---|
| 1 | _____ | Simulator, scenario, environment wrapper, solo runs, helicopter | `env/`, `scripts/run_solo.py` |
| 2 | _____ | AI brain (summarizer + decider), PPO training, baseline reproduction | `agents/`, `scripts/train.py` |
| 3 | _____ | Referee, federation rules, Shapley scoring, karma credits | `federation/`, `karma/` |
| 4 | _____ | Metrics, statistics, plots, safety shield, attacks and defenses | `eval/`, `safety/`, `attacks/` |
| Team lead | one of the above | Mentor contact, experiment log, report assembly, integration | `docs/`, `configs/experiments/` |

**Skills each role needs to pick up:**
- Member 1: BlueSky commands and Python API, basic geometry, Gymnasium/PettingZoo environment style
- Member 2: PyTorch, PPO, attention layers
- Member 3: Federated averaging, Shapley values, simple ledger logic
- Member 4: matplotlib, statistical tests (Mann-Whitney U, Holm correction), geometry for the shield; optional pandas for DataFrame inputs

---

## Timeline (14 weeks)

| Weeks | Team milestone |
|---|---|
| 1 to 2 | Setup, reading, interfaces agreed, overlap check of 2 preprints, GPU confirmed |
| 3 to 5 | Baseline: scenario + independent PPO (B1) + rule-based (B3) + solo runs; unfairness confirmed |
| 6 to 7 | Brain split into summarizer and decider; federation F1; normalized-delay metric |
| 8 to 9 | F2, F3; Shapley scoring; karma K1, K2 |
| 10 to 11 | Full runs with 3 seeds; attacks and defenses; route-leakage test (now core) |
| 12 | Stretch: helicopter and shield if not core |
| 13 | Analysis, plots, statistics |
| 14 | Report, presentation, demo video |

**Fallback if weeks 3 to 5 slip:** keep 2 companies and only F1, F2, K2. That still answers the main questions.

---

## Member 1: Environment

**Weeks 1 to 2**
- [ ] Learn BlueSky: create, move and delete aircraft by command and from Python
- [ ] Get Frisco route details from Sharifi (4 routes, ~10.33 km, merges at WP3 and WP7, intersection at WP9)
- [ ] Write `scenario_frisco.yaml` with waypoints and fleet specs (X: 44.88 m/s, 1.71 m/s², 1000 m; Y: 30.12 m/s, 1.02 m/s², 750 m)
- [ ] Decide headless run method and time per step (3 s)

**Weeks 3 to 5**
- [ ] `bluesky_wrapper.py`: multi-agent `reset()` and `step(actions)` returning obs, rewards, done flags, info
- [ ] Observations with relative positions only (privacy update)
- [ ] Reward following Sharifi
- [ ] Per-step and per-flight logging for Member 4
- [ ] `run_solo.py`: each fleet alone, record solo travel times
- [ ] Measure speed: how many simulated episodes per hour on CPU and GPU machine

**Weeks 6 to 12**
- [ ] Contest detection hook (two companies' drones within 500 m within 60 s) for Member 3
- [ ] Exam suite scenarios (hard crossings) for Member 3
- [ ] Manned helicopter that crosses routes (core or stretch, **[OPEN]**)
- [ ] Optional: X+X control scenario and X+Y+Y three-company scenario

## Member 2: AI brain and training

**Weeks 1 to 2**
- [ ] Read Brittain and Wei and Sharifi network sections in detail; write down layer sizes and input dimensions
- [ ] Read CleanRL PPO and run it on a simple Gymnasium task to learn the loop

**Weeks 3 to 5**
- [ ] `summarizer.py`: own-state encoder (FC64), neighbor encoder (FC64), attention (64×64), intent head (3×FC128)
- [ ] `decider.py`: 2×FC128 policy and value heads
- [ ] `ppo.py` and `buffer.py` with Sharifi's settings (lr 1e-4, entropy 1e-3, clip 0.2, batch 512, 8 epochs, Adam, GAE)
- [ ] Train B1 (independent) on small scenario, then full scenario
- [ ] Centralized B2 for reference

**Weeks 6 to 9**
- [ ] Clean split so only summarizer parts are exported and imported (`get_shared()`, `set_shared()`)
- [ ] Apply the "allowed actions" mask from shield and bid before choosing the action
- [ ] Ablations: no intent head, no attention (if time)

**Weeks 10 to 11**
- [ ] Run the full experiment grid with Team lead

## Member 3: Federation and karma

**Weeks 1 to 2**
- [ ] Read FedAvg idea, Chen et al. (federation loop), CARMA, a Shapley-in-FL paper
- [ ] Verify the q-FFL citation (Li et al., ICLR 2020)
- [ ] Look at Chen's code for how the federation round is written

**Weeks 3 to 5 (can start before the baseline is ready, using dummy models)**
- [ ] `aggregation.py`: F1 equal, F2 fairness-weighted, F3 contribution-weighted
- [ ] `ledger.py`: balances, spend, pool, giveback (uniform and need-based), 60% cap; unit tests
- [ ] `bidding.py`: fixed bidding rule (**[OPEN]**: which rule)

**Weeks 6 to 9**
- [ ] `referee.py`: receive updates every 50 episodes, integrity check, score, merge, mint credits, send back
- [ ] `shapley.py`: exact Shapley for 2 to 3 companies, utility = NMAC reduction + 0.1 × LoWC reduction, smoothing 0.8/0.2
- [ ] `exam_suite.py` with Member 1; rotation of exam scenarios
- [ ] `integrity.py`: cosine similarity check, shadow (hidden second) exam

## Member 4: Evaluation, safety, attacks

**Weeks 1 to 2**
- [ ] Read Sharifi's fairness and metrics section and ElSayed-Aly shield paper
- [x] Write `metrics.py` against fake logs: NMAC count, LoWC count, travel time, normalized delay Dk = (T_shared − T_solo) / T_solo, delay gap, worst-off delay, Ft = (1 − |TA − TB| / max) × 100

**Weeks 3 to 5**
- [x] `stats.py`: Mann-Whitney U, Holm correction, effect sizes
- [x] `plots.py`: standard figures (delay per company, NMAC per setup, credit balances over time)
- [ ] Evaluate B1 and B3 when ready (300 evaluation episodes each)

**Weeks 6 to 9**
- [ ] `shield.py`: 30 s worst-case look-ahead, 100 m drone / 500 m helicopter, fallback slow down; unit tests with hand-made cases
- [ ] Measure how often the shield intervenes

**Weeks 10 to 11**
- [ ] Attacks A1 free riding, A2 exam gaming; A3 rival slowdown only if time
- [ ] Route-leakage test (now core): can one company reconstruct the other's routes from shared updates? See `06_DESIGN_UPDATES.md`

## Team lead (in addition to own member role)

- [ ] Weekly 30-minute sync; a short written status in the shared drive
- [ ] Keep the experiment log sheet
- [ ] Take `07_OPEN_DECISIONS_AND_MENTOR_QUESTIONS.md` to the mentor
- [ ] Integration: one script that runs a full experiment from a single config
- [ ] Report outline from Week 6; each member writes their own sections

---

## Weekly rhythm

| Day | What |
|---|---|
| Monday | 30 min sync: done, next, blocked |
| Midweek | Pull requests reviewed within 48 hours |
| Friday | Update experiment log and write 5 lines of status |
| Every 2 weeks | Mentor check-in |
