# Experiment Plan

All **[PROPOSED]**. Numbers tagged [FROM PAPER] come from Sharifi et al. 2026.

---

## Research questions

| RQ | Question |
|---|---|
| RQ1 | Does federated learning between competing operators change the delay gap between a strong and a weak fleet, compared with each learning alone? |
| RQ2 | Which merging rule (equal, fairness-weighted, contribution-weighted) gives the best fairness without reducing safety? |
| RQ3 | Do contribution-earned karma credits reduce the gap further, and do giveback and cap prevent hoarding? |
| RQ4 | Can operators gain credits by cheating, and do the defenses stop it? |
| RQ5 | Can one operator infer another's routes from shared updates, and do the privacy fixes help? |
| RQ6 (stretch or core, [OPEN]) | Does the shield keep separation from a manned helicopter at acceptable cost to delay? |

## Setups

| ID | Setup | Answers |
|---|---|---|
| B1 | Independent learning, each company alone | Baseline |
| B2 | One centralized learner for all drones | Reference upper bound |
| B3 | Rule-based, no learning | Reference |
| F1 | Federated, equal average | RQ1, RQ2 |
| F2 | Federated, fairness-weighted | RQ2 |
| F3 | Federated, contribution-weighted | RQ2 |
| K1 | F + karma, no giveback, no cap | RQ3 |
| K2 | F + karma, with giveback and cap | RQ3 |
| K2 + A1 / A2 | K2 under free riding / exam gaming, with and without defenses | RQ4 |
| P0 / P1 | Route-leakage attack without / with privacy fixes | RQ5 |
| S1 | Best setup + helicopter + shield | RQ6 |

**Fleet mixes:** X+Y (main), X+X (control: should show no unfairness), X+Y+Y (optional, 3 companies).

**Ablations (if time):** no intent head; no attention; no smoothing of Shapley scores; uniform vs need-based giveback.

## Settings

| Setting | Value | Source |
|---|---|---|
| Fleets | 2 × 10 drones | [FROM PAPER] |
| Step | 3 s | [FROM PAPER] |
| Episode length | 18 min | [FROM PAPER] |
| Training episodes | 2,500 | [FROM PAPER] |
| Evaluation episodes | 300 | [FROM PAPER] |
| PPO | lr 1e-4, entropy 1e-3, clip 0.2, batch 512, 8 epochs, Adam, GAE | [FROM PAPER] |
| Federation interval | 50 episodes | [PROPOSED] |
| Seeds | 3 per setup | [PROPOSED] |
| Total runs | about 42 | [PROPOSED] estimate |
| Compute | about 300 GPU-hours | Rough estimate, Sharifi reports >7 h per run on RTX 3090 |

## Metrics

| Group | Metric |
|---|---|
| Safety | NMAC count, LoWC count (per company and total), shield intervention rate |
| Efficiency | Mean travel time per company |
| Fairness | Normalized delay per company (main), delay gap, worst-off company delay, Sharifi's Ft |
| Credits | Balance over time, share held by each company, Gini of balances |
| Integrity | Credits gained by attacker vs honest; detection rate; false alarms |
| Privacy | Route-guess accuracy of the attack |

## Statistics

- Compare setups with Mann-Whitney U over evaluation episodes and seeds.
- Holm correction for multiple comparisons.
- Report effect sizes, not only p-values.
- Report every result, including ones where our method does not help.

## Success criteria (decided before running, so we do not move the goalposts)

- **Fairness:** delay gap in F or K setups is smaller than in B1, statistically significant.
- **Safety:** NMAC not significantly higher than B1.
- **Integrity:** attackers gain no more credits than honest operators when defenses are on.
- If these fail, we report why. A clear negative result is acceptable.

## Fallback plan

If compute or time is short, run in this priority: B1, B3, solo runs → F1 → F2 → K2 → K2+A1 → P0/P1 → F3, K1 → S1 → ablations, X+Y+Y.
