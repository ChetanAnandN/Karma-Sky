# Safety_layer: Summary

## 1. What this folder is about

Methods that put a hard or probabilistic safety layer around a learning policy: logic-based shields for MARL, learned decentralized control barrier functions, an RL planner plus constrained-control safety filter for drones, and a survey of CBF-based safe RL. For KarmaSky this backs the safety shield (Member 4): a layer that removes unsafe actions before credits or the policy decide, with "manned aircraft first, then shield, then credits, then the AI's choice" (`00_START_HERE.md`, rule 4).

PDFs are not committed to the repository (public repo). Use the links in each card.

---

## 2. Paper cards

### 2.1 ElSayed-Aly et al. 2021: Safe Multi-Agent RL via Shielding

- **Citation:** Ingy ElSayed-Aly, Suda Bharadwaj, Christopher Amato, Rüdiger Ehlers, Ufuk Topcu, Lu Feng. "Safe Multi-Agent Reinforcement Learning via Shielding." Proc. of the 20th International Conference on Autonomous Agents and Multiagent Systems (AAMAS 2021), Online, May 3 to 7, 2021. arXiv:2101.11196v2 [cs.LG], 2 Feb 2021. Link: https://arxiv.org/abs/2101.11196
- **File:** `2101.11196v2.pdf`
- **Problem:** MARL has no safety guarantee during learning; safety is an emergent property of all agents together (Sec. 1).
- **Method:**
  - A shield is synthesized from a linear temporal logic (LTL) safety specification by solving a two-player safety game; it monitors actions and replaces unsafe ones (Sec. 3 to 5).
  - **Minimal interference:** correct a joint action only if it is unsafe, and change as few agents' actions as possible. Agents also receive a punishment reward for unsafe actions (Sec. 4).
  - **Centralized shield:** one shield over all joint actions; synthesis cost grows exponentially with the number of agents.
  - **Factored shields:** several shields, each covering a part of the state space; agents join and leave; on conflicts the default safe action is used (Sec. 5).
- **Setting / scenario:** Four 2-agent grid worlds (CQ-learning, independent Q-learning) and two 4-agent cooperative navigation tasks (MADDPG); 10 independent runs; shields synthesized within two minutes with the Slugs tool (Sec. 6).
- **Key results:**
  - Table 1 (evaluation after 1,000 training episodes; collisions on ISR / Pentagon / MIT / SUNY): IQL 20.30 / 11.60 / 0.00 / 72.60; CQ 0.40 / 0.20 / 0.90 / 0.30; CQ + centralized shield 0.00 on all; CQ + factored shield 0.00 on all. CQ + centralized shield had higher reward than unshielded CQ on three of four maps (e.g. ISR 93.85 vs 89.53).
  - Table 2 (collisions over 20,000 training episodes): MADDPG 207.20 (cross) and 14,419.20 (antipodal); MADDPG + factored shield 0.00 and 0.00.
  - Fig. 9: raising the collision penalty in the reward did not reach zero collisions and degraded the task; in two maps agents gave up reaching their targets.
  - Centralized shields could not be synthesized for more than two agents in the grid maps (Sec. 6).
- **Limitations stated by the authors:** centralized shielding does not scale; factored shielding can give less optimal policies (delay when switching shields); factorizations were designed by hand (Sec. 5, 7).
- **Relevance to KarmaSky:** **safety shield**. Directly supports our design: shield as an action filter (`allowed[drone_id] = [bool, bool, bool]`), minimal interference, penalty for blocked actions, and the evidence that reward penalties alone do not guarantee safety. Our per-pair / per-contest check is closer to factored shielding than to a single centralized shield.

### 2.2 Qin et al. 2021: Decentralized Neural Barrier Certificates

- **Citation:** Zengyi Qin, Kaiqing Zhang, Yuxiao Chen, Jingkai Chen, Chuchu Fan. "Learning Safe Multi-Agent Control with Decentralized Neural Barrier Certificates." Published as a conference paper at ICLR 2021. arXiv:2101.05436v4 [cs.MA], 17 Apr 2021. Link: https://arxiv.org/abs/2101.05436
- **File:** `2101.05436v4.pdf`
- **Problem:** Safe control for many agents avoiding each other and obstacles while reaching goals; hand-crafted CBFs are hard to build and centralized CBFs blow up with the number of agents (Sec. 1, 3.1).
- **Method:** Jointly learn each agent's controller and a decentralized control barrier function h_i(s_i, o_i) that depends only on local state and observation. Proposition 1: if every agent satisfies the decentralized CBF conditions, the whole system is safe without a central coordinator. Networks invariant to the number and order of neighbors. At test time, "spontaneous online policy refinement" adjusts the action by gradient steps to reduce CBF violations (Sec. 3, 4, Eq. 9).
- **Setting / scenario:** 2D ground robots (Navigation, Predator-Prey, Nested-Rings) and 3D drones (Maze, Tunnel); baselines MAMPS, PIC(-Safe), MADDPG(-Safe), and the planner S2M2 for drones; model-free RL baselines used 10^3 times more training data; 10 trials (Sec. 5).
- **Key results:** Figs. 4 and 5: with 32 agents the method keeps a high safety rate and reward while baselines degrade (values shown in figures only). Fig. 6: trained with 8 agents, tested with up to 1,024. One evaluation run with 32 agents takes 200 s, versus more than 70 hours estimated for a hand-crafted CBF-QP approach (7,000 steps at 36 s per step) (Sec. 5).
- **Limitations stated by the authors:** "our method still cannot guarantee that the agents are 100% safe", because the CBF conditions are enforced on training samples and may fail on unseen states (Sec. 5). Requires the system model.
- **Relevance to KarmaSky:** **safety shield** (alternative, learned design; shows decentralized per-agent safety conditions can give system-level safety). Its own limitation supports keeping a geometric, non-learned hard check for the 100 m / 500 m thresholds.

### 2.3 Safaoui et al. 2023: Filtered RL for safe multi-drone motion planning

- **Citation:** Sleiman Safaoui, Abraham P. Vinod, Ankush Chakrabarty, Rien Quirynen, Nobuyuki Yoshikawa, Stefano Di Cairano. "Safe multi-agent motion planning under uncertainty for drones using filtered reinforcement learning." arXiv:2311.00063v1 [cs.RO], 31 Oct 2023 (no venue printed). Link: https://arxiv.org/abs/2311.00063
- **File:** `2311.00063v1.pdf`
- **Problem:** Safe motion planning for several drones in a cluttered workspace with uncertain motion and sensing; RL planners treat safety as soft constraints (Abstract, Sec. I).
- **Method:** A single-agent RL policy proposes motion (reaches the target, ignores other agents). A constrained-control safety filter, a convex QP with chance constraints, corrects it to avoid obstacles and other agents with high probability while staying close to the RL reference; terminal constraints give recursive feasibility (Sec. III, Propositions 1 and 2).
- **Setting / scenario:** Hardware test with 6 quadrotors at a 0.1 s control period; simulation with 100 Monte-Carlo runs; scalability study from 2 to 24 agents (Sec. V).
- **Key results:**
  - Hardware: QP setup and solve averaged 0.05 s and stayed below 0.06 s; inter-agent clearances stayed positive (Figs. 5, 6).
  - Fig. 8: over a 100 × 100 grid of starts, the RL policy alone sometimes collides; RL + filter stays safe; for under 2% of starts the agent "loiters" (deadlock within 800 steps / 80 s) but stays safe.
  - Table I (100 Monte-Carlo runs): RL + filter with terminal constraints 99% success, completion time percentiles (206, 236, 401), minimum agent separation (0.31, 0.32, 0.36); without terminal constraints 92%; pure MPC without terminal constraints 55%; pure MPC with terminal constraints failed at control step 10.
  - Fig. 9: filter compute time grows only moderately from 2 to 24 agents.
- **Limitations stated by the authors:** safety holds with high probability, not certainty; deadlocks are possible; the filter is suboptimal and conservative compared with coordinated planning ("a trade-off between safety and performance"); future work on decentralized settings and nonlinear dynamics (Sec. V-B, V-C, VI).
- **Relevance to KarmaSky:** **safety shield**. Same architecture as ours (learned policy, then a filter that minimally changes its action). Warns about deadlocks: our "fallback slow down" rule and the shield intervention rate must be monitored.

### 2.4 Guerrier, Fouad and Beltrame 2024: Learning CBFs and their use in RL (survey)

- **Citation:** Maeva Guerrier, Hassan Fouad, Giovanni Beltrame. "Learning Control Barrier Functions and their application in Reinforcement Learning: A Survey." arXiv:2404.16879v1 [cs.LG], 22 Apr 2024. Link: https://arxiv.org/abs/2404.16879
- **File:** `2404.16879v1.pdf`
- **Problem:** RL lacks safety guarantees; control barrier functions (CBFs) can keep a system in a safe set, but building them needs domain knowledge, which motivates learning them from data (Abstract, Sec. I).
- **Method:** Literature survey of safe RL with soft and hard constraints, CBF-based safety filters, and ways to construct CBFs from data (expert demonstrations, refinement of hand-crafted CBFs, graph CBFs for multi-agent settings) (Sec. III, IV).
- **Setting / scenario:** Survey, no experiments.
- **Key results:**
  - Hard or probabilistic guarantees require a system model, known or learned, and are only as strong as that model (Sec. V-A).
  - Cited works report that adding a shield or CBF can improve both safety and convergence during training (Sec. V-B).
  - Challenges (Sec. V-C): most safe RL is built in simulation and certification during deployment is rare; external safety filters "can be arbitrarily conservative in a manner that does not match the conservativeness during training"; zero-shot generalization is seldom assessed.
- **Limitations stated by the authors:** a "short review" focused on CBF methods (Sec. VI).
- **Relevance to KarmaSky:** **safety shield** background; supports training with the shield active (so the policy experiences the same conservativeness it will see at evaluation) and reporting how often the shield intervenes.

---

## 3. What these papers point to together

- **Reward penalties are not enough.** ElSayed-Aly et al. (Fig. 9) and Safaoui et al. (Fig. 8) both show the learned policy alone still collides; a separate layer is needed. This matches Osipychev et al. and Samu et al. in other folders.
- **Filter the policy's action, minimally.** All three methods keep the learned action unless it is unsafe and change it as little as possible (minimal interference, minimum-deviation QP, online refinement).
- **Guarantees depend on models.** Logic shields give hard guarantees on an abstraction; CBF-based methods give hard or probabilistic guarantees only as good as the model; learned certificates (Qin et al.) are not 100% safe. The survey states this explicitly.
- **Costs of safety:** scalability (centralized shield synthesis), conservativeness and deadlocks (Safaoui et al.), and mismatch between training and deployment conservativeness (survey).
- **Gap for KarmaSky:** none of these combine a safety layer with *priority between operators*. Shields here treat all agents alike; nothing decides who yields based on earned credits, and nothing handles a manned aircraft as a higher class. (The TTR paper in `../closest_work/` is the only one with a priority-aware filter, and its priority is first-come-first-served.)

## 4. Overlap risk

- **Low.** These are generic safe-MARL and safe-RL methods. None involves competing operators, fairness, federation or credits. The shield is a borrowed building block (rule 2 in `00_START_HERE.md`) and must be presented as such.

## 5. What we use from here

- [FROM PAPER] Shield as an action filter with minimal interference: correct only unsafe actions, change as few agents' actions as possible (ElSayed-Aly et al., Sec. 4).
- [FROM PAPER] Penalty for actions the shield blocks, so the policy learns their cost (ElSayed-Aly et al., Sec. 4). Whether to add it to our reward is [OPEN] (rule 4: credits never enter the reward; this is a safety penalty, not a credit).
- [FROM PAPER] Evidence that increasing the collision penalty does not reach zero collisions and can make agents abandon their task (ElSayed-Aly et al., Fig. 9).
- [FROM PAPER] Local, per-neighborhood safety checks can give system-level safety (Qin et al., Proposition 1; ElSayed-Aly et al., factored shields). Supports a pairwise shield per contest.
- [FROM PAPER] Learned safety certificates are not 100% safe (Qin et al., Sec. 5): keep the shield geometric and rule-based.
- [FROM PAPER] Measure deadlocks ("loiter") and conservativeness, not only collisions (Safaoui et al., Sec. V-B, Table I). Adds to our shield intervention-rate metric.
- [FROM PAPER] Train with the shield in the loop so training and evaluation conservativeness match (Guerrier et al., Sec. V-C). Whether to do this from the start is [OPEN].

## Could not read

None. All 4 PDFs were read.
