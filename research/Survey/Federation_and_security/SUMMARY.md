# Federation_and_security: Summary

## 1. What this folder is about

Papers on how federated learning behaves when participants differ (heterogeneous environments or data) and when some participants cheat (poisoned model updates). For KarmaSky this backs the federation design (what to share, how to normalize, how to aggregate) and the integrity part (attacks A1/A2, defenses, the referee's exam).

PDFs are not committed to the repository (public repo). Use the links in each card.

---

## 2. Paper cards

### 2.1 Pang, Ni and Zhong 2025: Personalized Observation Normalization for FedRL

- **Citation:** Yiran Pang, Zhen Ni, Xiangnan Zhong. "Personalized Observation Normalization for Federated Reinforcement Learning in Simulation Environments with Heterogeneity." Accepted at the International Joint Conference on Neural Networks (IJCNN) 2025 (footnote); arXiv:2605.27385v1 [cs.LG], 10 Apr 2026. Link: https://arxiv.org/abs/2605.27385
- **File:** `2605.27385v1.pdf`
- **Problem:** In federated RL, agents whose environments have different transition dynamics see different input distributions; their weights end up at different scales and, under averaging, the larger-norm model overshadows the smaller one, biasing and slowing the global model (Sec. III-A, Fig. 2, Eq. 7 to 10).
- **Method:**
  - **PON:** each agent keeps a running mean and variance of its own observations (incremental update after Chan et al., Eq. 11 to 15) and normalizes locally; these statistics are **never shared** (Sec. III-B).
  - **FedRL-PPO:** FedAvg over both the policy and the value network (Eq. 5, 6; Sec. III-D).
  - They also test "shared ON" (averaging the normalization statistics across agents) and show it fails (Sec. III-C, Fig. 4, Fig. 6).
- **Setting / scenario:** MuJoCo HalfCheetah-v3, Ant-v3, Walker2d-v3 with different body morphologies per agent; 3 agents; MLP 2 × 64 Tanh; batch 64, lr 3 × 10^-4, γ 0.99; PyTorch and Tianshou; 5 seeds (Sec. IV-A).
- **Key results (Table I, best performance, mean ± sd over 3 agents and 5 runs; HalfCheetah / Ant / Walker2d):**
  - Independent PPO: 1923.08 ± 828.42 / 2168.26 ± 529.07 / 2304.43 ± 571.84.
  - FedRL-PPO: 2239.04 ± 1098.35 / 3370.11 ± 386.52 / 2931.00 ± 646.13.
  - FedRL-PPO with PON: 3938.03 ± 288.82 / 4354.00 ± 517.79 / 3532.11 ± 403.20.
  - Fig. 6: shared ON shows large fluctuations in training.
- **Limitations stated by the authors:** none listed explicitly; future work on adaptive loss reweighting and environment-specific policy components for large, variable real-world settings (Sec. V).
- **Relevance to KarmaSky:** **federation**. Fleets X and Y differ in speed, acceleration and sensing range, which is the heterogeneity studied here. Supports keeping per-company normalization statistics private (consistent with keeping the own-state encoder private, `06_DESIGN_UPDATES.md` Update 2). Also evidence that federated PPO can beat independent PPO under heterogeneity (in MuJoCo, not airspace).

### 2.2 Fang, Cao, Jia and Gong: Local Model Poisoning Attacks to Byzantine-Robust FL

- **Citation:** Minghong Fang, Xiaoyu Cao, Jinyuan Jia, Neil Zhenqiang Gong. "Local Model Poisoning Attacks to Byzantine-Robust Federated Learning." Iowa State University and Duke University. Venue and year are not printed in this preprint PDF (file name `sec20summer_fang_prepub.pdf`). TODO: confirm venue, year and link.
- **File:** `sec20summer_fang_prepub.pdf`
- **Problem:** "Byzantine-robust" aggregation rules (Krum, Bulyan, trimmed mean, median) claim to tolerate some malicious clients. Can an attacker who controls some clients and sends crafted model parameters still break the global model? The goal is untargeted: raise the test error; the authors note an attacker "may perform such attacks to its competitor's federated learning system" (Sec. 2.3).
- **Method:** Craft the compromised clients' local models by solving an optimization problem each round so the aggregated model moves as far as possible against the direction it would move without attack (Sec. 3). Partial knowledge (attacker sees only its own clients) and full knowledge; known and unknown aggregation rule. Two defenses generalized from data-poisoning defenses: **ERR** (remove local models with the largest negative impact on validation error) and **LFR** (largest negative impact on validation loss), plus their union (Sec. 5).
- **Setting / scenario:** MNIST, Fashion-MNIST, CH-MNIST, Breast Cancer Wisconsin; LR and DNN classifiers; 100 workers, 20 compromised by default; non-IID degree p = 0.5; 50 trials per experiment; validation set of 100 samples for the defenses (Sec. 4.1, 5).
- **Key results:**
  - Abstract: DNN on MNIST with Krum, error rate 0.11 → 0.75.
  - Sec. 4.2: LR on MNIST with Krum, partial-knowledge attack 0.14 → 0.72 (about 400% relative). Krum is less robust than trimmed mean and median in most cases; Gaussian noise and label flipping have limited effect.
  - Fig. 2, Fig. 3: error grows with the share of compromised workers and with the degree of non-IID.
  - Sec. 5, Table 6: LFR is equal to or better than ERR (trimmed mean + LFR 0.12 vs trimmed mean + ERR 0.21 when the attack targets trimmed mean); LFR fully defends trimmed mean in some cases, but Krum + LFR still goes 0.14 → 0.58 (314%). Defenses can also remove honest models and raise error.
- **Limitations stated by the authors:** untargeted attacks only; targeted poisoning and new defenses are future work (Sec. 7).
- **Relevance to KarmaSky:** **privacy/attacks** and **Shapley scoring**. The free-riding (A1) and exam-gaming (A2) attacks are local-model manipulations of this kind. ERR/LFR measure each participant's impact on a held-out validation set, which is close to our referee scoring each company's update on a secret exam suite. Caveat: their rules assume many clients (100); with 2 to 3 companies, "remove the c worst" or f < n/3 style rules do not transfer directly.

### 2.3 Mitra et al. 2026: Robust and personalized FL for aircraft-engine prognostics

- **Citation:** Chinmoy Mitra, Md. Mehedi Hasan Nipu, Mohammad Sakib Mahmood, Md. Rakibul Islam, M. F. Mridha. "Robust and Personalized Federated Learning for Aircraft-Engine Prognostics: Heterogeneity and Failure-Masking Poisoning on a Turbofan Benchmark." Preprint, arXiv:2608.04045v1 [cs.LG], 4 Aug 2026. Link: https://arxiv.org/abs/2608.04045
- **File:** `2608.04045v1.pdf`
- **Problem:** Aircraft operators that treat telemetry as "competitive intelligence" want to federate remaining-useful-life (RUL) models. Two separate problems: benign heterogeneity (honest operators with different fault modes) and adversarial heterogeneity (a compromised operator sends poisoned updates) (Abstract, Sec. 1).
- **Method:** Multi-task 1D CNN on NASA C-MAPSS. Benign remedies: FedRep (shared encoder, private per-client heads), FedCCFA (clustered personalization), FedProx, server-side reweighting. Attacks: five, including a physically motivated "failure-masking" sensor-value backdoor. Aggregators: four (FedAvg, trimmed mean, coordinate median, Krum). Also a stacked FedRep + Krum defense (Krum on shared-encoder deltas, private heads unchanged).
- **Setting / scenario:** primary federation of 4 clients on FD001 + FD003 (different fault modes); replications with 6 clients and on the harder FD002 + FD004; 5 seeds for key cells; paired Wilcoxon tests (Sec. 2 to 9, 11).
- **Key results (Sec. 11 and Table 21):**
  - Benign axis: FedRep closes 69.9% ± 6.4% of the local-to-centralized RMSE gap, FedCCFA 66.9% ± 6.6%, FedProx 21.0% ± 13.1%, reweighting 10.4% ± 6.9%.
  - Backdoor vs FedAvg: 94.9% ± 7.9% attack success while clean RMSE 16.86 ± 0.43 is statistically indistinguishable from the honest 16.59 ± 0.84 (paired Wilcoxon, p = 0.625). The triggered fault-head F1 drops from 0.891 to 0.093.
  - Krum cuts attack success to 6.4% ± 10.0% and is the only aggregator to survive 2-of-4 colluding attackers (RMSE 23.97 ± 9.92, while trimmed mean and coordinate median collapse to 84.03 ± 0.00).
  - FedRep alone gives no protection: honest clients' attack success 0.633 ± 0.320 vs attacker's own 0.616 ± 0.311, "because the poison acts on the shared representation rather than the private heads".
  - FedRep + Krum: honest-mean attack success 0.028 ± 0.024 (Abstract: 2.8%), about 2× lower than Krum alone, at a cost of +1.8 macro-RMSE (Sec. 10.4).
- **Limitations stated by the authors:** small client count (4) with results outside Krum's formal resilience regime; static, non-adaptive backdoor trigger, so no robustness claim against adaptive, defense-aware attackers (Sec. 10.3).
- **Relevance to KarmaSky:** **federation** and **privacy/attacks**. Closest setting in this folder to ours: rival operators, few clients, a shared encoder with private heads (FedRep is the same shape as our shared summarizer and private decider). Key warnings: (1) a poisoned shared part reaches every operator even if heads are private; (2) clean metrics can look normal while an attack succeeds, so attack success must be measured explicitly.

---

## 3. What these papers point to together

- **Heterogeneity needs personalization.** PON (keep normalization local) and FedRep (keep heads local) both find that sharing everything hurts when participants differ, and that keeping a private part restores most of the benefit. Both support the split into a shared summarizer and a private decider, and keeping the own-state side private.
- **Plain averaging is fragile against cheaters.** Fang et al. show even "robust" rules can be pushed far off; Mitra et al. show a backdoor can succeed against FedAvg with no visible change in clean accuracy.
- **Defenses work only in some cases.** Validation-based rejection (ERR/LFR) and Krum help in specific settings and fail in others; both papers say new or composed defenses are needed. Mitra et al. explicitly do not claim robustness against adaptive attackers.
- **Disagreement:** Fang et al. find Krum the least robust rule against their optimized untargeted attack; Mitra et al. find Krum the only rule that survives their coordinated backdoor with 4 clients. The attacks and client counts differ, so the "best aggregator" depends on the threat.
- **Gap left for KarmaSky:** none of these studies federated *multi-agent RL* between competing operators, none ties contribution to rewards or priority, and none measures fairness between participants. Mitra et al. use competing operators but for supervised prognostics.

## 4. Overlap risk

- **Mitra et al. (2608.04045): low to medium.** It already does federated learning between competing aircraft operators with personalization and Byzantine-robust aggregation, and frames telemetry as competitive. It is supervised RUL prediction, not MARL or airspace; no fairness, no contribution scoring, no priority.
- **Fang et al.: low.** Generic FL attacks and defenses.
- **Pang et al.: low.** Generic FedRL under heterogeneity (MuJoCo).
- None of these papers does our core idea (federation between competing operators for shared airspace, fairness between operators, contribution-earned priority).

## 5. What we use from here

- [FROM PAPER] Per-company running mean/variance observation normalization that is never shared (Pang et al., Sec. III-B). Whether to adopt it is [OPEN] (Member 2).
- [FROM PAPER] Evidence that sharing normalization statistics across heterogeneous agents destabilizes training (Pang et al., Sec. III-C, Fig. 6).
- [FROM PAPER] Shared encoder + private heads as the personalization pattern that works best under benign heterogeneity (Mitra et al., FedRep, Sec. 11). Matches our [PROPOSED] summarizer/decider split.
- [FROM PAPER] Measure attack success separately from clean performance; an attack can be invisible on clean metrics (Mitra et al., Sec. 11). Applies to our integrity metrics and to A1/A2.
- [FROM PAPER] Candidate robust aggregators for comparison: trimmed mean, coordinate median, Krum (Fang et al., Sec. 2.2; Mitra et al., Table 21). Whether any is used in F1/F2/F3 is [OPEN].
- [FROM PAPER] Validation-impact rejection (ERR/LFR) as a reference point for the referee's exam-based scoring and integrity check (Fang et al., Sec. 5).
- [FROM PAPER] A poisoned shared representation affects every participant even with private heads (Mitra et al., Sec. 11). Our shield and integrity check must not assume the private decider isolates a company from a bad merge.

## Could not read

None. All 3 PDFs were read.
