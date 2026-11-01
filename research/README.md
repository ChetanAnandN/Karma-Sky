# Research survey: index

This folder holds the literature survey for KarmaSky. Each subfolder of `Survey/` has a `SUMMARY.md` with one card per paper (citation, problem, method, setting, key results with table or figure numbers, stated limitations, relevance to KarmaSky), a synthesis, an overlap-risk section and a list of design choices we take, tagged [FROM PAPER].

**The PDFs are not in the Git repository** (the repository is public; the papers are copyrighted, and two carry an IEEE Xplore institutional licence stamp). Each card gives the arXiv link or DOI printed in the paper. Keep the PDFs on the shared drive. The Chen et al. code copy (`Survey/Core/Feasibility_&_workdone/Multi_UAV_Data_Harvesting-master/`) is also not committed; see https://github.com/Cirrick/Multi_UAV_Data_Harvesting (BSD 3-Clause).

Status tags follow the project docs: [FROM PAPER], [PROPOSED], [OPEN], [FOR REVIEW].

---

## Folders

### [`Survey/closest_work/`](Survey/closest_work/SUMMARY.md)
The papers nearest to our idea. Sharifi et al. 2026 (our baseline) show that two companies with different drones, each training its own PPO policy in BlueSky over Frisco, reach a safe equilibrium that delays the weaker company more (F_t 80.8%). Brittain and Wei (2019, 2020) supply the BlueSky MARL method; Chen et al. 2023 supply the federation loop (plain averaging every 50 episodes, one cooperative team). The two novelty-check preprints flagged in the plan were downloaded and read: HF-GAT (arXiv 2511.11616, federated graph attention for UAV collision avoidance with Byzantine-robust aggregation and DP) and the TTR paper (arXiv 2605.20625, CDC 2026, priority and fairness at a corridor merge with a priority-aware safety filter). Also Osipychev et al. (RL deconfliction with a real flight demo) and HRL4AG (KDD 2026, air-ground delivery dispatch).

### [`Survey/Core/`](Survey/Core/SUMMARY.md)
The three pillars from `05_READING_LIST.md`. Brittain and Wei 2022 (IEEE T-ASE) show decentralized PPO with attention and an intent-prediction head handles aircraft with different, unknown objectives, and already motivate this with competing companies; it is the source of our planned intent head (3 × FC128). Sharifi et al. v3 (main version) and Chen et al. (with their BSD-3 code) are carded in closest_work. Also Rezaee et al. 2024 (federated MADDPG for 96 drones, curves only) and Samu et al. 2026 (systematic review: 6 of 44 SAR drone studies handle crewed aircraft, none with provable separation).

### [`Survey/Federation_and_security/`](Survey/Federation_and_security/SUMMARY.md)
How federation behaves with heterogeneous and dishonest participants. Pang et al. (IJCNN 2025): keep observation-normalization statistics local under heterogeneous dynamics. Fang et al.: optimized local model poisoning breaks "Byzantine-robust" aggregators; validation-based rejection helps only sometimes. Mitra et al. 2026: rival aircraft operators federating prognostics models; a shared encoder with private heads works best for honest heterogeneity, but a backdoor in the shared part reaches every operator and is invisible on clean metrics; Krum (plus personalization) is the strongest defense they tested.

### [`Survey/General/`](Survey/General/SUMMARY.md)
Surveys for context: MARL for UAV control (Ekechi et al. 2025), AI for UAV deconfliction (Chagas et al. 2025), MARL for truck-drone logistics (Arishi and Ahuja 2025), and federated / cooperative / noncooperative MARL (Cheruiyot et al. 2025). Common points: the field is simulation-heavy; federated MARL for UAVs exists mostly for networking tasks with few UAVs; averaging across heterogeneous environments converges to a suboptimal policy; self-interested federated participants need incentives. The SAR review duplicate points to Core.

### [`Survey/Safety_layer/`](Survey/Safety_layer/SUMMARY.md)
Safety layers around learned policies. ElSayed-Aly et al. (AAMAS 2021): LTL shields for MARL give zero collisions during learning with minimal interference, and reward penalties alone do not. Qin et al. (ICLR 2021): learned decentralized barrier certificates scale to 1,024 agents but are not 100% safe. Safaoui et al. 2023: RL planner plus chance-constrained QP filter on 6 real quadrotors (99% success in simulation, possible deadlocks). Guerrier et al. 2024: CBF-based safe RL survey; guarantees depend on the model, and filters can be more conservative at deployment than in training.

---

## All papers

22 unique papers (25 PDF files; three are duplicates or versions, noted below).

| # | Title | Year | Folder | Role for KarmaSky |
|---|---|---|---|---|
| 1 | Separation Assurance between Heterogeneous Fleets of Small Unmanned Aerial Systems via Multi-Agent Reinforcement Learning (Sharifi et al.) | 2026 | closest_work (v1), Core/Workdone (v3, main) | Baseline; fairness metric F_t; scenario and settings |
| 2 | Autonomous Air Traffic Controller: A Deep Multi-Agent Reinforcement Learning Approach (Brittain, Wei) | 2019 | closest_work | Baseline lineage (BlueSky MARL) |
| 3 | A Deep Multi-Agent Reinforcement Learning Approach to Autonomous Separation Assurance (Brittain, Yang, Wei) | 2020 | closest_work | Baseline (attention encoder; γ 0.99, λ 0.95) |
| 4 | Reinforcement Learning-Based Air Traffic Deconfliction (Osipychev et al.) | 2022 | closest_work | Safety shield argument; relative observations |
| 5 | Model-aided Federated Reinforcement Learning for Multi-UAV Trajectory Planning in IoT Networks (Chen et al.) | 2023 | closest_work, Core/Feasibility_&_workdone (identical) | Federation loop; 50-episode interval; F1 |
| 6 | Hierarchical Federated Graph Attention Networks for Scalable and Resilient UAV Collision Avoidance (Shit, Subudhi) | 2025 | closest_work (downloaded) | Novelty check; federation, robust aggregation, DP |
| 7 | Time-To-Reach Separation and Safety Filtering for Safe, Fair, and Efficient Multi-Agent Coordination (Low et al.) | 2026 | closest_work (downloaded) | Novelty check; priority-aware safety filter; fairness metric |
| 8 | Hierarchical Reinforcement Learning for Cooperative Air-Ground Delivery in Urban System (Lei et al.) | 2026 | closest_work | Context (delivery dispatch) |
| 9 | Scalable Autonomous Separation Assurance With Heterogeneous Multi-Agent Reinforcement Learning (Brittain, Wei) | 2022 | Core/Workdone | Baseline (intent head); feasibility |
| 10 | Federated Multi-Agent Reinforcement Learning for UAV Collision Avoidance in Dense Smart City Environment (Rezaee et al.) | 2024 | Core/Feasibility_&_workdone | Federation (shallow example) |
| 11 | Optimization and Tactical Deconfliction for Drone Search-and-Rescue in Low-Altitude Airspace: A Systematic Literature Review (Samu et al.) | 2026 | Core/Gap, General (identical) | Safety shield evidence (crewed aircraft gap) |
| 12 | Personalized Observation Normalization for Federated Reinforcement Learning in Simulation Environments with Heterogeneity (Pang et al.) | 2025 | Federation_and_security | Federation (heterogeneous fleets) |
| 13 | Local Model Poisoning Attacks to Byzantine-Robust Federated Learning (Fang et al.) | TODO (not printed) | Federation_and_security | Privacy/attacks; integrity checks; exam-style scoring |
| 14 | Robust and Personalized Federated Learning for Aircraft-Engine Prognostics (Mitra et al.) | 2026 | Federation_and_security | Federation and attacks between rival operators |
| 15 | A Survey on UAV Control with Multi-Agent Reinforcement Learning (Ekechi et al.) | 2025 | General | Background (federated MARL for UAVs) |
| 16 | Artificial Intelligence Approaches for UAV Deconfliction: A Comparative Review and Framework Proposal (Chagas et al.) | 2025 | General | Background (deconfliction methods) |
| 17 | Multi-Agent Reinforcement Learning for truck-drone routing in smart logistics: A comprehensive review (Arishi, Ahuja) | 2025 | General | Context (logistics) |
| 18 | A Survey of Multi Agent Reinforcement Learning: Federated Learning and Cooperative and Noncooperative Decentralized Regimes (Cheruiyot et al.) | 2025 | General | Federation theory; incentives (karma motivation); privacy |
| 19 | Safe Multi-Agent Reinforcement Learning via Shielding (ElSayed-Aly et al.) | 2021 | Safety_layer | Safety shield |
| 20 | Learning Safe Multi-Agent Control with Decentralized Neural Barrier Certificates (Qin et al.) | 2021 | Safety_layer | Safety shield (learned alternative) |
| 21 | Safe multi-agent motion planning under uncertainty for drones using filtered reinforcement learning (Safaoui et al.) | 2023 | Safety_layer | Safety shield (filter on RL) |
| 22 | Learning Control Barrier Functions and their application in Reinforcement Learning: A Survey (Guerrier et al.) | 2024 | Safety_layer | Safety shield background |

Code (not a paper): Chen et al., Multi_UAV_Data_Harvesting (BSD 3-Clause), in `Core/Feasibility_&_workdone/`, not committed.

---

## Overall research picture

**What is done**
- MARL with PPO and attention keeps many aircraft separated on BlueSky route networks using speed-only actions (Brittain and Wei 2019, 2020, 2022).
- Two competing companies with different drones can each train their own policy and reach a safe equilibrium, but the weaker company is delayed more (Sharifi et al.: T̄_B 22.4% above T̄_A, F_t 80.8%).
- Federated RL works for UAVs inside one team (Chen et al.; Rezaee et al.; HF-GAT) and for heterogeneous environments when some parts stay private (Pang et al.; Mitra et al.).
- Poisoned updates can break averaging and even "robust" aggregators (Fang et al.; Mitra et al.).
- Shields and safety filters keep learned policies safe with minimal interference (ElSayed-Aly et al.; Safaoui et al.; TTR paper), and a priority-aware filter can enforce a right-of-way order (TTR paper).

**The gap KarmaSky targets**
- No paper in this survey federates learning between *competing* drone operators that share airspace.
- No paper measures or tries to reduce the delay gap between operators that Sharifi et al. found.
- No paper turns measured contribution to shared learning into priority at contested crossings (karma credits), and none combines that with a hard shield that puts manned aircraft first.
- Incentives for self-interested federated participants are named as an open need (Cheruiyot et al., Sec. 3.12) but not built.

**Main overlap risks**
- **Sharifi et al. (2605.01041)** already owns the problem statement (competing companies, heterogeneous fleets, unfairness, F_t, the Frisco scenario). We must present the unfairness as their finding and our work as the response. A follow-up from the same group on fairness-aware deconfliction is a realistic risk. TODO: re-check arXiv before Gate 0 and before writing.
- **HF-GAT (2511.11616)** already combines federated learning, UAV collision avoidance, Byzantine-robust aggregation and DP, but in one swarm with no operators, fairness or credits.
- **TTR paper (2605.20625)** already combines right-of-way priority, a priority-aware safety filter and a fairness metric at a merge, but priority is first-come-first-served, not earned, and there is no learning, federation or operators.
- **Brittain and Wei 2022** already frames heterogeneous agents as competing companies with proprietary models, but studies safety only.
- **Mitra et al. 2026** already studies federation and poisoning between rival aircraft operators, but for supervised prognostics, not airspace MARL.

**Not covered by this folder (TODO)**
- Papers listed in `05_READING_LIST.md` but not present here: FedAvg (McMahan et al.), q-FFL (Li et al.), CARMA and Multi-Karma (Elokda et al.), Shapley volatility in FL (Geimer et al.), FRIDA, honesty among competitors, gradient inversion for RL (Li, Ding, Zhao) and RGIA, Market Design for Drone Traffic Management, FairFly, Huang et al. cross-silo FL, and BlueSky / BlueSky-Gym. The karma, Shapley and free-rider papers matter most for the overlap check of the karma part.
- The Sharifi et al. rule-based baseline reference (arXiv 2603.28561) is not in this folder.
