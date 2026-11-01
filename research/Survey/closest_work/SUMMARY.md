# closest_work: Summary

## 1. What this folder is about

These are the papers closest to KarmaSky. They cover RL-based separation assurance in BlueSky (Brittain and Wei), the two-company heterogeneous-fleet study that is our baseline (Sharifi et al.), federated RL for UAVs (Chen et al., HF-GAT), priority and fairness at a merge with a safety filter (TTR paper), RL with a surrogate model and real flight tests (Osipychev et al.), and air-ground delivery dispatch (HRL4AG). The two preprints the plan flagged as novelty risks (arXiv 2511.11616 and 2605.20625) were downloaded into this folder on 2026-11-01 and are covered below.

**Files and versions**
- `2605.01041v1.pdf` is version 1 of Sharifi et al. The main version used here is **v3**, stored at `../Core/Workdone/2605.01041v3.pdf`. Text comparison: v1 and v3 report the same method, settings and numbers; v3 drops the "Index Terms" line and trims the reference list (v1 ends at reference [26], v3 at [25]).
- `2306.02029v2.pdf` (Chen et al.) is the same file as `../Core/Feasibility_&_workdone/2306.02029v2.pdf` (identical checksum). Its full card is here; the Core summary points back to it.

PDFs are not committed to the repository (public repo). Use the links in each card.

---

## 2. Paper cards

### 2.1 Sharifi et al. 2026: heterogeneous fleets of competing companies (OUR BASELINE)

- **Citation:** Iman Sharifi, Hyeong Tae Kim, Maheed Hatem Ahmed, Mahsa Ghasemi, Peng Wei. "Separation Assurance between Heterogeneous Fleets of Small Unmanned Aerial Systems via Multi-Agent Reinforcement Learning." arXiv preprint, arXiv:2605.01041v3 [cs.MA], 8 May 2026 (v1: 1 May 2026). Link: https://arxiv.org/abs/2605.01041
- **Files:** `2605.01041v1.pdf` (this folder), `../Core/Workdone/2605.01041v3.pdf` (main version)
- **Problem:** Two questions: (1) can separately trained tactical deconfliction policies of two companies with different aircraft reach an equilibrium with a conflict-free airspace, and (2) if so, does that equilibrium discriminate against the company with weaker aircraft? (Abstract, Sec. I)
- **Method:**
  - PPO-driven advantage actor-critic (PPOA2C) with GAE and a multiplicative attention module over intruders (Sec. III-B).
  - Each fleet trains its own policy; agents inside a fleet share one policy and one replay buffer; nothing is shared between fleets except publicly broadcast state (Remote ID assumption) (Sec. III-A, III-C).
  - State: ownship [distance to next waypoint, speed, heading, acceleration]; each intruder mirrors this but uses ownship-to-intruder distance. Only "front intruders" (aircraft reaching the next bottleneck earlier) are considered (Sec. III-C.1).
  - Action: {-Δv, 0, +Δv}, fleet-specific magnitude (Sec. III-C.2).
  - Reward: R_LoS + R_V + R_A + R_M + R_T (separation, speed limits, action changes, mission completion, time) (Sec. III-C.3).
  - Network: ownship and intruder inputs through separate 64-unit FC layers, 64×64 attention, two 128-unit FC layers, then actor and critic heads (Sec. III-D). No intent head is described in this paper.
  - Settings (Sec. III-D): learning rate 10^-4, entropy coefficient 10^-3, clip 0.2, batch 512, Adam, 8 epochs per episode, d_NMAC 100 m, d_LoWC 500 m, goal tolerance 50 m, time step 3 s, mission horizon T 18 min, speed offsets 5.14 and 2.57 m/s. Discount factor and GAE lambda are not printed.
- **Setting / scenario (Sec. IV-A):**
  - BlueSky, airspace over Frisco (Dallas, Texas). Four fixed routes of about 10.33 km: I WP1→WP3→WP9→WP4, II WP2→WP3→WP9→WP4, III WP5→WP7→WP9→WP8, IV WP6→WP7→WP9→WP8. Merges at WP3 (M1) and WP7 (M2), intersection at WP9 (IN).
  - 20 agents, 10 per company, 5 per route. Company A flies routes I and III, Company B routes II and IV. Spawn times 35 + 5k s, k random in {0, ..., 10}.
  - Configuration X (strong, based on Google Wing Hummingbird): speed [0, 44.88] m/s, acceleration {-1.71, 0, 1.71} m/s², sensing 1000 m. Configuration Y (weak, based on Amazon MK30): [0, 30.12] m/s, {-1.02, 0, 1.02} m/s², 750 m.
  - Baselines: an enhanced rule-based policy (from the authors' reference [25]) and a random policy. Seven policy-configuration combinations.
  - Training: PyTorch, one RTX 3090, 2,500 episodes per run (about 600,000 steps), about 12 min of flight (240 steps) per episode, more than 7 hours per run, 5 seeds (about 140 hours), 300 evaluation episodes.
- **Key results:**
  - Fig. 3: for PPOA2C(X)+PPOA2C(Y), rewards converge after about 1,200 episodes; successful agents approach 20.
  - Table I, total average NMACs per episode: Random(X)+Random(Y) 7.99; Rule(X)+Rule(Y) 0.77; PPOA2C(X)+PPOA2C(Y) 0.22; PPOA2C(X)+Rule(Y) 0.006; Rule(X)+Rule(X) 0.53; PPOA2C(X)+PPOA2C(X) 0.30; PPOA2C(X)+Rule(X) 0.14.
  - Table I, success N_s/20 (same order): 3.96±1.77, 18.53±1.65, 19.55±0.98, 19.98±0.10, 19.42±0.7, 19.79±0.60, 19.90±0.34.
  - Table I, mission time T̄_A / T̄_B (min) and fairness F_t (%): Rule XY 5.88 / 7.13, 82.4; **PPOA2C(X)+PPOA2C(Y) 7.23 / 8.94, 80.8**; PPOA2C(X)+Rule(Y) 6.58 / 7.60, 86.5; Rule XX 5.05 / 5.05, 100; PPOA2C XX 7.42 / 7.54, 98.4; PPOA2C(X)+Rule(X) 5.46 / 5.02, 91.9.
  - Sec. IV-C text: PPOA2C success rates 97.75% (XY) and 98.95% (XX). Against the rule-based pair, PPOA2C raised N_s by 5.5% (1.9%) and cut NMACs by 71.4% (43.3%). About 75% of remaining NMACs in PPOA2C(X)+PPOA2C(Y) are between the two companies (AB).
  - Sec. IV-D: **T̄_B is 22.4% greater than T̄_A** in PPOA2C(X)+PPOA2C(Y); average F_t of 81.6% when configurations differ. With identical configurations but different policies, PPOA2C(X)+Rule(X) has T̄_A 8.76% greater than T̄_B (F_t 91.9%).
  - Fairness metric (Sec. IV-D): F_t(%) = (1 − |t1 − t2| / max(t1, t2)) × 100.
- **Limitations stated by the authors:** occasional NMACs remain under dense traffic, which the authors attribute to interdependent actions (Sec. IV-B). They state that both policy and configuration heterogeneity lower time-based fairness and call for "fairness-aware conflict management" (Abstract, Sec. IV-D, V). They propose no fix. (Note: Sec. III-D sets the mission horizon to 18 min while Sec. IV-A.3 says each episode simulated about 12 minutes; the paper does not explain the difference.)
- **Relevance to KarmaSky:** **baseline** (B1 reproduces this setup) and **fairness metric** (F_t, mission time per company). The fleet specs, scenario, reward and PPO settings in our configs come from here.

### 2.2 Brittain and Wei 2019: Autonomous Air Traffic Controller (DD-MARL)

- **Citation:** Marc Brittain, Peng Wei. "Autonomous Air Traffic Controller: A Deep Multi-Agent Reinforcement Learning Approach." arXiv:1905.01303v1 [cs.LG], 2 May 2019. Link: https://arxiv.org/abs/1905.01303 (venue not printed in the PDF)
- **File:** `1905.01303v1.pdf`
- **Problem:** Resolve conflicts between many aircraft in a high-density en-route sector with intersections and merging points, using speed advisories (Sec. 1, 3).
- **Method:** Centralized learning, decentralized execution: one A2C network with PPO clipped loss shared by all aircraft. State: ownship plus the 3 closest relevant aircraft (rules: same or conflicting route, not past the intersection). The N-closest information is encoded by a 32-node FC layer, joined with the ownship state, then 2 × 256 FC layers with shared actor and critic. Action every 12 s from {min speed, hold, max speed}. Conflict = closer than 3 nmi. Settings: lr 0.0001, γ 0.99, ε 0.2, α 0.1, β 0.005, Adam (Sec. 3.3, 4, 5.2).
- **Setting / scenario:** BlueSky. All aircraft Boeing 747-400, fixed routes. Case Study 1: three routes, two intersections. Case Study 2: two routes merging. 30 aircraft per episode, arrivals uniform over 4, 5 and 6 minutes (Sec. 3.2, 5.3, 5.4).
- **Key results:** Trained 20,000 episodes (Case 1) and 5,000 (Case 2). Table 1 (200 test episodes): Case 1 mean 29.99 ± 0.141, median 30; Case 2 mean 30, median 30, i.e. 99.97% and 100% of conflicts resolved. Case 1 training took less than 4 days (Sec. 5.5).
- **Limitations stated by the authors:** some stochastic geometries may make 3 nmi separation impossible, in which case human ATC would be alerted; uniform loss-of-separation only (non-uniform left for future work) (Sec. 3.3.1, 5.5).
- **Relevance to KarmaSky:** **baseline** lineage (the PPO-A2C + BlueSky + speed-advisory design Sharifi builds on). One policy for everyone, no competing operators, no fairness, no federation.

### 2.3 Brittain, Yang and Wei 2020: D2MAV-A with attention

- **Citation:** Marc W. Brittain, Xuxi Yang, Peng Wei. "A Deep Multi-Agent Reinforcement Learning Approach to Autonomous Separation Assurance." arXiv:2003.08353v2 [cs.LG], 27 Aug 2020. Link: https://arxiv.org/abs/2003.08353 (venue not printed in the PDF)
- **File:** `2003.08353v2.pdf`
- **Problem:** Separation assurance for a variable number of aircraft without fixing N closest neighbors or a sorting rule (Sec. I-B, III).
- **Method:**
  - PPO with a Luong multiplicative attention network over all intruders (Eq. 10 to 13); one shared network (centralized learning, decentralized execution).
  - Ownship and intruder inputs pre-processed by 128-node FC layers, attention with 128 nodes, attention vector joined with the ownship vector, 2 × 256 FC layers. Leaky ReLU.
  - Reward R(s) + R(a), where R(a) penalizes every non-hold action.
  - Ray-based parallel BlueSky with 30 workers (Sec. IV, V-A).
  - Table 1 hyperparameters: lr 0.0001, GAE γ 0.99, GAE λ 0.95, PPO ε 0.2, α 0.1, δ 0.05, ψ 0.001, entropy β 0.0001, 30 workers, Leaky ReLU α 0.2.
- **Setting / scenario:** BlueSky, Airbus A320, three en-route case studies (A, B, C), 30 aircraft, inter-arrival uniform over 3 to 6 minutes in 12 s steps, conflict at 3 nmi (Sec. III, V-C).
- **Key results:**
  - Table 2 (200 episodes, mean ± sd): D2MAV-A 29.99 ± 0.141 (A), 30 ± 0.0 (B), 30.0 ± 0.0 (C); random baseline 17.77, 10.36, 17.45.
  - Table 3 (episodes to convergence): D2MAV-A 3,994 / 17,390 / 68,912; it was the only variant that converged on C.
  - Fig. 5: normalized performance constant from 10 to 100 aircraft.
  - Sec. VI-D: 100k episodes took 5 to 8 days without parallel workers versus 3 to 5 hours with D2MAV-A (RTX 2080 Ti).
  - Table 4: transfer learning cut convergence on case D from 37,172 to 908 episodes.
- **Limitations stated by the authors:** same note that 3 nmi may sometimes be unachievable and human ATC would be alerted (Sec. VI-A).
- **Relevance to KarmaSky:** **baseline** (source of the attention encoder used by Sharifi; also the only paper in this folder that prints a GAE λ: 0.95, together with γ 0.99). Single shared policy, no fairness, no federation.

### 2.4 Osipychev, Margineantu and Chowdhary 2022: RL deconfliction with surrogate and flight demo

- **Citation:** Denis Osipychev, Dragos Margineantu, Girish Chowdhary. "Reinforcement Learning-Based Air Traffic Deconfliction." 36th Conference on Neural Information Processing Systems (NeurIPS 2022) (footer); arXiv:2301.01861v1 [cs.RO], 5 Jan 2023. Link: https://arxiv.org/abs/2301.01861
- **File:** `2301.01861v1.pdf`
- **Problem:** Horizontal separation of two aircraft in uncontrolled airspace without procedural separation (Sec. 1).
- **Method:** Train a PPO policy (Stable Baselines, MLP 2 × 256) on a lightweight 2D surrogate environment (Dubins turns, mass-less kinematics) that is deliberately more conservative than the real aircraft (Table 1). Observations use relative quantities only (heading, airspeed, distance and angle to goal and intruder), normalized to [-1, 1]. At run time the policy and surrogate are rolled out to produce 20 waypoints spaced 20 s apart (400 s horizon), published via ROS (Sec. 2, 3).
- **Setting / scenario:** 20 × 20 km area, one agent and one passive intruder. Evaluation in a Boeing high-fidelity simulation and on a real Cessna 208 Caravan (Grant County International Airport, 2021) (Sec. 3.2, 5).
- **Key results:** Training ran 10^8 steps (about 10^6 episodes, about three years of simulated time); average score +75.0 on the surrogate (Sec. 3.1, Fig. 4). Batch evaluation over more than 10^4 random conditions: 98% success, 2% failures, mostly cases that started too close (Sec. 4.1, Fig. 6). Response time below 60 ms per trajectory (Sec. 3.3).
- **Limitations stated by the authors:** single passive intruder that does not change intent; full observability assumed; surrogate and real dynamics differ, causing trajectory error (Fig. 7). "With the relatively high number of failures, the system is not designed to work as a stand-alone system and requires a safety layer constructed on top" (Sec. 4.1).
- **Relevance to KarmaSky:** **safety shield** (argument that a learned avoidance policy needs a safety layer on top) and **privacy** (relative-only observations, matching privacy fix 2 in `06_DESIGN_UPDATES.md`). Single agent, no fairness, no federation.

### 2.5 Chen et al. 2023: Model-aided Federated RL (FedQMIX) for multi-UAV data harvesting

- **Citation:** Jichao Chen, Omid Esrafilian, Harald Bayerlein, David Gesbert, Marco Caccamo. "Model-aided Federated Reinforcement Learning for Multi-UAV Trajectory Planning in IoT Networks." arXiv:2306.02029v2 [cs.LG], 7 Oct 2023; footnote: final version accepted by IEEE GLOBECOM Workshops 2023. Link: https://arxiv.org/abs/2306.02029. Code: https://github.com/Cirrick/Multi_UAV_Data_Harvesting
- **Files:** `2306.02029v2.pdf` (also in `../Core/Feasibility_&_workdone/`)
- **Problem:** Plan cooperative trajectories for several UAVs collecting data from IoT devices when real-world training data is expensive and the radio channel and some device positions are unknown (Sec. I, II).
- **Method:** Alternate between (1) learning a simulation model from real measurements (neural channel model, PSO to localize unknown devices) and (2) training QMIX in that simulation. In FedQMIX each UAV trains a local QMIX model in its own simulated copy; every N_freq episodes all UAVs send their model to an aggregator that takes the plain average θ = (1/I) Σ θ_i and sends it back (Sec. IV-B, Algorithm 1). A safety controller restricts each agent to feasible actions (boundaries, battery to reach destination) (Sec. III-A).
- **Setting / scenario:** 3 UAVs at fixed, different altitudes (55, 60, 65 m), so no collision avoidance between them. Two maps: RBM 600 m × 800 m and RDM 1000 m × 1200 m, 10 devices each. Adam lr 5 × 10^-4, **N_freq = 50**, E_max = 30 real-world episodes, N = 1000 simulated episodes per real episode (Sec. V).
- **Key results:** Fig. 2 (averaged over three runs): model-aided FedQMIX reaches the same data-collection performance as QMIX trained on real samples while using "around three magnitudes" less real-world data, converges faster than model-aided QMIX without federation; IQL underperforms (Sec. V).
- **Limitations stated by the authors:** environment-model learning is still centralized (measurements go to a central server); full decentralization is future work (Sec. V, VI).
- **Relevance to KarmaSky:** **federation** (template for the federation round and the F1 equal-average rule; source of the 50-episode interval). All UAVs belong to one cooperative team with a shared reward: there is no competition and no fairness question between operators.

### 2.6 Shit and Subudhi 2025: HF-GAT, hierarchical federated graph attention for UAV collision avoidance (NOVELTY CHECK 1)

- **Citation:** Rathin Chandra Shit, Sharmila Subudhi. "Hierarchical Federated Graph Attention Networks for Scalable and Resilient UAV Collision Avoidance." arXiv:2511.11616v1 [cs.RO], 5 Nov 2025. Link: https://arxiv.org/abs/2511.11616 (no venue printed)
- **File:** `2511.11616.pdf` (downloaded 2026-11-01)
- **Problem:** Balance real-time performance, Byzantine resilience and privacy for collision avoidance in large UAV swarms (Abstract, Sec. I).
- **Method:** Three layers (Sec. II, III):
  - Local (0 to 10 ms): dense temporal graph attention over 5 to 8 neighbors within 100 m, reflexive maneuver when risk > 0.8, differential privacy on shared positions (ε = 0.5).
  - Regional (10 to 30 ms): clusters of 20 to 50 UAVs, sparse attention with k = log2(n) neighbors. Asynchronous federated learning with coordinate-wise trimmed-mean aggregation, f < n/3, aggregation once the buffer holds 2f + 1 gradients, anomaly threshold 0.3. Adaptive DP budget ε ∈ [0.1, 1.0] driven by a threat score = 0.5·r_reject + 0.3·d_anomaly + 0.2·c_comm.
  - Global (30 to 50 ms): Hashgraph-inspired consensus and a Kademlia DHT audit log with zero-knowledge proofs.
- **Setting / scenario:** AirSim with rotor dynamics, NVIDIA Jetson Xavier NX, 1 km communication radius, 10 to 500 UAVs in a 1 km³ urban area. Baselines: centralized DRL, vanilla FedAvg, monolithic federated GAT with blockchain logging (Sec. IV).
- **Key results (text and Figs. 2 to 4; the paper has no result tables):** 95th-percentile decision latency below 40 ms at 500 UAVs, about 70% lower than monolithic FGAT; up to 92% less communication; under Byzantine attack (gradient poisoning, false positions) collision rate does not exceed 6% with 89.1% mission success, versus over 40% collisions for vanilla FedAvg; below 2% collisions in normal conditions; 12 to 18% higher accuracy than static high-privacy settings; DHT audit "estimated 85%" lower overhead than blockchain.
- **Limitations stated by the authors:** future work on hardware-in-the-loop validation, safety verification and energy-aware allocation (Sec. V). The paper does not report the RL algorithm, reward, training budget or number of seeds.
- **Relevance to KarmaSky:** **federation** and **privacy/attacks** (trimmed-mean robust aggregation, adaptive DP, Byzantine clients). All UAVs are one swarm: no competing operators, no fairness between operators, no contribution scoring, no credits.

### 2.7 Low et al. 2026: Time-To-Reach separation and safety filtering (NOVELTY CHECK 2)

- **Citation:** Matthew Low, Jasmine Jerry Aloor, Victoria Marie Tuck, Pierluigi Nuzzo, Jason J. Choi. "Time-To-Reach Separation and Safety Filtering for Safe, Fair, and Efficient Multi-Agent Coordination." arXiv:2605.20625v2 [eess.SY], 25 Sep 2026; "Accepted to appear in the 65th IEEE Conference on Decision and Control (CDC 2026)". Link: https://arxiv.org/abs/2605.20625. Code: https://github.com/mlow2/ttr_guidance
- **File:** `2605.20625.pdf` (downloaded 2026-11-01; the file is v2)
- **Problem:** Coordinate several air taxis merging into one air corridor safely, efficiently and fairly (Abstract, Sec. III).
- **Method:** Minimum time-to-reach (TTR), computed offline with Hamilton-Jacobi reach-avoid analysis, is used three ways (Sec. IV):
  - priority: first come, first served by initial TTR;
  - temporal spacing: each vehicle tracks a target TTR, T_target_i = T_target_1 + (i − 1)·ΔT;
  - a priority-consistent control barrier function (CBF) safety filter built from a pairwise HJ value function.

  Three filter modes: decentralized pairwise CBF-QP (Dec), priority-coordinated multi-stage QP where the lower-priority vehicle yields first (Prio), and a centralized joint QP (Cent) (Table I). Fairness is measured with Kendall's τ between actual arrival order and priority order, plus the spread of normalized delay (Sec. III-B, Table II).
- **Setting / scenario:** 2D air-taxi model with wind; 100 random scenarios with N = 8 vehicles, ΔT = 10 s, separation 500 m (Table IV), communication range 3 km, horizon 200 s (Table V). HJ computation under 30 minutes on an RTX 5090 (Sec. IV-B).
- **Key results (Table III, mean ± sd):**
  - Greedy TTR-min with no filter: 7.836 ± 7.616% unsafe time, P_pass 19.
  - TTR separation with no filter: 2.081 ± 2.667%, P_pass 43.
  - Greedy TTR-min with filters: Dec 0.194%, Prio 0.256%, Cent 0.742%; τ_K 0.91; P_pass 90 / 87 / 72; P⁺_pass 35 / 33 / 32.
  - TTR separation with filters: Dec 0.118%, Prio 0.058%, Cent 0.044%; τ_K 0.99; P_pass 95 / 96 / 93; P⁺_pass 82 / 82 / 80.
  - Efficiency cost: T_last 97.67 / 99.69 / 96.16 s versus 82.42 / 83.88 / 81.15 s for greedy with filters.
  - Prio filter solve time about 5 ms; it halves the Dec violation rate (Sec. V-3).
- **Limitations stated by the authors:** planar 2D model (3D is future work); numerical TTR error up to about 10 s (Remark 2); TTR computation scalability (Sec. VI). Vehicles are homogeneous and nothing is learned.
- **Relevance to KarmaSky:** **safety shield** (priority-aware filter, "lower priority yields" logic close to our "credits decide who yields, shield has final say") and **fairness metric** (order-based fairness, an alternative to F_t). Priority here is first-come-first-served from physics, not earned, and there is one operator, no learning and no federation.

### 2.8 Lei et al. 2026: HRL4AG, hierarchical RL for cooperative air-ground delivery

- **Citation:** Songxin Lei, Chunming Ma, Haomin Wen, Yexin Li, Lizhenghe Chen, Qianyu Yang, Fugee Tsung, Lei Chen, Sijie Ruan, Yuxuan Liang. "Hierarchical Reinforcement Learning for Cooperative Air-Ground Delivery in Urban System." Proceedings of the 32nd ACM SIGKDD Conference on Knowledge Discovery and Data Mining (KDD '26), 2026. DOI: https://doi.org/10.1145/3770855.3818964. arXiv:2602.12913v2 [cs.CY], 4 Aug 2026. Code: https://github.com/thunderlrr/Cooperative-Air-Ground-Delivery
- **File:** `2602.12913v2.pdf`
- **Problem:** Dispatch delivery orders across a heterogeneous fleet of UAVs and ground carriers at scale (Sec. 1).
- **Method:** One central dispatcher modeled as an MDP. A manager chooses UAV or carrier mode per order; mode-specific workers score order-vehicle pairs; type-specific transformer encoders; intrinsic reward for workers following the manager; trajectory-based reward shaping (weights 1.5 matched, 3.0 picked up, 10.0 delivered; 0.2 time decay); DDPG. Feasibility pruning includes a UAV safe-return energy check (Sec. 3, 4).
- **Setting / scenario:** Shanghai (20,664 orders, 30 days) and Chengdu (96,376 orders, 6 days) datasets (Table 1); 30 to 50 vehicles, UAV:carrier 1:1; 5 seeds; RTX A4000; batch 32, lr 0.005, hidden size 256 (Sec. 5.1).
- **Key results (Table 2):**
  - Shanghai, HRL4AG pickups / deliveries / execution time: 38 / 30 / 0.17 s (30 vehicles), 41 / 36 / 0.2 s (40), 49 / 39 / 0.35 s (50).
  - Chengdu, same order: 82 / 76 / 0.35 s, 89 / 85 / 0.56 s, 95 / 88 / 0.83 s.
  - Sec. 5.2: 18% to 28% (Shanghai) and 20% to 25% (Chengdu) more deliveries than the second-best baseline. The abstract states up to 26% higher delivery success and an 80-fold efficiency gain.
  - Removing the hierarchy raised execution time from 0.35 s to 22.1 s on Shanghai (Sec. 5.3.1).
- **Limitations stated by the authors:** objective ignores UAV energy use and carrier detours; policy sensitive to order distributions, and extreme demand may make it rely on one mode, "leading to uneven fleet wear and potential resource allocation unfairness"; real deployment would need collision avoidance and no-fly-zone handling, which are not modeled (Sec. 7).
- **Relevance to KarmaSky:** context only (delivery operations layer). One operator, no airspace conflicts, no federation. Low relevance to our mechanism.

---

## 3. What these papers point to together

- **MARL works for tactical deconfliction in BlueSky-style route networks.** Brittain and Wei (2019, 2020) and Sharifi et al. all reach near-optimal success on structured routes with speed-only actions and attention over intruders. They agree that attention removes the need to fix N neighbors (Brittain 2020, Table 3).
- **Heterogeneity creates unfairness, and nobody fixes it.** Sharifi et al. is the only paper here with two companies. It shows the weaker fleet is delayed (T̄_B 22.4% above T̄_A, F_t 80.8%) and stops at "the need for fairness-aware conflict management". The TTR paper treats fairness as respecting a first-come-first-served order between identical vehicles of one system, which is a different notion.
- **Federation is shown for UAVs, but only inside one team.** Chen et al. (cooperative data harvesting, plain averaging every 50 episodes) and HF-GAT (one swarm, trimmed-mean aggregation, DP) both federate agents that share a goal. Neither has rival operators, a fairness objective, or any scoring of who contributed what.
- **Safety layers on top of learning are widely recommended.** Osipychev et al. say their RL system needs a safety layer; Chen et al. mask infeasible actions; the TTR paper's priority-consistent CBF filter is the most developed version. They agree that the filter, not the policy, should make the final safety decision.
- **Where they differ:** Brittain/Sharifi share one policy per fleet and train inside BlueSky; Osipychev trains on a simplified surrogate; HF-GAT and TTR do not use BlueSky. Fairness is measured by mission time (Sharifi, F_t) versus arrival order (TTR, Kendall τ).
- **The gap KarmaSky targets:** no paper here combines (1) federated learning between *competing* operators, (2) an explicit fairness objective between operators, and (3) priority that is *earned* through measured contribution (karma credits), with (4) a safety shield that overrides that priority. Sharifi supplies the problem, Chen the federation loop, TTR and Osipychev the safety-layer argument.

## 4. Overlap risk

Blunt assessment, paper by paper:

- **Sharifi et al. (2605.01041): high overlap on the problem, none on the solution.** It already owns "competing companies, heterogeneous fleets, independent PPO, weaker fleet is treated unfairly", including the F_t metric, the Frisco scenario and the X/Y specs. We cannot claim to have discovered the unfairness; we can only claim to address it. It does not federate, score contributions, or give priority. Same research group (Peng Wei) as Brittain and Wei; a follow-up from them on fairness-aware deconfliction is a realistic risk. TODO: re-check arXiv for newer versions or follow-ups from these authors before Gate 0 and again before writing.
- **HF-GAT (2511.11616): medium overlap on the federation and security part.** It already does federated learning for UAV collision avoidance with Byzantine-robust aggregation (trimmed mean) and differential privacy. Our federation, integrity checks and DP option are therefore not new on their own. It does not have competing operators, fairness between operators, contribution scoring or earned priority. All numbers come from figures and the method details are thin, so it is a weak comparison point for exact numbers.
- **TTR separation and safety filtering (2605.20625): medium overlap on the priority and safety part.** It already assigns right-of-way at a merge, enforces it with a priority-consistent safety filter, and measures fairness. Our "priority + shield" layer resembles this. Differences: their priority is first-come-first-served from physics, not earned through contribution; vehicles are homogeneous and belong to one system; no learning, no federation, no operators.
- **Chen et al. (2306.02029): low overlap.** Federated MARL for UAVs, but one cooperative team, no collisions between UAVs (fixed altitudes), no fairness. The docs already call it "the gap".
- **Brittain and Wei 2019, 2020; Osipychev et al.; HRL4AG: low overlap.** Single operator or single policy; no federation, no fairness between operators, no earned priority.
- **Nothing in this folder implements contribution-earned priority (karma credits from Shapley-scored contributions) between competing operators.** On the papers present, the combined core idea is still open. This only holds for these files; the karma, Shapley-in-FL and free-rider papers in `05_READING_LIST.md` are not in `research/` and were not checked here. TODO.

## 5. What we use from here

- [FROM PAPER] Frisco scenario: four routes of about 10.33 km, merges at WP3 and WP7, intersection at WP9, 2 companies × 10 drones, 5 per route, spawn 35 + 5k s (Sharifi et al., Sec. IV-A). Waypoint coordinates are not printed: TODO.
- [FROM PAPER] Fleet X: speed [0, 44.88] m/s, acceleration ±1.71 m/s², sensing 1000 m. Fleet Y: [0, 30.12] m/s, ±1.02 m/s², 750 m (Sharifi et al., Sec. IV-A.2).
- [FROM PAPER] Step 3 s, mission horizon 18 min, d_NMAC 100 m, d_LoWC 500 m, goal tolerance 50 m (Sharifi et al., Sec. III-D).
- [FROM PAPER] PPO settings: lr 10^-4, entropy 10^-3, clip 0.2, batch 512, 8 epochs per episode, Adam, GAE (Sharifi et al., Sec. III-B, III-D).
- [FROM PAPER] Network: 64-unit ownship and intruder encoders, 64 × 64 attention, two 128-unit layers, actor and critic heads (Sharifi et al., Sec. III-D).
- [FROM PAPER] 2,500 training episodes, 300 evaluation episodes (Sharifi et al., Sec. IV-A.3). Sharifi used 5 seeds; our plan uses 3 seeds [PROPOSED].
- [FROM PAPER] Fairness metric F_t = (1 − |t1 − t2| / max(t1, t2)) × 100, and NMAC counts split AA / AB / BB and by bottleneck (Sharifi et al., Sec. IV-C, IV-D).
- [FROM PAPER] Enhanced rule-based baseline as the reference for B3 (Sharifi et al., Sec. IV-B.1; details in their reference [25], arXiv:2603.28561, not in this folder: TODO).
- [FROM PAPER] Federation round: local training, send model every N_freq = 50 episodes, plain average, send back (Chen et al., Sec. IV-B, V). Basis of F1 and of the 50-episode interval.
- [FROM PAPER] Candidate GAE values γ 0.99, λ 0.95 (Brittain, Yang and Wei 2020, Table 1). Sharifi et al. do not print them; whether to use these is [OPEN].
- [FROM PAPER] Relative-only observations (Osipychev et al., Sec. 2.3) as a precedent for privacy fix 2.
- [FROM PAPER] Priority-consistent safety filter where the lower-priority vehicle adapts first, and Kendall τ as a secondary fairness check (Low et al., Sec. III-B, IV-D). Whether we adopt these is [OPEN].
- [FROM PAPER] Trimmed-mean aggregation and adaptive DP as possible defenses for the integrity and privacy experiments (Shit and Subudhi, Sec. III-A, III-B). Whether we adopt them is [OPEN].

## Could not read

None. All 8 PDFs in this folder were read.
