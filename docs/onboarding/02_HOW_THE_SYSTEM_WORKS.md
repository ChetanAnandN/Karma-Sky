# How the System Works: The 4 Loops

Everything in KarmaSky runs as **four loops running at different speeds**, like gears of different sizes.

| Loop | How often | What happens | Who runs it |
|---|---|---|---|
| Loop 1: Fly | Every 3 seconds (simulated) | Each drone decides slow / hold / speed up | Each drone (company's brain) |
| Loop 2: Learn | After each episode (~18 sim minutes) | Each company improves its own brain from its private diary | Each company privately |
| Loop 3: Share | Every 50 episodes | Referee scores and merges summarizer updates, mints credits | Referee |
| Loop 4: Credits | Continuously, with each bid | Credits are spent, pooled, given back, capped | Referee's credit ledger |

All settings below are **[PROPOSED]** unless tagged **[FROM PAPER]**.

---

## The brain (one per company)

```
  Own drone state ─┐
                   ├─> SUMMARIZER (shared, federated) ──> 64 numbers about self
  Nearby drones ───┘                                 ──> 64 numbers about traffic (attention picks who matters)
                                                     ──> intent guesses for neighbors
                                       │
                                       v
                          DECIDER (private, per company) ──> scores for slow / hold / speed up
```

- **Two neural networks**, both standard designs from prior work (PPO actor-critic with attention, from Brittain and Wei; Sharifi). **[FOR REVIEW]**
- **Attention** lets the drone handle any number of neighbors by focusing on the ones that matter most.
- **Parameter sharing:** all 10 drones of one company use the same brain. On a computer, all 10 are processed in one batch.
- Rough size: about 90 to 100 thousand numbers in total (well under 1 MB). This is our rough estimate, to be confirmed when built.

---

## Loop 1: one drone, one decision (every 3 s)

Order of steps (**updated**, see `06_DESIGN_UPDATES.md`):

1. **Look.** Read own position, speed, distance to goal, and nearby drones (up to sensing range: X 1000 m, Y 750 m). Only relative positions are used.
2. **Bid.** If a drone from another company is on course to come within 500 m within 60 s at a crossing, a contest is opened. Each company's fixed bidding rule offers credits. The referee picks the winner. Result: "you have priority" or "you must yield".
3. **Think.** The brain produces scores for slow / hold / speed up. The brain always runs, every step.
4. **Check.** Remove options, in this order:
   - Manned helicopter rule: remove anything that breaks 500 m from the helicopter.
   - Shield: remove anything that, in the 30 s worst case, breaks 100 m from another drone.
   - Bid result: if this drone must yield, remove "speed up" (and "hold" if needed).
   - If nothing is left: slow down (fallback).
5. **Act.** Pick the highest-scoring option that is still allowed.
6. **Score.** The simulator moves everything 3 s forward. The drone gets a reward: penalties for near misses and warnings, a small cost for time, a bonus for reaching the goal. Credits are **never** part of the reward.

Key idea: **the brain decides, the bid and shield only remove options.** They never pick a new action themselves.

---

## Loop 2: learning from the diary (every episode)

1. During the episode each drone writes a diary: what it saw, what it did, what reward it got.
2. After the episode, the company uses the diary to update both parts of its brain with **PPO** (a standard RL training method that makes small, safe steps).
3. Training settings from Sharifi **[FROM PAPER]**: learning rate 1e-4, entropy 1e-3, clip 0.2, batch 512, 8 epochs, Adam optimizer, GAE.
4. The diary stays with the company. It is never sent anywhere.

---

## Loop 3: sharing through the referee (every 50 episodes)

1. Each company sends **only the changes to its shared summarizer parts** (not the decider, not the diary). See privacy updates in `06_DESIGN_UPDATES.md`.
2. **Integrity check:** the referee compares updates (cosine similarity) to spot copies or junk.
3. **Grading:** the referee runs the secret hard-crossing exam with each combination of updates and computes Shapley contribution scores. Utility = reduction in near misses + 0.1 × reduction in warnings. Scores are smoothed: new score = 0.8 × old + 0.2 × this round.
4. **Merge** using one of three rules:
   - F1: equal average (FedAvg)
   - F2: fairness-weighted (give more weight to the company that is worse off, idea from q-FFL)
   - F3: contribution-weighted (weight by Shapley score)
5. **Mint credits** in proportion to contribution.
6. **Send back** the merged summarizer. Each company plugs it into its brain and keeps its own private decider.

---

## Loop 4: the credit cycle

1. **Spend:** at each contest, the winner pays its bid.
2. **Pool:** paid credits go into a pool.
3. **Give back:** the pool is redistributed (uniform or need-based, **[OPEN]**).
4. **Cap:** no company can hold more than 60% of all credits.
5. **Earn:** new credits come from contribution in Loop 3.

Without giveback and cap (setup K1), one company may hoard credits. With them (K2), credits keep circulating. Comparing K1 and K2 is one of our experiments.

---

## Where things live

**In our simulation:** everything runs on one computer. Each company is a Python object with its own brain and diary. The referee is another Python object. Federation is a function call.

**In a real deployment (vision only, not built):**
- A trained copy of the brain runs on each drone. No learning in flight.
- Company servers retrain from flight logs.
- The referee would be the UTM provider (Digital Sky in India).
- Bids go over a data link. If the link is lost, the drone assumes it lost the bid and yields.
- Not solved here: certification, a real bidding system, the gap between simulation and reality.
