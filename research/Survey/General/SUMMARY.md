# General: Summary

## 1. What this folder is about

Surveys and reviews that give the wider picture: MARL for UAV control, AI for UAV deconfliction, MARL for truck-drone logistics, federated/cooperative/noncooperative MARL theory, and drone search-and-rescue deconfliction. For KarmaSky they provide background, confirm that the field is simulation-heavy, and show where fairness and incentives appear (or do not) in the literature. No experiments of their own except as noted.

**Duplicate:** `drones-10-00596.pdf` is identical to `../Core/Gap/drones-10-00596.pdf`; its full card is in `../Core/SUMMARY.md` (section 2.4).

PDFs are not committed to the repository (public repo). Use the links in each card.

---

## 2. Paper cards

### 2.1 Ekechi, Elfouly, Alouani and Khattab 2025: A Survey on UAV Control with MARL

- **Citation:** Chijioke C. Ekechi, Tarek Elfouly, Ali Alouani, Tamer Khattab. "A Survey on UAV Control with Multi-Agent Reinforcement Learning." Drones 2025, 9, 484. DOI: https://doi.org/10.3390/drones9070484 (published 9 July 2025; CC BY)
- **File:** `drones-09-00484.pdf`
- **Problem:** The MARL-for-UAV literature is fragmented across algorithms, architectures and metrics; the survey categorizes it and identifies gaps (Abstract, Sec. 1).
- **Method:** Collected peer-reviewed papers that apply MARL to UAV coordination, navigation, exploration, tracking and coverage; compared them on environment type, training scheme (centralized, decentralized, hybrid), swarm size, success rate, scalability, fault tolerance and convergence. Values read from text or approximated from graphs; scalability rated high/moderate/low (Sec. 1).
- **Setting / scenario:** Survey. Sections on value-based (DQN etc.), policy-based (DDPG, MATRPO, PPO) and multi-agent federated RL (Sec. 4 to 6).
- **Key results:**
  - Sec. 6, Table 5: federated MARL for UAVs (MAFRL) is studied mainly in wireless networking (trajectory design, edge computing, emergency communications, resource allocation). The compared studies use small swarms of 3 to 10 UAVs, mostly simulation only, and many depend on a central server. One cited work ([121]) targets fairness, but in users' data rates, not between operators.
  - Sec. 8, open problems: scalability to large swarms, real-time adaptation, turbulence, energy, transfer and generalization, and convergence under non-stationarity and the sim-to-real gap.
- **Limitations stated by the authors:** none for the survey itself.
- **Relevance to KarmaSky:** **federation** background (federated MARL for UAVs exists, but for networking tasks, small and central-server based) and evidence that convergence under non-stationarity is an open issue.

### 2.2 Chagas, Ruseno and Bechina 2025: AI Approaches for UAV Deconfliction

- **Citation:** Fabio Suim Chagas, Neno Ruseno, Aurilla Aurelie Arntzen Bechina. "Artificial Intelligence Approaches for UAV Deconfliction: A Comparative Review and Framework Proposal." Automation 2025, 6, 54. DOI: https://doi.org/10.3390/automation6040054 (published 11 October 2025; extended version of a CoDIT 2024 paper; SESAR AI4HyDrop project; CC BY)
- **File:** `automation-06-00054.pdf`
- **Problem:** Drone traffic is growing faster than regulation; separation between drones and manned aircraft needs better automated solutions at strategic and tactical levels (Abstract).
- **Method:** Keyword search (2020 to 2025, English), categorized into deep learning, reinforcement learning and bio-inspired learning; proposes a hybrid AI deconfliction framework for AI4HyDrop (Sec. 2, 3).
- **Setting / scenario:** Review. Fig. 2 counts 37 deep learning, 21 RL and 19 bio-inspired publications.
- **Key results:**
  - MARL (cited studies, Sec. 2.2.2, 3.1.2): graph-based MARL (DGN) reaches zero NMACs in 3- and 4-agent scenarios; mean-field graph RL scales to 120 UAVs; energy-aware MARL reaches over 80% mission success; a single-agent RL method improves mission success by 40.6% over rule-based tactics.
  - RL drawbacks: long training, complex reward shaping, heavy compute; validation mostly in Gazebo, AirSim or custom simulators; gap between simulated and operational performance; aviation needs explainable decisions (Sec. 3.2).
  - Conclusions: focus in the literature is tactical rather than strategic; fairness, explainability, transparency and privacy named as ethical considerations still to address (Sec. 4).
- **Limitations stated by the authors:** uneven evidence base across categories; most studies use custom or limited datasets and simulation (Sec. 3.2). (Note: Sec. 4 calls RL "the most applied" while Fig. 2 counts more deep learning than RL publications; the paper does not explain this.)
- **Relevance to KarmaSky:** background on deconfliction methods; supports **safety shield** (RL alone needs safe validation) and shows fairness is only raised as an ethical point, not studied.

### 2.3 Arishi and Ahuja 2025: MARL for truck-drone routing review

- **Citation:** Ali Arishi, Paras Ahuja. "Multi-Agent Reinforcement Learning for truck-drone routing in smart logistics: A comprehensive review." Computers and Electrical Engineering 127 (2025) 110529. DOI: https://doi.org/10.1016/j.compeleceng.2025.110529
- **File:** `1-s2.0-S0045790625004720-main.pdf`
- **Problem:** Classical vehicle routing struggles with dynamic last-mile truck-drone delivery; how is MARL used there? (Abstract, Sec. 1)
- **Method:** Narrative review with a taxonomy by learning strategy (value-based, policy-based, hybrid, meta-RL), optimization objective and real-world constraint; comparison tables (Tables 1 to 12). No search protocol or study count is printed.
- **Setting / scenario:** Review.
- **Key results:** MARL is reported to outperform heuristics on delivery efficiency, energy and route adaptability (Sec. 7). Challenges (Sec. 6.2): computational scalability, real-time coordination, regulatory and safety compliance (airspace laws, no-fly zones), energy, infrastructure and adversarial robustness (reward hacking, sensor spoofing). Percentages in Sec. 6.2 are taken from cited studies, not measured by the authors. Future directions include federated learning for decentralized policy updates, graph-based and hierarchical MARL, edge computing and explainability (Sec. 6, 7).
- **Limitations stated by the authors:** none for the review itself.
- **Relevance to KarmaSky:** context only (delivery logistics layer); federated MARL appears only as a future direction. Airspace conflicts between operators are not a focus.

### 2.4 Cheruiyot et al. 2025: Survey of federated, cooperative and noncooperative MARL

- **Citation:** Kemboi Cheruiyot, Nickson Kiprotich, Vyacheslav Kungurtsev, Kennedy Mugo, Vivian Mwirigi, Marvin Ngesa. "A Survey of Multi Agent Reinforcement Learning: Federated Learning and Cooperative and Noncooperative Decentralized Regimes." arXiv:2507.06278v1 [cs.MA], 8 Jul 2025. Link: https://arxiv.org/abs/2507.06278
- **File:** `2507.06278v1.pdf`
- **Problem:** Unify three regimes of multi-agent learning: federated RL (central coordination), decentralized cooperative MARL (peer-to-peer), and noncooperative MARL (self-interested agents) (Abstract, Sec. 1).
- **Method:** Formal survey of formulations, algorithms and theoretical guarantees (Sec. 3 to 5).
- **Setting / scenario:** Survey, no experiments.
- **Key results:**
  - Federated RL (Sec. 3.7, 3.9): averaging methods QAvg and PAvg (Jin et al. 2022) converge to suboptimal policies, with a gap that grows with the difference in transition dynamics between environments; personalized variants share everything except embedding layers.
  - Privacy and incentives (Sec. 3.12): adversaries "might still infer environment properties from the aggregated models"; differential privacy may worsen suboptimality; cross-silo settings (few, capable participants) differ from cross-device; "In open federated systems with self-interested agents, participation may be limited if collaboration offers minimal local benefits", and economic mechanisms could address this.
  - Noncooperative MARL (Sec. 5.6, 5.8): non-stationarity, Nash equilibria that are PPAD-complete to compute, possible cycling; opponent modeling and mean-field methods as responses.
- **Limitations stated by the authors:** none for the survey itself; open problems listed per section.
- **Relevance to KarmaSky:** **federation** (heterogeneity makes plain averaging suboptimal), **privacy/attacks** (inference from merged models, DP trade-off: supports route-leakage test P0/P1 and the DP option), **karma/credits** (incentive design for self-interested participants is named as an open need). Our setting is cross-silo with 2 to 3 operators.

### 2.5 Samu, Yang and Poddar 2026: SAR deconfliction review (pointer)

Full card in `../Core/SUMMARY.md`, section 2.4. File here: `drones-10-00596.pdf`.

---

## 3. What these papers point to together

- **The field is simulation-heavy.** Every review notes a gap between simulated results and real operations (Chagas et al. Sec. 3.2; Ekechi et al. Sec. 8; Samu et al. 86% simulation-only). Simulation-only work, like ours, is normal but must say so.
- **Federated MARL is a recognized direction but still small-scale.** Ekechi et al. find federated MARL for UAVs mostly in networking tasks with 3 to 10 UAVs; Arishi and Ahuja list it as future work; Cheruiyot et al. show averaging is suboptimal under heterogeneity.
- **Fairness and incentives are mentioned but not studied in airspace.** Chagas et al. list fairness as an ethical consideration; Cheruiyot et al. say self-interested participants need incentives; the only fairness study in Ekechi et al. concerns communication data rates. None looks at fairness between operators sharing airspace.
- **Safety with manned aircraft is rarely handled** (Samu et al.; Chagas et al. emphasize separation from manned aircraft as the motivating concern).
- **Gap for KarmaSky:** fairness between competing operators in shared airspace, and incentive-compatible federation (contribution-earned priority), are open in these reviews.

## 4. Overlap risk

- **None of these reviews describes work that already does our core idea.** The closest statement is Cheruiyot et al. calling for economic mechanisms to motivate self-interested participants in federated RL; it is a direction, not an implementation. Caveat: reviews only cover what their search found (for example, Samu et al. excluded general UTM and delivery work).

## 5. What we use from here

- [FROM PAPER] Framing: averaging across heterogeneous environments converges to a suboptimal policy whose gap grows with dynamics divergence (Cheruiyot et al., Sec. 3.9, citing Jin et al. 2022). Supports reporting "federation may not help" as a valid result.
- [FROM PAPER] Framing: in open federated systems with self-interested agents, participation needs incentives (Cheruiyot et al., Sec. 3.12). Motivation for karma credits.
- [FROM PAPER] Framing: aggregated models may leak environment properties, and DP trades privacy for utility (Cheruiyot et al., Sec. 3.12). Motivation for the route-leakage test and the DP option.
- [FROM PAPER] Reporting practice: state simulation-only scope and validation level clearly (Samu et al., Sec. 4.5.2, Table A3 checklist; Chagas et al., Sec. 3.2).

## Could not read

None. All PDFs were read.
