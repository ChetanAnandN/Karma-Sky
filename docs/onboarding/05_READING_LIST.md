# Reading List

Read in this order. You do not need to read every paper fully. The "what to look for" column tells you which parts matter.

---

## Core papers (everyone reads these)

| # | Role | Paper | Link | What to look for |
|---|---|---|---|---|
| 1 | Proof the idea is feasible | Brittain and Wei, Scalable Autonomous Separation Assurance With Heterogeneous Multi-Agent RL, IEEE T-ASE 19(4), 2022 | https://doi.org/10.1109/TASE.2022.3151607 | How MARL keeps drones apart; attention; intent prediction; network layers |
| 2 | What is already done | Sharifi, Kim, Ahmed, Ghasemi, Wei, Separation Assurance between Heterogeneous Fleets of sUAS via MARL, 2026 (preprint) | https://arxiv.org/abs/2605.01041 | Frisco scenario, fleet specs, training settings, the unfairness result, fairness score Ft. **Our baseline** |
| 3 | The gap | Chen et al., Model-aided Federated RL for Multi-UAV Trajectory Planning, GLOBECOM Workshops 2023 | https://arxiv.org/abs/2306.02029 | Federation round structure; note that all drones belong to one team, no competition |

## By role

### Member 1 (environment)
| Paper | Link | What to look for |
|---|---|---|
| Hoekstra and Ellerbroek, BlueSky ATC Simulator Project, ICRAT 2016 | Search title; code: https://github.com/TUDelft-CNS-ATM/bluesky | How BlueSky works |
| BlueSky-Gym | https://github.com/TUDelft-CNS-ATM/bluesky-gym | How it wraps BlueSky for RL |
| Sharifi 2026 (again) | above | Scenario section in full |

### Member 2 (AI brain)
| Paper | Link | What to look for |
|---|---|---|
| Brittain and Wei 2022 (again) | above | Network architecture in full |
| Schulman et al., Proximal Policy Optimization, 2017 | https://arxiv.org/abs/1707.06347 | PPO basics |
| Spinning Up PPO page | https://spinningup.openai.com/en/latest/algorithms/ppo.html | Plain explanation |

### Member 3 (federation and karma)
| Paper | Link | What to look for |
|---|---|---|
| McMahan et al., Communication-Efficient Learning of Deep Networks from Decentralized Data (FedAvg), 2017 | https://arxiv.org/abs/1602.05629 | The averaging rule F1 |
| Li, Sanjabi, Beirami, Smith, Fair Resource Allocation in Federated Learning (q-FFL), ICLR 2020 | https://arxiv.org/abs/1905.10497 | Idea behind F2. Verify citation |
| Elokda et al., CARMA: Nontradable Karma Credits | https://arxiv.org/abs/2208.07113 | Credit minting, bidding, redistribution |
| Elokda et al., Multi-Karma Economies | https://arxiv.org/abs/2412.17002 | Variations of karma |
| Geimer, Fiz, State, Volatility of Shapley-Based Contribution Metrics in FL, IJCNN 2025 | Search title | Why we smooth scores |
| Rezaee et al., Federated MARL for UAV Collision Avoidance, JAC-ECC 2024 | https://doi.org/10.1109/JAC-ECC64419.2024.11061244 | Another federated drone example (shallow) |

### Member 4 (evaluation, safety, attacks)
| Paper | Link | What to look for |
|---|---|---|
| ElSayed-Aly et al., Safe Multi-Agent RL via Shielding, AAMAS 2021 | https://arxiv.org/abs/2101.11196 | How a shield removes unsafe actions |
| FRIDA: Free-Rider Detection using Privacy Attacks | https://arxiv.org/abs/2410.05020 | Free-riding detection |
| Incentivizing Honesty among Competitors in Collaborative Learning | https://arxiv.org/abs/2305.16272 | Why competitors cheat |
| Li, Ding, Zhao, Gradient Inversion Attack on RL ("Your Room is not Private") | https://arxiv.org/abs/2306.09273 | How shared updates can leak private info |
| Gradient Inversion in Federated RL (RGIA) | https://arxiv.org/abs/2512.00303 | Same, for federated RL; basis of our route-leakage test |

### Background and context (anyone)
| Paper | Link |
|---|---|
| Samu, Yang, Poddar, Drone Search-and-Rescue Deconfliction review, Drones 10(8):596, 2026 | https://doi.org/10.3390/drones10080596 |
| Market Design for Drone Traffic Management, AAAI 2022 | https://arxiv.org/abs/2110.13784 |
| FairFly: A Fair Motion Planner for Fleets of Autonomous UAVs | https://arxiv.org/abs/2008.09297 |
| Huang et al., Promoting Collaboration in Cross-Silo FL, IEEE Comm. Magazine 2024 | Search title |
| 14 CFR 107.37 (drones must yield to manned aircraft) | https://www.ecfr.gov/current/title-14/chapter-I/subchapter-F/part-107/subpart-B/section-107.37 |

## Must read in Weeks 1 to 2 (novelty risk)

| Paper | Link | Why |
|---|---|---|
| Hierarchical federated graph attention networks for UAV collision avoidance | https://arxiv.org/abs/2511.11616 | May overlap with our federated part |
| Time-To-Reach separation and safety filtering for safe, fair, and efficient multi-agent coordination | https://arxiv.org/abs/2605.20625 | May overlap with our fairness part |

Write a half-page note for each: what they do, what overlaps, what does not.

**Note on links:** links to arXiv IDs and DOIs were taken from our earlier verified list. Links for PPO, FedAvg, q-FFL and the shield paper are standard arXiv IDs we did not re-check in this pass. Open each once and confirm the title matches.

---

## How to read a paper quickly (for teammates new to research)

1. Abstract and conclusion first.
2. Look at every figure and table.
3. Read the method section only for the parts in "what to look for".
4. Write 5 lines in the shared notes: problem, method, result, limitation, how it relates to KarmaSky.

## Prompt to summarize a paper with an AI tool

Paste the PDF and this prompt:

```
Summarize this paper for a student team building a federated multi-agent RL system
for fairness between competing drone delivery companies (simulated in BlueSky).
Give, in markdown:
1. Problem and setting (one paragraph)
2. Method: exact network layers, inputs, actions, reward, training settings
3. Scenario and simulation details (numbers with units)
4. Results: only numbers that appear in the paper, with table/figure numbers
5. Limitations stated by the authors
6. What this paper does NOT do that is relevant to: federation between competitors,
   fairness between operators, contribution-based priority, safety shields
Do not add any number or claim that is not in the paper. Quote section numbers.
```
