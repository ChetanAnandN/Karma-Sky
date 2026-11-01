# FAQ and Glossary

---

## Common confusions

**Q: Are there two separate AIs, one for flying and one for bidding?**
No. Each company has one brain with two parts (summarizer and decider). Bidding is a simple fixed rule, not AI. The shield is also a fixed rule.

**Q: If a drone loses a bid, does it stop using its brain?**
No. The brain always runs and gives scores for slow / hold / speed up. Losing a bid only removes options (for example "speed up"). The drone then picks the best remaining option by the brain's scores.

**Q: Why is the summary 64 numbers for the drone itself and 64 for traffic?**
The summarizer turns two kinds of input into fixed-size summaries: one about the drone's own state, one about all neighbors combined (attention squeezes any number of neighbors into 64 numbers). The decider reads both.

**Q: Are these new neural networks we invent?**
No. They are standard designs from Brittain and Wei and Sharifi. We reuse them. What is new is how they are shared between competitors and what we measure.

**Q: Does each drone have its own brain?**
Each drone runs a copy of its company's brain. All 10 drones of a company use the same brain (parameter sharing). In simulation it is literally one network processing 10 drones at once.

**Q: Do the drones learn while flying?**
In simulation, learning happens between episodes (Loop 2). In a real system, drones would only use a trained copy; learning would happen on company servers.

**Q: Why can't a company just buy credits?**
Then the richest company wins, which is the unfairness we are trying to fix. Credits are earned only by helping everyone's safety.

**Q: Why are credits not in the reward?**
If drones were rewarded for collecting credits, they might learn to take risks to earn them. Keeping credits out of the reward keeps the AI focused on safety and speed.

**Q: Can a company see another company's routes through federation?**
Possibly, if we are careless. See `06_DESIGN_UPDATES.md`, Update 2, for the fixes and the route-leakage test.

**Q: Is our contribution enough if all pieces exist already?**
The pieces exist; the combination, setting and questions are new: federation between competitors, fairness between operators measured with normalized delay, and priority earned by safety contribution. If federation does not reduce the gap, that is still a reportable finding. Read brief Section 10.

**Q: Why simulation only?**
It is the norm in this field (the Drones review found most studies are simulation-based), it is safe, and it allows thousands of repeat runs.

**Q: What if the baseline does not show unfairness?**
Stop and discuss with the mentor. The project depends on that result.

---

## Glossary

| Term | Meaning |
|---|---|
| Agent | One decision maker; here, one drone |
| Episode | One full simulated run, about 18 simulated minutes |
| Step | One decision moment, every 3 simulated seconds |
| Reward | Score the simulator gives after each step; the AI learns to get more of it |
| RL (reinforcement learning) | Training by trial and error with rewards |
| MARL | RL with many agents at once |
| PPO | Proximal Policy Optimization; a standard, stable RL training method |
| Actor-critic | A network with two outputs: action scores (actor) and an estimate of how good the situation is (critic) |
| GAE | A standard way to estimate how good each action was, used inside PPO |
| Neural network | A function with many adjustable numbers (weights) that is trained from data |
| Encoder / summarizer | The network part that turns raw inputs into a short summary |
| Decider / policy head | The network part that turns the summary into action scores |
| Attention | A layer that weighs neighbors by importance and combines any number of them |
| Intent prediction head | Extra output that guesses what neighbors will do next; helps learning |
| Parameter sharing | All drones of a company use one set of network weights |
| Federated learning | Several parties train a shared model by sending model updates, not data |
| FedAvg | Federated averaging: merge updates by averaging them |
| q-FFL | Fair federated learning: gives more weight to parties doing worse |
| Referee | Neutral server that merges updates, scores contribution and keeps credits |
| Shapley value | Game-theory method to split credit fairly among contributors |
| Exam suite | Secret set of hard crossing scenarios used to score updates |
| Karma credits | Non-tradable credits earned by contribution, spent for priority |
| Contest | Two drones of different companies predicted within 500 m within 60 s at a crossing |
| Giveback | Redistribution of spent credits from the pool |
| Cap | No company may hold more than 60% of all credits |
| Safety shield | Rule-based filter that removes unsafe actions |
| NMAC | Near mid-air collision: closer than 100 m |
| LoWC | Loss of well-clear: closer than 500 m |
| Normalized delay | (time in shared airspace − time flying alone) / time flying alone |
| Ft | Sharifi's fairness score: (1 − abs(TA − TB) / max) × 100 |
| Free riding | Sending useless updates but still getting credits |
| Exam gaming | Tuning updates to score well on the exam without real benefit |
| Gradient inversion | Attack that reconstructs training data from shared updates |
| Differential privacy | Adding controlled noise to hide individual data |
| BlueSky | Open-source air traffic simulator from TU Delft |
| BlueSky-Gym | RL environments built on BlueSky |
| PettingZoo | Standard Python interface for multi-agent environments |
| UTM | Unmanned Traffic Management, the system that would coordinate drones in real airspace |
| Digital Sky | India's drone regulation and UTM platform |
| Seed | Random starting number; different seeds give different runs, used to check results are not luck |
| Mann-Whitney U | Statistical test to compare two groups without assuming a normal distribution |
| Holm correction | Adjustment when running many tests so we do not find false "significant" results |
| Ablation | Removing one part to see how much it mattered |
