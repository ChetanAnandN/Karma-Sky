# KarmaSky: Full Project Brief for the Team

**Project:** SDG 9 main semester project
**Status as of 2026-10-15:** Design stage. Nothing has been built yet. Mentor approval of the refined scope is still pending.
**All work is simulation-only. No physical drones are involved at any stage.**

---

## How to read this document

Every claim and decision in this file carries one of these tags, so any reader (human or AI) knows how settled it is:

| Tag | Meaning |
|---|---|
| **[FROM PAPER]** | A fact taken from a paper we have read. Source is named. |
| **[PROPOSED]** | Our design choice, agreed in discussion, but not yet approved by the mentor or tested. |
| **[OPEN]** | Not decided. Needs a team or mentor decision. |
| **[FOR REVIEW]** | Still under discussion. Do not treat as confirmed. Section 14 is entirely in this state. |

Numbers marked "start at" are initial guesses to be tuned, not results.

---

## Table of contents

1. Where the idea came from
2. The problem in plain words
3. Title, problem statement, objective
4. What already exists (papers we read)
5. The research gap
6. What we are building: the KarmaSky system
7. Methodology, phase by phase
8. Experiments
9. Metrics and statistics
10. Novelty: what is and is not new
11. Impact
12. Assumptions and limitations
13. Plan: timeline, team split, compute, risks
14. FOR REVIEW: building blocks borrowed from prior work
15. Open decisions and immediate to-dos
16. Glossary
17. References

---

## 1. Where the idea came from

1. We first searched broadly for SDG 9 project ideas and ranked about 20 candidates (industrial energy monitoring, PLC security, firmware analysis, flood and e-bus resilience, log parsing, and others) on novelty, complexity, feasibility, data access, skill fit and SDG fit.
2. Our mentor then gave a direct idea: **"Develop a federated multi-agent reinforcement learning framework for UAV and manned aerial vehicle delivery networks."** That idea became the project.
3. The generic version of the mentor's idea already exists (federated MARL for drone collision avoidance, see Section 4), so we narrowed it.
4. We chose **fairness between competing drone operators** as the core problem, because a 2026 paper measured this unfairness and did not fix it.
5. To add novelty, we added **contribution-based airspace priority**: operators who help the shared learning more earn more right of way.
6. To stop big operators from dominating, we added **karma credits** (earned, spent, and redistributed), adapted from a road-traffic fairness scheme.
7. Manned aircraft (from the mentor's original wording) are kept as a **safety shield and helicopter module**. **[OPEN]** whether this is core or stretch.

---

## 2. The problem in plain words

Picture a future city where several delivery companies (say an Amazon-like company and a Swiggy-like company) fly drones in the same sky, and an air ambulance helicopter sometimes flies through.

- Each company trains its own drone control AI and keeps it secret.
- A 2026 study showed this ends up **safe but unfair**: the company with weaker drones gets delayed more. **[FROM PAPER: Sharifi et al. 2026]**
- If companies could learn together without revealing secrets, maybe the sky becomes fairer. But then new problems appear:
  - some companies may take the benefit without contributing (free riding)
  - rewarding contribution may let big companies grab permanent priority
  - companies may cheat to earn priority
- Real airspace also has manned aircraft, and drones must always give way to them. **[FROM PAPER: 14 CFR 107.37]**

Our project builds and tests a system that tries to solve all of this together, in simulation.

---

## 3. Title, problem statement, objective

**Title [PROPOSED]:** KarmaSky: Contribution-Earned Airspace Priority for Fair Federated Multi-Agent Drone Delivery

Alternative titles considered:
- Learn Together, Fly Fair: Credit-Based Federated MARL for Multi-Operator Drone Delivery
- Earning the Right of Way: Fair and Incentive-Compatible Federated Learning for Shared Urban Airspace

**Problem statement [PROPOSED]:**
Future urban airspace will be shared by competing drone delivery operators with unequal fleets. Recent multi-agent RL work shows that when operators train their deconfliction policies independently, the result is safe but unfair: the operator with weaker drones took 22.4% longer to complete its missions, and fairness fell to 80.8% (Sharifi et al. 2026). Federated learning could let operators learn collectively without sharing raw data, but it introduces three new problems: operators may free ride on others' contributions, contribution-based rewards can let larger operators dominate, and selfish operators may game the system. No existing framework addresses fairness, incentives, and integrity of collaborative learning together in shared airspace.

**One-line research question:** How can competing drone operators learn together so that contributing to everyone's safety earns fair, non-monopolizable airspace priority, without leaking private data, rewarding cheating, or compromising safety around manned aircraft?

**Main objective [PROPOSED]:**
To design and evaluate a fairness-aware federated multi-agent reinforcement learning framework in which independent drone delivery operators with unequal fleets collaboratively learn tactical deconfliction policies while keeping raw operational data and their private decision policies confidential, and to determine whether federation, combined with explicit fairness mechanisms, reduces the hardware-normalized delay gap between strong and weak operators compared with independent training, without reducing safety.

**Research questions and hypotheses [PROPOSED]:**

| RQ | Question | Hypothesis |
|---|---|---|
| RQ1 | Does partial federation (sharing only a traffic encoder) reduce the normalized delay gap vs independent training? | Partly. Policy-driven unfairness shrinks; hardware-driven unfairness remains. |
| RQ2 | Do fairness-targeted aggregation rules reduce it further? | Yes, with no significant safety loss. |
| RQ3 | Does contribution-based priority encourage sharing, and does it hurt small operators? | It increases contribution but widens the gap, unless credits are redistributed and capped (karma). |
| RQ4 | Does safety-based contribution scoring favor the weak fleet (it sees harder conflicts)? | Possibly. Untested. |
| RQ5 | Can a cheating operator inflate its priority, and do the defenses stop it? | Yes it can without defenses; defenses limit the gain. |
| RQ6 (stretch) | Do fairness gains hold with a non-yielding manned helicopter under a safety shield? | Unknown. |

A null result on RQ1 (federation does not help) is still a valid finding: it would show fairness must be engineered explicitly.

**SDG 9 link:** fair access to shared low-altitude airspace, treated as emerging public infrastructure (target 9.1: resilient, equitable infrastructure).

---

## 4. What already exists (papers we read)

All five core papers below were read in full by the team's AI assistant (the Rezaee PDF's text was partly garbled; its figures and readable pages were used).

### 4.1 Sharifi et al. 2026 (arXiv 2605.01041, preprint): our closest prior work [FROM PAPER]

- **Setup:** 2 companies, 10 drones each (20 total), package delivery over Frisco, Dallas, Texas, simulated in **BlueSky**.
- **Routes:** 4 fixed routes, about 10.33 km each. Merge points WP3 and WP7, intersection WP9.
- **Method:** PPOA2C (PPO combined with advantage actor-critic) with an attention module over nearby intruders. Each fleet trains its own policy **separately** to keep it private. Drones within one fleet share one policy.
- **Actions:** decelerate, hold, accelerate (speed only).
- **Reward:** 5 terms: loss-of-separation penalty, speed-limit penalty, action-change penalty, mission-completion bonus, per-step time penalty.
- **Thresholds:** NMAC (near mid-air collision) under 100 m; LoWC (loss of well clear) under 500 m.
- **Timing:** decision step 3 s, mission horizon 18 min.
- **Fleet configurations:**

| Config | Speed range | Acceleration | Sensing range | Based on |
|---|---|---|---|---|
| X (strong) | 0 to 44.88 m/s | ±1.71 m/s² | 1000 m | Google Wing Hummingbird |
| Y (weak) | 0 to 30.12 m/s | ±1.02 m/s² | 750 m | Amazon MK30 |

- **Training:** 2,500 episodes per run, more than 7 hours per run on an RTX 3090, 5 seeds, 300 evaluation episodes. Learning rate 1e-4, entropy coefficient 1e-3, clip 0.2.
- **Key results (Table I):**

| Pairing | Success (out of 20) | Fairness Ft |
|---|---|---|
| PPOA2C(X) + PPOA2C(Y) | 19.55 | 80.8% |
| PPOA2C(X) + PPOA2C(X) | 19.79 | 98.4% |
| PPOA2C(X) + Rule-based(Y) | 19.98 | 86.5% |
| PPOA2C(X) + Rule-based(X) | 19.90 | 91.9% |
| Rule-based(X) + Rule-based(Y) | 18.53 | 82.4% |

- With different configs, Company B's mission time was **22.4% longer** than Company A's.
- Fairness metric: Ft = (1 − |T_A − T_B| / max(T_A, T_B)) × 100.
- **Their conclusion:** fairness-aware conflict management is needed. They propose none.
- **Missing:** federation, manned aircraft, safety guarantees, more than 2 fleets, code release.

### 4.2 Brittain and Wei 2022 (IEEE T-ASE 19(4), peer-reviewed): the foundation [FROM PAPER]

- MAASA framework, also in BlueSky. Decentralized MARL with PPO.
- Key idea: an **intent-learning model** that predicts each intruder's next action, so agents with different objectives can cooperate.
- 50 Airbus A320s per episode, 150k training episodes, 5 different reward functions to create heterogeneous agents.
- With 5 agent types: **4 loss-of-separation events vs 28** for the baseline (86% fewer). With 3 types: 0 vs 32.
- Intent prediction accuracy about 90% (89% in the hardest case).
- Used 75 parallel workers (Ray); about 10 hours for 100k episodes.
- **Limits for us:** airliners en route, not drones; no federation; no fairness analysis. Code was "to be made available."

### 4.3 Chen et al. 2023 (GLOBECOM Workshops; arXiv 2306.02029): federation works for UAVs [FROM PAPER]

- FedQMIX: each UAV trains a local QMIX model; models are averaged every **50 episodes**.
- 3 UAVs on a data-harvesting task (not delivery).
- Federation converged faster than non-federated training; model-aided training needed about 3 orders of magnitude less real-world data.
- **Public code:** github.com/Cirrick/Multi_UAV_Data_Harvesting (we have the zip).
- **Limits for us:** federation is among copies of one team, not competing companies. UAVs avoid collisions by flying at fixed different altitudes, so there is no learned collision avoidance.

### 4.4 Rezaee et al. 2024 (JAC-ECC 2024, IEEE regional conference): shallow prior attempt [FROM PAPER]

- Federated MADDPG, 96 drones in 1 km², 2D, speeds 5 to 15 m/s, global model update every 50 episodes.
- Average collisions moved only from about 0.312 to 0.305 per their plot: a marginal improvement.
- They list heterogeneity and security as open problems.
- **Use:** cite as "work done (shallow)", not as proof of feasibility.

### 4.5 Samu, Yang and Poddar 2026 (Drones 10(8):596, MDPI, peer-reviewed): the gap source [FROM PAPER]

- Systematic review of 44 studies on drone search and rescue (2022 to 2026).
- Only **6 of 44** handle crewed aircraft at all; 4 of those come from adjacent domains.
- **None** provides formally assured separation from crewed aircraft. The review names control barrier functions, reachability analysis and runtime shielding as what is missing.
- About **86%** of studies were validated in simulation only.
- **Caution:** the review deliberately excluded delivery and generic drone traffic studies. Applying its gap to delivery is our extrapolation.

### 4.6 Supporting papers (read at abstract level only)

| Paper | What it gives us |
|---|---|
| CARMA, Elokda et al., Transportation Science 2025 | Non-tradable karma credits, bid for a fast lane, redistributed daily; fair across income groups |
| Multi-karma economies, Elokda et al., arXiv 2412.17002 | Uniform redistribution reached maximum welfare in their case study |
| Market Design for Drone Traffic Management, AAAI 2022 (arXiv 2110.13784) | No agreed definition of airspace fairness; first-come-first-serve and auctions each disadvantage someone |
| FairFly (arXiv 2008.09297) | Fair motion planning between UAV operators (non-learning) |
| Airbus UTM and MIT Fairness Engine (industry, 2023) | Measures an operator's cost as delay beyond solo operation |
| Huang et al., IEEE Commun. Mag. 2024; arXiv 2305.16272 | Competing companies in federated learning may free ride or manipulate updates |
| Geimer et al., IJCNN 2025 | Shapley-based contribution scores are unstable across rounds |
| FRIDA (arXiv 2410.05020) | Honest operators with unusual data can look like free riders |
| RGIA (arXiv 2512.00303); Li et al. 2023 (arXiv 2306.09273) | Shared gradients in federated RL can leak training data |
| ElSayed-Aly et al., AAMAS 2021 | Safe MARL via shielding |
| Li et al., ICLR 2020 (q-FFL) | Fairness-weighted federated aggregation (citation still to verify) |

---

## 5. The research gap

1. No work applies **federated learning between competing drone operators**. Existing federated UAV work federates within one team.
2. The unfairness Sharifi et al. measured has **no proposed fix**.
3. Existing fairness measurement compares raw mission times, which **confuses unfair treatment with slower hardware**.
4. Airspace fairness mechanisms exist (auctions, fairness engines), but **none is learning-based or tied to collaborative learning**.
5. Karma credits have been used for roads and bandwidth, **not airspace**, and never earned through learning contribution.
6. Drone studies rarely include manned aircraft, and **none guarantees separation** from them (Drones 2026 review).

Points 1, 4 and 5 are based on our searches. **[OPEN]** They must be re-checked against arXiv 2511.11616 and arXiv 2605.20625 (not yet read) before we claim them.

---

## 6. What we are building: the KarmaSky system [PROPOSED]

A simulated delivery network where competing drone companies share the sky with a manned helicopter. The system loop:

1. **Train locally.** Each operator trains its drones in BlueSky for N episodes.
2. **Share the encoder only.** Operators upload updates to a shared traffic encoder. Private policy heads never leave.
3. **Score contribution.** A neutral aggregator measures how much each update reduces near-misses on a secret hard-scenario suite (Shapley value).
4. **Aggregate.** Updates are combined and the new encoder is sent back.
5. **Mint credits.** Contribution scores convert into non-tradable karma credits.
6. **Fly and bid.** At conflicts between operators, drones spend credits for right of way. Spent credits are pooled and redistributed each period.
7. **Guard.** A safety shield overrides unsafe actions, manned aircraft always have priority, and an integrity check flags operators gaming their scores.

**Fixed priority order (top wins):**
1. Manned aircraft (drones always yield)
2. Safety shield (blocks any unsafe action)
3. Karma credits (decide who yields among safe options only)
4. Learned policy (chooses freely within what remains)

---

## 7. Methodology, phase by phase [PROPOSED]

### Phase 1: Environment
Reproduce Sharifi et al. in BlueSky first, so our baseline can be checked against published numbers.

| Element | Setting |
|---|---|
| Simulator | BlueSky, wrapped as a multi-agent RL environment |
| Airspace | Frisco, Dallas, 4 routes of about 10.33 km, 2 merges, 1 intersection |
| Operators | 2 to start (10 drones each); 3 if compute allows |
| Fleets | X (strong) and Y (weak), as in Section 4.1 |
| Timing | 3 s steps, 18 min horizon |
| Thresholds | NMAC under 100 m, LoWC under 500 m |
| Manned aircraft | One scripted helicopter crossing the corridors, never yields |

Every operator is also run **alone** in the same scenario. Those solo times feed the normalized-delay fairness metric.

### Phase 2: Agent model
- PPO actor-critic with attention over intruders (Sharifi et al. design).
- **Observation:** own state (distance to waypoint, speed, heading, acceleration) plus variable-length intruder states. We add per intruder: operator ID, current credit bid, manned-aircraft flag.
- **Actions:** decelerate, hold, accelerate. **[OPEN]** Add a hold-pattern action if speed changes cannot clear a crossing helicopter.
- **Reward:** Sharifi's 5 terms. **Credits never enter the reward**, so drones cannot learn to farm them.
- **Split network:**

| Part | Contents | Shared? |
|---|---|---|
| Shared encoder | Embedding layers, attention module, intent-prediction head (Brittain and Wei style) | Yes, federated |
| Private policy head | Layers after attention; actor and critic outputs | Never |

- All drones of one operator share weights.

### Phase 3: Federation protocol
- Every N episodes (start at 50, as Chen et al.), each operator sends only its encoder weight change Δ.
- No trajectories, rewards or policy-head weights leave an operator.
- Three aggregation rules to compare:

| Rule | Weighting | Question |
|---|---|---|
| F1 | Equal (FedAvg) | Does collaboration alone help fairness? |
| F2 | More weight to the operator with larger normalized delay (q-FFL spirit) | Does steering toward the worse-off operator help more? |
| F3 | Proportional to safety contribution score | Does rewarding useful updates improve the shared model? |

- Karma (Phase 5) is tested on top of the best of F1 to F3.

### Phase 4: Safety-based contribution scoring
- **Hard-conflict suite:** fixed scenarios held by the aggregator, never shown to operators: dense merges, simultaneous intersection arrivals, mixed fleets, helicopter crossings. A second suite is partly redrawn each period (for Phase 7).
- **Utility of a group S of operators:** build an encoder from only S's updates, run the suite:
  - v(S) = U(∅) − U(S), where U(S) = NMAC count + w × LoWC count (start w = 0.1)
- **Shapley value** of operator k: the average marginal gain v(S ∪ {k}) − v(S) over all groups S. With 2 to 3 operators that is only 4 to 8 evaluations per round, so it is computed exactly.
- **Smoothing:** s_k ← 0.8 × s_k + 0.2 × φ_k (because Shapley scores are unstable round to round, IJCNN 2025).
- **Hypothesis:** the weak fleet meets harder conflicts, so its updates may score higher.

### Phase 5: Karma credit economy (adapted from CARMA)
1. **Minting:** each round, M new credits split by smoothed contribution: operator k gets M × s_k / Σs. Not tradable, not buyable.
2. **Conflict detection:** two drones from different operators predicted within 500 m at a merge or intersection within 60 s (to tune).
3. **Bidding:** Version A: fixed rule (bid more when running late). Version B (stretch): the private head learns the bid.
4. **Resolution:** higher bidder keeps its plan; lower bidder yields (its accelerate action is masked until clear). Ties go to the drone closer to the conflict point. Winner pays its bid.
5. **Redistribution:** paid credits are pooled and returned each period. Compare:
   - Uniform: equal share to all
   - Need-based: more to the operator with higher normalized delay
6. **Cap:** no operator may hold more than a fixed share of all credits (start at 60%).

### Phase 6: Safety shield and manned aircraft
- **Shield:** over a 30 s look-ahead (to tune), predict each drone's position under each action, assuming every intruder may move at maximum speed in the worst direction. Remove actions that breach separation (500 m from the helicopter, 100 m from drones). If none remain, use the fallback: decelerate.
- **Helicopter:** scripted, fixed path across the corridors, never changes course, flagged in observations. Start with one crossing per episode.
- **Guarantee holds only if:** positions are known, no aircraft exceeds the assumed maximum speed, and the fallback is always physically possible. These assumptions are stated openly.

### Phase 7: Integrity (attack and defense)

| Attack | What the cheater does | Goal |
|---|---|---|
| A1 Free riding | Sends near-zero or recycled updates | Get the shared encoder for free |
| A2 Suite overfitting | Tunes its update to score well on test-like scenarios | Inflate credits |
| A3 Rival slowdown (stretch) | Crafts updates that make rivals more cautious | Win conflicts without bidding |

**Defenses:**
1. Hidden, rotating suite: a score that collapses on the new draw is flagged.
2. Consistency check: updates far from the others (low cosine similarity) or sudden score jumps are held back one round.
3. Smoothing and cap limit what one round of cheating can buy.
4. Shadow evaluation on the full training scenario.

**Stretch: route leakage.** Test whether a rival can reconstruct another operator's hubs and routes from its encoder updates (gradient inversion), and whether encoder-only sharing or added noise prevents it.

---

## 8. Experiments [PROPOSED]

**Methods:**

| ID | Method | Shares | Role |
|---|---|---|---|
| B1 | Independent training (Sharifi et al.) | Nothing | Main baseline |
| B2 | One centralized policy | Everything | Upper bound (not private) |
| B3 | Rule-based deconfliction | Nothing | Non-learning reference |
| F1, F2, F3 | Federated encoder, three aggregation rules | Encoder updates | Does federation help? Which rule? |
| K1 | Best F + contribution-ranked priority, no redistribution | Encoder updates | Shows the "rich get richer" risk |
| K2 | Best F + full karma | Encoder updates | Full KarmaSky |
| K2 + attacks | K2 under A1/A2, with and without defenses | Encoder updates | Integrity |

**Ablations on K2:** uniform vs need-based redistribution; no cap; reward-based vs safety-based scoring; no smoothing; no intent head.

**Scenarios:** X+Y (main), X+X (control), X+Y+Y (3 operators, if compute allows); each with and without the helicopter.

**Seeds:** 3 per configuration (Sharifi used 5).

**Compute estimate:** core set (B1, B2, F1 to F3, K1, K2) × (X+Y, X+X) × 3 seeds = **42 runs**. At Sharifi's more-than-7-hours per run, about **300 GPU-hours** on an RTX 3090. Reduce by shortening training once convergence is known, parallel environments, and fewer seeds for X+X and ablations.

---

## 9. Metrics and statistics [PROPOSED]

| Group | Metric | Definition |
|---|---|---|
| Safety | Mission success rate | Missions with no NMAC, out of 20 |
| Safety | NMACs | Pairs under 100 m, split within-operator and between-operator |
| Safety | Helicopter separation violations | Drone inside 500 m of helicopter (target 0 with shield) |
| Efficiency | Mission time | Mean per operator, minutes |
| Fairness | Ft (Sharifi) | (1 − \|T_A − T_B\| / max(T_A, T_B)) × 100 |
| Fairness | Normalized delay D_k | (T_shared − T_solo) / T_solo per operator |
| Fairness | Delay gap, worst-off delay | \|D_A − D_B\| and max(D_A, D_B) |
| Incentive | Contribution and credit share | Share of φ and credits over time; Gini of credits |
| Integrity | Attack gain, detection delay | Extra credits a cheater wins; rounds until flagged |
| Cost | Compute and communication | GPU-hours per run; bytes per federation round |

**Why normalized delay:** Ft compares raw times, so slower drones look unfairly treated even when they are just slower. D_k measures delay beyond what each operator gets flying alone (same idea as the Airbus UTM Fairness Engine).

**Evaluation:** 300 episodes per run with learning frozen.

**Statistics:** mean and standard deviation across seeds; Mann–Whitney U test vs B1 on per-episode values; Holm correction for multiple comparisons; effect sizes reported. With 3 seeds, claims rest on consistent direction across seeds, not p-values alone.

**Success criterion:** a method counts as better only if it improves fairness **without a significant safety loss**.

---

## 10. Novelty: what is and is not new

**Honest summary:** every tool we use already exists. Our novelty is in the setting and the questions, not the tools. This is normal for research.

| Level | Status | Strength |
|---|---|---|
| Tools (MARL, federated learning, karma, Shapley, shields) | Not new. Do not claim. | None |
| Setting: federation between **competing** drone operators | Not found in our searches | Moderate, to verify |
| Questions: does federation fix unfairness? does contribution priority entrench big operators? does safety scoring favor small ones? | Not asked in shared airspace | Strongest part |
| Normalized-delay fairness metric | Adapted from an industry idea, new in this research setting | Small but reusable |
| Karma earned through learning contribution, applied to airspace | Not found in our searches | Moderate, to verify |

**Pitch line [PROPOSED]:** "The first study of whether collaborative learning and contribution-based priority can make shared airspace fair between competing drone operators."

**What could reduce novelty:** arXiv 2511.11616 (hierarchical federated graph attention for UAV collision avoidance) and arXiv 2605.20625 (Time-To-Reach separation and safety filtering for safe, fair multi-agent coordination). Both are unread.

---

## 11. Impact

- **Academic:** an open-source BlueSky environment with multiple operators, a helicopter, and fairness metrics, so others can benchmark against it.
- **Policy and SDG 9:** drone traffic management rules are still being designed. "Who gets priority, and is it fair to small operators?" is unresolved. Our results inform that debate.
- **Limited by:** simulation only, 2 to 3 operators. It informs design choices; it does not prove real-world readiness.

**Realistic positioning:** strong for a course project. As a research paper, a solid workshop or mid-tier conference contribution if results are clean.

---

## 12. Assumptions and limitations

- **Simulation only.** BlueSky models aircraft kinematics, not wind, battery drain or radio loss. This is the norm in this field (all five core papers are simulation-only), and we state it openly.
- **Trusted aggregator.** We assume a neutral aggregator (for example a UTM service provider) that scores honestly.
- **Shared positions.** Drones broadcast positions (FAA Remote ID). The shield depends on this.
- **Encoder sharing can still leak.** It reduces but does not prove privacy.
- **Small scale.** Exact Shapley stops being practical beyond about 10 operators.
- **Conditional safety guarantee.** See Phase 6.
- **Novelty not yet fully verified.** See Section 10.

---

## 13. Plan

### Timeline (14 weeks) [PROPOSED]

| Weeks | Milestone |
|---|---|
| 1 to 2 | Read the 2 unread preprints; BlueSky setup; confirm GPU access |
| 3 to 5 | Reproduce Sharifi baseline (B1, B3); confirm the unfairness result; solo runs |
| 6 to 7 | Split network; F1; normalized-delay metric |
| 8 to 9 | F2, F3; Shapley scoring; karma (K1, K2) |
| 10 to 11 | Full runs and seeds; attacks and defenses |
| 12 | Stretch: helicopter and shield (if not core); route leakage |
| 13 | Analysis, plots, statistics |
| 14 | Report, presentation, demo video |

**Fallback:** if weeks 3 to 5 slip, keep 2 operators and F1, F2, K2 only. That still answers RQ1 to RQ3.

### Team split (4 members) [PROPOSED]

| Member | Responsibility |
|---|---|
| 1 | BlueSky environment, scenario, RL wrapper, solo runs, helicopter |
| 2 | MARL agents (PPO + attention + intent head), baseline reproduction |
| 3 | Federation, aggregation rules, Shapley scoring, karma economy |
| 4 | Evaluation pipeline, metrics, statistics, plots; shield; attacks and defenses |

### Risks

| Risk | Mitigation |
|---|---|
| MARL training unstable or slow | Start from Sharifi's hyperparameters; get the baseline converging before adding anything |
| BlueSky has no ready RL interface | Budget weeks 1 to 3; Brittain and Wei describe a Ray-based extension |
| Federation does not reduce the gap | Report it as a finding; karma then becomes the main contribution |
| Novelty overlap discovered | Read the 2 preprints in weeks 1 to 2 |
| Compute shortfall | Fewer seeds and episodes; prioritize X+Y |
| Too many pieces, half-finished | Integrity attacks and route leakage stay stretch goals |

---

## 14. FOR REVIEW: building blocks borrowed from prior work

> **⚠ STATUS: FOR REVIEW. STILL IN DISCUSSION. NOT CONFIRMED.**
> These five pieces are **existing work by other researchers** that we plan to reuse. They are **not our contributions** and must never be described as new. Whether and how each one is used is still under discussion within the team and with the mentor. Any reader (human or AI) should treat this section as a working list, not a final decision.

| # | Building block | Who did it | How we plan to use it | Review status |
|---|---|---|---|---|
| 1 | MARL for multi-company drone separation | Sharifi et al. 2026; Brittain and Wei 2022 | Base agent design (PPOA2C with attention), scenario, reward, baseline B1; intent-prediction head in the shared encoder | FOR REVIEW |
| 2 | Federated RL for drones | Chen et al. 2023; Rezaee et al. 2024 | Federation round structure (average every 50 episodes); Chen's code as a reference implementation | FOR REVIEW |
| 3 | Karma credits for fair access | CARMA, Elokda et al. 2025 (road traffic) | Credit minting, bidding, redistribution, adapted from road lanes to airspace | FOR REVIEW |
| 4 | Shapley contribution scoring | Federated learning literature | Measuring each operator's contribution, with safety-based utility instead of accuracy | FOR REVIEW |
| 5 | Safety shields | ElSayed-Aly et al., AAMAS 2021 | Runtime shield overriding unsafe drone actions near the helicopter | FOR REVIEW |

**Points to discuss for each block:**
1. MARL base: copy Sharifi's design exactly for comparability, or change the action space for the helicopter case?
2. Federated RL: is averaging every 50 episodes right for our setup, or should N be tuned? Is Chen's code reusable (it uses QMIX, we use PPO)?
3. Karma: uniform or need-based redistribution? Fixed-rule or learned bidding? What cap value?
4. Shapley: is safety-based utility (near-miss reduction) the right measure, or should efficiency count too? Exact computation only works with few operators.
5. Shield: is it core or stretch? Can our assumptions (known positions, max speed) be justified?

**Rule for writing:** in the report, these appear under "Background" or "Building blocks," always with citations. Our contributions are only the items in Section 10 marked as new.

---

## 15. Open decisions and immediate to-dos

| # | Item | Owner | Status |
|---|---|---|---|
| 1 | Mentor approval of the refined scope (fairness + karma) vs the original wording | Team lead | [OPEN] |
| 2 | Is the manned helicopter + shield core or stretch? | Mentor | [OPEN] |
| 3 | Did the mentor's "manned aerial vehicle delivery networks" mean manned aircraft that also deliver (mixed fleet), or other airspace users drones must avoid? | Mentor | [OPEN] |
| 4 | Is a mechanism-design angle (karma, incentives) acceptable, or should the focus stay on the RL framework? | Mentor | [OPEN] |
| 5 | Read arXiv 2511.11616 and 2605.20625 for overlap | All | To do, weeks 1 to 2 |
| 6 | Confirm GPU access (about 300 GPU-hours needed for the core set) | All | [OPEN] |
| 7 | Verify the q-FFL citation (Li et al., ICLR 2020) | Member 3 | To do |
| 8 | Check whether 2 to 3 operators is enough for the course evaluators | Team lead | [OPEN] |
| 9 | Finalize review of the 5 borrowed building blocks (Section 14) | All | [FOR REVIEW] |

---

## 16. Glossary

| Term | Meaning |
|---|---|
| MARL | Multi-agent reinforcement learning: many agents learning by trial and error at once |
| Federated learning | Training together by sharing model updates, not raw data |
| Operator | A drone delivery company |
| Deconfliction | Keeping aircraft safely apart |
| NMAC | Near mid-air collision; here, closer than 100 m |
| LoWC | Loss of well clear; here, closer than 500 m |
| Encoder | The part of the network that turns raw observations into general understanding |
| Policy head | The part that turns understanding into decisions |
| Shapley value | A fair way to split credit among contributors, from game theory |
| Karma credits | Non-tradable tokens earned and spent for priority, then redistributed |
| Shield | A safety layer that blocks unsafe actions before they execute |
| BlueSky | Open-source air traffic simulator used by our core papers |
| Ft | Sharifi's fairness metric based on mission time |
| Normalized delay | Delay beyond what an operator gets flying alone |
| UTM | Unmanned aircraft traffic management |

---

## 17. References

1. I. Sharifi, H. T. Kim, M. H. Ahmed, M. Ghasemi, P. Wei. Separation Assurance between Heterogeneous Fleets of Small Unmanned Aerial Systems via Multi-Agent Reinforcement Learning. arXiv:2605.01041, 2026 (preprint).
2. M. Brittain, P. Wei. Scalable Autonomous Separation Assurance With Heterogeneous Multi-Agent Reinforcement Learning. IEEE Transactions on Automation Science and Engineering, 19(4):2837 to 2848, 2022. doi:10.1109/TASE.2022.3151607
3. J. Chen, O. Esrafilian, H. Bayerlein, D. Gesbert, M. Caccamo. Model-aided Federated Reinforcement Learning for Multi-UAV Trajectory Planning in IoT Networks. IEEE GLOBECOM Workshops, 2023. arXiv:2306.02029. Code: https://github.com/Cirrick/Multi_UAV_Data_Harvesting
4. M. R. Rezaee et al. Federated Multi-Agent Reinforcement Learning for UAV Collision Avoidance in Dense Smart City Environment. JAC-ECC 2024. doi:10.1109/JAC-ECC64419.2024.11061244
5. J. Samu, C. Yang, K. R. Poddar. Optimization and Tactical Deconfliction for Drone Search-and-Rescue in Low-Altitude Airspace: A Systematic Literature Review. Drones, 10(8):596, 2026. doi:10.3390/drones10080596
6. E. Elokda et al. CARMA: Fair and Efficient Bottleneck Congestion Management via Nontradable Karma Credits. Transportation Science, 2025. arXiv:2208.07113
7. E. Elokda et al. To Travel Quickly or to Park Conveniently: Coupled Resource Allocations with Multi-Karma Economies. arXiv:2412.17002
8. Market Design for Drone Traffic Management. AAAI 2022. arXiv:2110.13784
9. FairFly: A Fair Motion Planner for Fleets of Autonomous UAVs in Urban Airspace. arXiv:2008.09297
10. Airbus UTM and MIT, Fairness Engine concept (industry, reported 2023)
11. C. Huang et al. Promoting Collaboration in Cross-Silo Federated Learning: Challenges and Opportunities. IEEE Communications Magazine, 2024.
12. Incentivizing Honesty among Competitors in Collaborative Learning and Optimization. arXiv:2305.16272
13. A. Geimer, B. Fiz, R. State. On the Volatility of Shapley-Based Contribution Metrics in Federated Learning. IJCNN 2025.
14. FRIDA: Free-Rider Detection using Privacy Attacks. arXiv:2410.05020
15. Gradient Inversion in Federated Reinforcement Learning (RGIA). arXiv:2512.00303
16. M. Li, W. Ding, D. Zhao. Your Room is not Private: Gradient Inversion Attack on Reinforcement Learning. arXiv:2306.09273
17. M. ElSayed-Aly et al. Safe Multi-Agent Reinforcement Learning via Shielding. AAMAS 2021, pp. 483 to 491.
18. T. Li, M. Sanjabi, A. Beirami, V. Smith. Fair Resource Allocation in Federated Learning. ICLR 2020 (to verify).
19. J. M. Hoekstra, J. Ellerbroek. BlueSky ATC Simulator Project: An Open Data and Open Source Approach. ICRAT 2016.
20. 14 C.F.R. 107.37, Operation near aircraft; right-of-way rules.

**Unread, must check before claiming novelty:**
- arXiv:2511.11616: hierarchical federated graph attention networks for UAV collision avoidance
- arXiv:2605.20625: Time-To-Reach separation and safety filtering for safe, fair, and efficient multi-agent coordination
