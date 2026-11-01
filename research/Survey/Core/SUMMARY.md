# Core: Summary

## 1. What this folder is about

The three core pillars from `05_READING_LIST.md`: proof that MARL can keep heterogeneous aircraft apart (Brittain and Wei, T-ASE 2022), what is already done (Sharifi et al. 2026, our baseline) and the federated gap (Chen et al. 2023 plus its code, and a second federated drone example). The `Gap/` subfolder holds a 2026 systematic review on drone search-and-rescue deconfliction that documents the missing crewed-aircraft and right-of-way logic. Subfolders: `Feasibility_&_workdone/`, `Gap/`, `Workdone/`.

**Files and duplicates**
- `Workdone/2605.01041v3.pdf` (Sharifi et al., v3) is the main version; its full card is in `../closest_work/SUMMARY.md` (section 2.1). v1 is in `../closest_work/`.
- `Feasibility_&_workdone/2306.02029v2.pdf` (Chen et al.) is identical to `../closest_work/2306.02029v2.pdf`; full card in `../closest_work/SUMMARY.md` (section 2.5).
- `Gap/drones-10-00596.pdf` is identical to `../General/drones-10-00596.pdf`; the full card is here (section 2.4), and the General summary points back.
- `Feasibility_&_workdone/Multi_UAV_Data_Harvesting-master/` and the `.zip` are the Chen et al. code. Not committed to our repository (third-party code, includes a 77 MB `.npy` file). See section 2.5.

PDFs are not committed (public repo). Two PDFs in this folder (Brittain and Wei 2022, Rezaee et al. 2024) carry an IEEE Xplore institutional licence stamp and must not be redistributed in any case.

---

## 2. Paper cards

### 2.1 Brittain and Wei 2022: MAASA, heterogeneous MARL with intent learning (FEASIBILITY)

- **Citation:** Marc Brittain, Peng Wei. "Scalable Autonomous Separation Assurance With Heterogeneous Multi-Agent Reinforcement Learning." IEEE Transactions on Automation Science and Engineering, vol. 19, no. 4, pp. 2837 to 2848, October 2022. DOI: https://doi.org/10.1109/TASE.2022.3151607
- **File:** `Workdone/Scalable_Autonomous_Separation_Assurance_With_Heterogeneous_Multi-Agent_Reinforcement_Learning.pdf`
- **Problem:** Earlier decentralized separation assurance (D2MAV-A) assumed every aircraft optimizes the same reward. In future airspace, "companies will operate their own autonomous aircraft with potentially proprietary software", so agents may follow different, unknown objectives (Sec. I-B, II, III-B).
- **Method:**
  - Each aircraft is an agent; agents are assigned to one of M models, each optimizing its own reward function.
  - An **intention learning model** predicts each intruder's action distribution and is trained jointly with PPO through a cross-entropy term: L = L_π + L_v + L_CE (Sec. III-B, Eq. 8 to 9).
  - Architecture (Sec. III-C, Figs. 1 and 2): ownship and intruder states each pre-processed by two 128-node FC layers; intent model of three 128-node FC layers plus a 3-node softmax output; predicted distribution concatenated to intruder features (128 to 131), back to 128 by an FC layer; attention as in D2MAV-A; concatenated with ownship; two 256-node FC layers; outputs value, policy and action prediction. Leaky ReLU.
  - State includes a model identifier m for ownship and intruders (Sec. III-A.1). Action every 12 s from {decelerate, hold, accelerate}. Reward R(s) + R(a) + ν (time step penalty).
  - Table I: lr 0.0001, GAE γ 0.99, GAE λ 0.95, PPO ε 0.4, entropy β 0.0001, 75 parallel workers, Leaky ReLU α 0.2.
- **Setting / scenario:** BlueSky with Ray parallel workers. Four en-route case studies (Table II: A 2 routes / 1 intersection, B 3/2, C 3/3, D 7/8). 50 Airbus A320 per episode, inter-arrival uniform over 3 to 6 minutes, 150k training episodes, 200 test episodes. Five reward functions (Table III), three used by default. AMD Threadripper 2950x and RTX 2080 Ti (Sec. IV).
- **Key results:**
  - Table IV, episodes to convergence: MAASA 3,110 / 28,278 / 81,539 / 81,898 (A to D); D2MAV-A 5,225 / 67,172 / did not converge / did not converge. 100k episodes take about 10 hours; case A about 30 minutes.
  - Table V (200 episodes, optimal 50): MAASA 49.75 ± 0.719, 50.0 ± 0.0, 50.0 ± 0.0, 49.92 ± 0.44; D2MAV-A 47.52 ± 2.21, 49.96 ± 0.28, 49.84 ± 0.578, 49.775 ± 0.689.
  - Table VI (case C, 1 / 3 / 5 models): MAASA LOS events 0 / 0 / 4; D2MAV-A 0 / 32 / 28 ("86% decrease" at five models, Sec. IV-B.3).
  - Table VII: at 3 to 6 min inter-arrival MAASA 50.0 vs D2MAV-A 49.84; equal at 3 to 8 and 3 to 10 min.
  - Table VIII: intent accuracy 92%, 92%, 91%, 89%. Table IX: Wasserstein-1 distance 0.02 to 0.03 vs 0.41 to 0.42 for a uniform baseline.
- **Limitations stated by the authors:** performance degrades as the number of models (heterogeneity) grows under the limited training budget (Sec. IV-B.3); top-1 accuracy is a poor metric for near-uniform distributions (Sec. IV-B.5); en-route structured airspace only, 3D left as an extension (Sec. V).
- **Relevance to KarmaSky:** **baseline** (source of the intent head, 3 × FC128, that our summarizer plans to include; note that Sharifi et al. do not describe an intent head). The paper already frames the setting as competing companies with proprietary models, but it measures safety only: no fairness between companies, no federation, no priority.

### 2.2 Sharifi et al. 2026 (v3): pointer

Full card in `../closest_work/SUMMARY.md`, section 2.1. File here: `Workdone/2605.01041v3.pdf` (main version).

### 2.3 Rezaee, Abdul Hamid and Ismail 2024: Federated MADDPG for UAV collision avoidance

- **Citation:** Mohammad Reza Rezaee, Nor Asilah Wati Abdul Hamid, Zurita Ismail. "Federated Multi-Agent Reinforcement Learning for UAV Collision Avoidance in Dense Smart City Environment." 2024 12th International Japan-Africa Conference on Electronics, Communications, and Computations (JAC-ECC), pp. 7 to 10, IEEE, 2024. DOI: https://doi.org/10.1109/JAC-ECC64419.2024.11061244
- **File:** `Feasibility_&_workdone/Federated_Multi-Agent_Reinforcement_Learning_for_UAV_Collision_Avoidance_in_Dense_Smart_City_Environment.pdf`. Note: the PDF text layer uses a shifted font encoding and drops digits; numbers below were read from the rendered pages.
- **Problem:** Collision avoidance for many drones in a dense urban area, where earlier MARL work handled few drones (Abstract, Sec. I).
- **Method:** Each agent has a local MADDPG model (actor on local knowledge, critic on global state). A global model is updated every 50 episodes and the local models are synchronized with it (Sec. IV-A, Algorithm 1). The aggregation rule is not stated.
- **Setting / scenario:** 96 UAVs in a 1 km² area, speeds 5 to 15 m/s, all at 100 m height (2D). Actions: none, 30° left, 30° right. Positive reward for collision-free navigation, negative for collisions or getting too close (no values given). Action every 5 s, 60 s episodes. Python on an Ubuntu server (Sec. IV-B).
- **Key results:** Fig. 3 shows total cumulative reward rising over about 10,000 episodes; Fig. 4 shows average total collisions falling (axis from 0.312 down to 0.305). No tables, no baselines, no seeds; the authors call these "initial findings" (Sec. IV-B).
- **Limitations stated by the authors:** scalability and communication overhead; heterogeneity of agents' compute and data; security of model updates and adversarial attacks; 2D only with a limited action space; future work on 3D, faster drones and obstacles (Sec. V, VI).
- **Relevance to KarmaSky:** **federation** (second example of federated MARL for drone collision avoidance, with the same 50-episode sync interval as Chen et al.). Shallow, as `05_READING_LIST.md` notes. One swarm, no operators, no fairness.

### 2.4 Samu, Yang and Poddar 2026: SAR deconfliction systematic review (GAP)

- **Citation:** Joel Samu, Chuyang Yang, Kush R. Poddar. "Optimization and Tactical Deconfliction for Drone Search-and-Rescue in Low-Altitude Airspace: A Systematic Literature Review." Drones 2026, 10, 596. DOI: https://doi.org/10.3390/drones10080596 (received 28 June 2026, published 3 August 2026; CC BY)
- **Files:** `Gap/drones-10-00596.pdf` (identical copy in `../General/`)
- **Problem:** Whether drone search-and-rescue (SAR) swarm algorithms address safe coexistence with crewed rescue aircraft and are validated realistically. RQ1 algorithm families, RQ2 tactical deconfliction and manned-unmanned teaming (MUM-T), RQ3 validation maturity (Sec. 1.5).
- **Method:** PRISMA 2020 systematic review of AIAA ARC, IEEE Xplore and Web of Science plus a supplementary Scopus search; 8-item quality appraisal by three reviewers (Sec. 2).
- **Setting / scenario:** 498 records → 85 duplicates removed → 413 screened → 116 sought → 115 retrieved → 34 included, plus 10 from the supplementary search: **44 studies (2022 to 2026)** (Sec. 3.1).
- **Key results:**
  - About 86% (38 of 44) validated only in idealized software simulation (Abstract, Sec. 3.7).
  - Only 6 of 44 address crewed-aircraft deconfliction at all, and 4 of those 6 are transfer evidence from non-SAR settings; deconfliction rests on procedural separation, shared telemetry or reactive maneuvers, not provable bounds (Sec. 3.6, Table 5).
  - "No reviewed SAR swarm algorithm provides formally assured separation" (Sec. 4.1).
  - Quality appraisal: 18 of 44 studies have operationally realistic scenarios; 12 of 44 address uncertainty, latency or degraded communications (Sec. 4.3).
  - DRL (PPO, SAC) and bio-inspired metaheuristics dominate; most models assume uncontested airspace and use implicit deconfliction through reward penalties (Sec. 3.6, 5).
- **Limitations stated by the authors:** three databases plus Scopus, English peer-reviewed only, no gray literature; strict SAR scope may have excluded general UTM, UAM and delivery collision-avoidance work (Sec. 4.4).
- **Relevance to KarmaSky:** **safety shield** (evidence that learned swarms rarely handle crewed aircraft or right-of-way explicitly, and that reward penalties alone give no separation guarantee; supports a hard shield and manned aircraft first). Domain is SAR, not delivery; no federation, no operator fairness.

### 2.5 Chen et al. code: Multi_UAV_Data_Harvesting (Model-aided FedQMIX)

- **Source:** https://github.com/Cirrick/Multi_UAV_Data_Harvesting (local copy in `Feasibility_&_workdone/Multi_UAV_Data_Harvesting-master/` and `.zip`)
- **License:** BSD 3-Clause License, Copyright (c) 2023, Jichao Chen (from the `LICENSE` file in the local copy). If we copy or adapt any of this code, we must keep the copyright notice and licence text.
- **What it contains (from its README and code):** implementation of the paper in `../closest_work/SUMMARY.md` section 2.5. `main.py` runs `fl_train` when `--federated=True`; `common/arguments.py` defaults: `aggregation_period=50`, `aggregation_method='average'`, `model_learning_period=1000`. QMIX and IQL in `policy/`, environment in `Libs/Environments/`, maps in `config/` (`RDM_link_status.npy` is 77 MB, `RBM_link_status.npy` 13 MB). README requirements: Python 3.7.15+, numpy 1.21.5+, torch 1.12.1+, matplotlib 3.5.3+, pyswarms 1.3.0+. QMIX/IQL code is credited to `starry-sky6688/marl-algorithms`.
- **Relevance to KarmaSky:** **federation** (reference for how a federation round is written, Member 3 task in `04_TEAM_ROLES_AND_TASKS.md`).
- **Not committed to our repository:** third-party code and large data files. Link above instead.

### 2.6 Chen et al. 2023 paper: pointer

Full card in `../closest_work/SUMMARY.md`, section 2.5. File here: `Feasibility_&_workdone/2306.02029v2.pdf`.

---

## 3. What these papers point to together

- **Feasibility is established.** Brittain and Wei (2022) show decentralized PPO with attention and intent learning keeps up to 50 aircraft separated even when agents follow different reward functions; Sharifi et al. show the same family of methods reaches an equilibrium between two companies with different drones in BlueSky.
- **Heterogeneity hurts, in two ways.** Brittain and Wei show heterogeneous objectives raise loss-of-separation events unless agents model intent (Table VI). Sharifi et al. show heterogeneous aircraft lead to unequal delays (closest_work card). Both papers come from the same group and neither tries to equalize outcomes.
- **Federation for drones exists but is thin and cooperative.** Chen et al. and Rezaee et al. both sync local models every 50 episodes; both assume one team; Rezaee et al. give no baselines or numbers beyond curves.
- **Safety with crewed aircraft is largely missing.** The SAR review finds only 6 of 44 studies handle crewed aircraft and none give provable separation.
- **Gap:** no paper here federates learning between rival operators, measures who contributed what, or turns contribution into priority, and none couples that with a hard safety layer that respects manned aircraft first.

## 4. Overlap risk

- **Brittain and Wei 2022: low to medium.** It already names "competing companies" with proprietary models as the motivation and handles heterogeneous objectives, so we cannot claim to be first to consider competing operators in MARL separation assurance. It does not federate, does not measure fairness, does not assign priority.
- **Sharifi et al.: high on the problem statement** (see closest_work summary).
- **Chen et al., Rezaee et al.: low.** Federated MARL for UAVs, but single team, no competition, no fairness, no contribution scoring.
- **SAR review: none.** Background evidence only.

## 5. What we use from here

- [FROM PAPER] Intent head: three 128-node FC layers and a 3-way softmax predicting each intruder's action distribution, trained with cross-entropy jointly with PPO (Brittain and Wei 2022, Sec. III-B, III-C, Fig. 2). This is the source of "intent head (3×FC128)" in `04_TEAM_ROLES_AND_TASKS.md`.
- [FROM PAPER] Candidate GAE values γ 0.99, λ 0.95 (Brittain and Wei 2022, Table I). Sharifi et al. do not print them; choice is [OPEN].
- [FROM PAPER] Model identifier in the observation so an agent knows which operator's policy an intruder follows (Brittain and Wei 2022, Sec. III-A.1). Whether to include it is [OPEN] (it may conflict with privacy fix 2).
- [FROM PAPER] Federation interval of 50 episodes and plain averaging as the F1 starting point (Chen et al., Sec. V; code default `aggregation_period=50`, `aggregation_method='average'`; Rezaee et al., Sec. IV-A).
- [FROM PAPER] Evidence that reward penalties alone do not guarantee separation from crewed aircraft, supporting the shield and the "manned aircraft first" rule (Samu et al., Sec. 3.6, 4.1).

## Could not read

None. All PDFs were read. The Rezaee et al. PDF has a broken text layer (shifted font encoding, digits missing); its numbers were read from rendered page images.
