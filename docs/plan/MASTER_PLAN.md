# KarmaSky Master Plan

How to work on the project **as a whole**: what matters most, in what order, and when to stop and check. For who does what, see [`04_TEAM_ROLES_AND_TASKS.md`](../onboarding/04_TEAM_ROLES_AND_TASKS.md). This file is about the project, not individuals.

All dates and settings are **[PROPOSED]**. Where this file disagrees with older files, [`06_DESIGN_UPDATES.md`](../onboarding/06_DESIGN_UPDATES.md) and this file win.

---

## 1. The one sentence that drives every decision

> Show, in simulation, whether shared learning plus contribution-earned priority reduces the delay gap between a strong and a weak drone fleet **without making the airspace less safe**.

If a task does not help answer this sentence, it waits.

---

## 2. Priority tiers

| Tier | What | Rule |
|---|---|---|
| **Tier 0: Must exist or there is no project** | Frisco scenario in BlueSky, 2 companies × 10 drones, independent PPO baseline (B1), solo runs, normalized-delay metric, unfairness confirmed | Nothing else starts being trained until this works |
| **Tier 1: The core contribution** | Brain split (summarizer + decider), federation F1 and F2, Shapley scoring, karma credits K2, safety and fairness evaluation with 3 seeds, statistics | This is what the report is about |
| **Tier 2: Makes it strong** | F3, K1 (no giveback/cap), B2 and B3 references, X+X control, free-riding and exam-gaming attacks, route-leakage test, privacy fixes | Do after Tier 1 has results |
| **Tier 3: Stretch** | Manned helicopter + shield (unless the mentor makes it core), rival-slowdown attack, X+Y+Y three companies, differential privacy sweep, ablations, learned bidding | Only if time is left |

**Rule:** a lower tier is never started while a higher tier is broken. Code for a lower tier can be written in parallel (for example, the ledger with dummy data), but training runs follow tier order.

---

## 3. Phases and gates

Each phase ends with a **gate**: a yes/no check. If the answer is no, fix it before moving on, or apply the fallback.

### Phase 0: Foundation (Weeks 1 to 2)

**Goal:** everyone understands the project, tools installed, scope agreed.

| Do | Why it matters |
|---|---|
| Read core papers and research summaries | Shared understanding |
| Read arXiv 2511.11616 and 2605.20625 | **Novelty risk.** If someone already did this, we must know now, not in Week 12 |
| Mentor meeting with [`07_OPEN_DECISIONS...`](../onboarding/07_OPEN_DECISIONS_AND_MENTOR_QUESTIONS.md) | Scope must be fixed before building |
| Install BlueSky, check BlueSky-Gym multi-agent support | Decides how much wrapper work is needed |
| Confirm GPU access | Decides how many runs we can afford |
| Agree `interfaces.py` | Lets 4 people work in parallel |

**Gate 0:**
- [ ] Mentor approved scope (or told us what to change)
- [ ] No paper found that already does our core idea
- [ ] GPU access confirmed, or reduced plan agreed
- [ ] BlueSky runs headless from Python on at least one machine

### Phase 1: Baseline (Weeks 3 to 5) **CRITICAL PATH**

**Goal:** reproduce the Sharifi setting and see the unfairness ourselves.

| Do | Why it matters |
|---|---|
| Scenario + multi-agent wrapper | Everything runs on this |
| PPO agent with attention and intent head | Our base learner |
| Small test (2 drones per company, 10 episodes) first | Catches bugs in minutes, not hours |
| Full B1 training, solo runs, B3 rule-based | Baseline numbers |
| Metrics pipeline on real logs | We need to measure before we improve |
| Meanwhile, in parallel: ledger, aggregation, shield code with unit tests on dummy data | Saves time later |

**Gate 1 (most important gate in the project):**
- [ ] B1 learns: near misses drop during training
- [ ] Weak fleet Y shows larger normalized delay than X in shared airspace
- [ ] Results repeat across at least 2 seeds

**If Gate 1 fails:** stop new features. Debug for up to one week. If unfairness still does not appear, meet the mentor: options are changing the scenario (denser traffic, bigger fleet difference) or reframing the question. Do not build federation on a baseline that does not work.

### Phase 2: Core mechanism (Weeks 6 to 9)

**Goal:** build and connect the new parts.

| Order | Do |
|---|---|
| 1 | Split brain into shared and private parts, with privacy fix (share neighbor/attention/intent only) [OPEN, see 06] |
| 2 | Referee + F1 equal merge. Check performance does not collapse after a merge |
| 3 | F2 fairness-weighted merge |
| 4 | Exam suite + Shapley scoring + smoothing |
| 5 | Karma: contest detection, bidding, ledger, giveback, cap (K2) |
| 6 | F3 and K1 if time |

**Gate 2:**
- [ ] A full federated run (F1) completes and safety is not clearly worse than B1
- [ ] Shapley scores are computed for all 4 combinations and are stable after smoothing
- [ ] Credits flow: no negative balances, cap respected, bids change who goes first
- [ ] Unit tests pass for shield/priority order (helicopter > shield > credits > policy)

**If behind:** drop F3 and K1. Keep F1, F2, K2.

### Phase 3: Full experiments (Weeks 10 to 11)

**Goal:** produce the numbers for the report.

| Priority order of runs |
|---|
| 1. B1, B3, solo runs (3 seeds) |
| 2. F1, F2 |
| 3. K2 |
| 4. K2 + free riding (A1), K2 + exam gaming (A2) |
| 5. Route-leakage test with and without privacy fixes |
| 6. X+X control |
| 7. F3, K1, B2 |

**Gate 3:**
- [ ] Every Tier 1 setup has 3 seeds and 300 evaluation episodes
- [ ] Every run is in the experiment log with config and commit
- [ ] First plots exist for delay gap and near misses per setup

**Freeze rule:** after Week 11, no new features. Only bug fixes and reruns.

### Phase 4: Stretch (Week 12)

Only if Gate 3 passed. Pick at most two: helicopter + shield, rival-slowdown attack, X+Y+Y, ablations, DP noise. If the mentor made the helicopter core, it moves into Phase 2 and this week becomes buffer.

### Phase 5: Analysis and writing (Weeks 13 to 14)

| Do |
|---|
| Statistics: Mann-Whitney U, Holm correction, effect sizes |
| Answer each research question in one paragraph with evidence |
| Write limitations honestly (simulation only, simplified physics, 2 to 3 companies) |
| Separate clearly: borrowed building blocks vs our contribution |
| Demo video of one contested crossing, with and without credits |
| Final presentation |

**Gate 5:**
- [ ] Every number in the report traces to a logged run or a cited paper
- [ ] Negative results are reported, not hidden
- [ ] No borrowed work described as ours

---

## 4. Timeline at a glance

| Week | Phase | Main focus | Gate |
|---|---|---|---|
| 1 to 2 | 0 | Read, set up, mentor, novelty check | Gate 0 |
| 3 to 5 | 1 | Baseline and unfairness | **Gate 1** |
| 6 to 7 | 2 | Brain split, F1, F2 | |
| 8 to 9 | 2 | Shapley, karma | Gate 2 |
| 10 to 11 | 3 | Full runs, attacks, leakage | Gate 3, feature freeze |
| 12 | 4 | Stretch or buffer | |
| 13 to 14 | 5 | Analysis, report, demo | Gate 5 |

Writing starts in **Week 6**, not Week 13: each part of the report is drafted when the part is built.

---

## 5. Decisions and when they must be made

| Decision | Latest by | Blocks |
|---|---|---|
| Scope approval, helicopter core or stretch | End of Week 2 | Phase plan |
| GPU source | End of Week 2 | Number of runs |
| Use BlueSky-Gym or own wrapper | End of Week 2 | Phase 1 |
| Copy Sharifi design exactly | Week 3 | Baseline comparability |
| Which summarizer parts are shared | Week 6 | Federation code |
| Bidding rule, giveback rule | Week 8 | Karma code |
| Shapley utility definition | Week 8 | Scoring |
| Success criteria (from [`09_EXPERIMENT_PLAN.md`](../onboarding/09_EXPERIMENT_PLAN.md)) | **Before** Week 10 runs | Honest evaluation |

---

## 6. What to watch every week

| Signal | Meaning | Action |
|---|---|---|
| A training run takes much longer than expected | Compute plan at risk | Cut seeds or episodes, prioritize per Section 3 |
| Performance drops after each federation round | Shared part confuses private part | Try more frequent rounds or gradual blending |
| Shapley scores jump around | Unstable credits | Check smoothing, exam size |
| Shield intervenes very often | Too conservative | Log it, tune look-ahead within safety limits |
| Someone blocked for more than 3 days | Integration problem | Raise in Monday sync |
| Two weeks behind | Plan too big | Apply the fallback for the current phase |

---

## 7. Fallback ladder

If the project is behind, cut in this order (last item cut first):

1. Ablations, learned bidding, DP sweep
2. X+Y+Y, rival-slowdown attack
3. Helicopter + shield (if stretch)
4. F3, K1, B2
5. Exam-gaming attack
6. Route-leakage test (reduce to a simple version, do not drop entirely)

**Never cut:** B1, solo runs, normalized delay, F1, F2, K2, safety metrics, 3 seeds, statistics. Without these there is no result.

---

## 8. Definition of done

The project is done when we can show:
1. The unfairness exists in our baseline.
2. What federation does to it (better, worse or no change), with statistics.
3. What earned priority adds, and that safety did not get worse.
4. Whether cheating pays, and whether routes leak.
5. A clear, honest statement of what is borrowed and what is ours.
