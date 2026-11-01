# KarmaSky in Plain Words

No AI or ML background needed. Technical terms are explained the first time they appear, and all are in `08_FAQ_AND_GLOSSARY.md`.

---

## 1. The situation

Picture a city suburb (we use Frisco, near Dallas, because a published study already modeled it). Two delivery companies, call them **Company X** and **Company Y**, each fly 10 drones along 4 fixed routes about 10 km long. The routes **merge** at two points and **cross** at one intersection. Drones from both companies meet there.

- **Company X** has strong drones: faster (about 44.9 m/s top speed), better acceleration, sees farther (1000 m sensing). **[FROM PAPER: Sharifi et al. 2026]**
- **Company Y** has weaker drones: slower (about 30.1 m/s), weaker acceleration, sees less far (750 m). **[FROM PAPER]**

Each drone can only do three things every 3 seconds: **slow down, hold speed, or speed up**. That is enough to avoid each other at merges and crossings.

Two safety distances matter:
- **Near miss (NMAC):** two drones closer than 100 m. Very bad.
- **Loss of well-clear (LoWC):** closer than 500 m. A warning sign.

---

## 2. What has already been done by others

**Reinforcement learning (RL)** is a way of training an AI by trial and error. The AI tries actions in a simulator, gets a score (reward) for good outcomes and a penalty for bad ones, and slowly learns what works. **Multi-agent RL (MARL)** is the same with many AIs (here, many drones) learning at once.

- **Brittain and Wei (2022)** trained drones with MARL to keep safe distances in busy airspace. They added a trick where each drone learns to **predict what neighbors will do next** (intent prediction). **[FROM PAPER]**
- **Sharifi et al. (2026)** did this with **two companies with different drones**. Key finding: the weaker company ends up **yielding more and being delayed more**. They proposed a fairness score but did not try to fix the unfairness. **[FROM PAPER]**
- **Chen et al. (2023)** and **Rezaee et al. (2024)** used **federated learning** for drones: several learners improve a shared AI by sending model updates, not raw data. But in their work, all drones belong to one team. Nobody is competing. **[FROM PAPER]**
- **CARMA (Elokda et al.)** used **karma credits** for fair road traffic: you earn credits by yielding, spend them for priority, and you cannot buy them with money. Never used for airspace. **[FROM PAPER]**

---

## 3. The gap (what nobody has done)

1. Federated learning between **competing** drone companies, where each company has its own interests.
2. Measuring **fairness between companies** in that shared learning.
3. Giving **priority based on how much a company helped** everyone's safety, instead of based on who has bigger, faster drones.
4. Making sure this priority system **cannot be gamed** and **never reduces safety**.

---

## 4. What we build

### Piece 1: Each company has its own AI "brain" with two parts
- **Summarizer (shared part):** looks at the drone's own state and nearby drones and turns it into a short summary (a list of 64 numbers, a "fingerprint" of the situation). This part is shared and improved together.
- **Decider (private part):** reads the summary and picks slow down, hold, or speed up. This part stays private to each company, because it is the company's own strategy.

One brain per company, copied into all 10 of its drones. Every drone runs the same brain on its own view of the sky.

### Piece 2: Shared learning (federation)
Every 50 practice episodes (one episode is about 18 simulated minutes of flying), each company sends **only the changes to its summarizer** to a neutral **referee**. The referee merges them and sends back an improved summarizer. Raw flight logs never leave the company.

### Piece 3: Contribution scoring
Before merging, the referee checks how much each company's update helps. It runs a **secret exam**: a set of hard crossing situations that companies have not seen. It measures how much each update reduces near misses and warnings. The scoring method is called a **Shapley value**, a fair way to split credit among contributors from game theory.

### Piece 4: Karma credits
- Companies get credits in proportion to their contribution score.
- When two drones from different companies are about to meet at a crossing (within 500 m within 60 s), each company can **bid credits**. The higher bid gets priority; the other drone yields.
- The winner pays. Paid credits go into a pool and are given back, so credits do not pile up with one company. No company may hold more than 60% of all credits.
- Credits **cannot be bought** and are **not part of the AI's training reward**. They only affect who goes first.

### Piece 5: Safety shield
A simple rule-based checker, not AI. It looks 30 seconds ahead at worst-case movements and **removes any action** that would break 100 m from another drone or 500 m from a manned helicopter. If no action is safe, the drone slows down.

**Priority order, always:** manned aircraft > safety shield > credit result > AI's choice.

### Piece 6: Integrity (anti-cheating)
Companies might try to cheat: send useless updates and still earn credits (free riding), tune updates to pass the exam but not help in reality (exam gaming), or send harmful updates to slow a rival (stretch goal). Defenses: rotate the secret exam, compare updates for suspicious similarity, smooth scores over time, cap credits, and check updates on a hidden second exam.

---

## 5. How we know if it worked

We compare many setups in simulation:
- Each company learns alone (no sharing)
- One central AI for everyone (an upper-bound reference)
- Simple fixed rules (no AI)
- Shared learning with three merging rules: equal, fairness-weighted, contribution-weighted
- Shared learning plus karma credits, with and without the giveback and cap
- Karma credits under cheating attacks

We measure:
- **Safety:** number of near misses and warnings
- **Efficiency:** how long deliveries take
- **Fairness:** the gap between companies. Our main fairness measure is **normalized delay**: how much slower a company's drones are in shared airspace compared to flying alone. Comparing to "flying alone" is fair because Company Y's drones are slower even with an empty sky.

**Success looks like:** the delay gap between X and Y shrinks, near misses do not increase, and cheating does not pay. **If the delay gap does not shrink, that is still a valid finding we report honestly.**

---

## 6. Why this is worth doing

- Drone delivery is growing, and airspace will be shared by competitors. Regulators (in India, the Digital Sky platform; elsewhere, UTM providers) will need fair rules.
- Today, priority goes to whoever has better hardware. We test whether priority can be earned by helping safety instead.
- This is a SDG 9 project: fair, safe shared infrastructure.

## 7. What this project is not

- Not physical drones. Simulation only, which is normal in this research area.
- Not a product ready for certification.
- Not inventing RL, federated learning, karma, Shapley values or shields. We combine them in a new setting and answer new questions.
