# KarmaSky: Architecture Explained in Detail

**Project:** SDG 9 main semester project (federated multi-agent RL for fair drone delivery)
**Status as of 2026-10-15:** Design stage. Nothing built yet. Mentor approval pending.
**Everything runs in simulation. No physical drones.**

This document explains the system in plain language first, then adds the technical details the team needs to build it. You do not need an AI background to follow it.

---

## How to read this document

| Tag | Meaning |
|---|---|
| **[FROM PAPER]** | Taken from a paper we read. Source named. |
| **[PROPOSED]** | Our design choice. Agreed in discussion, not yet tested or approved by the mentor. |
| **[OPEN]** | Not decided yet. |

All numbers in **examples** are made up to illustrate. Numbers in **settings** are either from papers or starting values to be tuned.

---

## Table of contents

1. The big picture
2. Key ideas in plain words
3. View 1: How the system behaves (the 4 loops)
   - Loop 1: one moment (every 3 s)
   - Loop 2: one practice run
   - Loop 3: the sharing round (every 50 runs)
   - Loop 4: the credit cycle
4. The drone's brain in detail
5. The safety shield and the helicopter
6. Catching cheaters
7. View 2: What the parts are (components)
8. What data goes where (privacy map)
9. All settings in one place
10. Known risks in the architecture
11. Open decisions
12. Common confusions, answered
13. References

---

## 1. The big picture

Two delivery companies (A and B) fly drones in the same simulated sky over a suburb of Dallas, Texas. Company A's drones are faster; Company B's are slower. Sometimes an ambulance helicopter flies through.

Each company's drones learn to fly safely and efficiently by practice. The companies also **share what they learn about traffic** through a neutral referee, without revealing their secrets. Companies that share more useful lessons earn **credits**, which let their drones go first at busy crossings. Spent credits are recycled so no company can hog priority forever. A **safety shield** and **helicopter priority** always override everything.

```
┌──────────────────────── BlueSky simulator (one shared sky) ─────────────────────────┐
│   Company A drones (fast)      Company B drones (slow)      Scripted helicopter      │
└───────────────▲──────────────────────────▲──────────────────────────────────────────┘
                │ what each drone sees / what each drone does
        ┌───────┴────────┐         ┌───────┴────────┐
        │ Company A      │         │ Company B      │   each: own network, own diary,
        │ summarizer     │         │ summarizer     │   own private decider
        │ decider (priv) │         │ decider (priv) │
        └───────┬────────┘         └───────┬────────┘
                │ summarizer changes only (every 50 runs)
        ┌───────▼──────────────────────────▼────────┐
        │ Referee                                    │
        │  checks, secret exam grading, merging,     │
        │  credit ledger (wallets, pool, cap)        │
        └────────────────────────────────────────────┘

Every step, before a drone moves:
  brain's preferences → credit check (may remove "speed up") → safety check (removes unsafe) → act
```

---

## 2. Key ideas in plain words

| Term | Plain meaning |
|---|---|
| **Neural network ("brain")** | A big calculator with thousands of adjustable knobs. Numbers go in (what the drone sees), numbers come out (how much it likes each choice). Practice tunes the knobs. |
| **Layer** | One round of "multiply, add, keep the positive part" inside the calculator. |
| **64 units** | That layer produces 64 numbers: a compact summary of the situation. |
| **Knobs (weights)** | The adjustable values inside the network. Learning = adjusting knobs. |
| **Episode / practice run** | One full delivery run, start to finish. |
| **Reinforcement learning** | Learning by trial and error from scores, like a learner driver. |
| **PPO** | The specific "review and improve" method. It improves habits in small, careful steps. |
| **Attention** | Focusing on the neighbors that matter most and blending them into one summary. |
| **Federated learning** | Learning together by sharing changes to the network, not raw data. |
| **Shapley value** | A fair way to split credit for an improvement among contributors, from game theory. |
| **Karma credits** | Tokens earned for helping, spent to go first, then recycled. Idea from road traffic (CARMA). |
| **Shield** | A fixed safety rule-checker that blocks unsafe moves. Not learned. |
| **NMAC** | Near mid-air collision: closer than 100 m. |
| **LoWC** | Loss of well clear: closer than 500 m. |

---

## 3. View 1: How the system behaves (the 4 loops)

The system runs as four nested loops, from fastest to slowest:

| Loop | How often | What happens |
|---|---|---|
| 1 | Every 3 seconds (simulated) | Each drone looks, thinks, gets checked, moves, gets scored |
| 2 | Every practice run (up to 18 min simulated) | Drones fly a full run; each company learns from its own diary |
| 3 | Every 50 runs | Companies share summarizer changes; referee checks, grades, merges, hands out credits |
| 4 | Every period (once per sharing round, to tune) | Spent credits are recycled; cap is enforced |

Running example used throughout: **drone A3** (Company A) and **drone B7** (Company B) both approaching crossing WP9, with the helicopter **H** nearby.

---

### Loop 1: one moment (every 3 seconds)

Every drone does five stages, every 3 seconds.

#### Stage 1: Look
The drone collects facts as numbers.

**About itself (4 numbers)** [FROM PAPER: Sharifi et al. 2026]:
- distance to next waypoint
- speed
- direction (heading)
- acceleration

**About each nearby aircraft** within sensing range (1000 m for Company A, 750 m for Company B) [FROM PAPER: Sharifi et al.]:
- the same 4 facts, plus distance from the drone

**Extra facts we add** [PROPOSED]:
- same company or other company
- that drone's current credit bid
- manned-aircraft flag (is it the helicopter?)

Example:

| Who | Distance to waypoint | Speed | Direction | Accel. | Distance from A3 | Other company? | Bid | Manned? |
|---|---|---|---|---|---|---|---|---|
| A3 (self) | 400 m | 30 m/s | 90° | 0 | | | | |
| B7 | 350 m | 20 m/s | 180° | 0 | 600 m | yes | 4 | no |
| H | | 40 m/s | 45° | 0 | 900 m | yes | none | yes |

Numbers are scaled to small values before entering the network so no single fact dominates.

The number of neighbors changes every step (could be 0, could be 8). The network handles this with attention (Stage 2).

#### Stage 2: Think (the network)
Each company has **one network made of two parts** (details in Section 4):

1. **Summarizer (shared with other companies):**
   - turns the drone's 4 facts into a **64-number self-summary**
   - turns each neighbor into a **64-number neighbor summary**
   - guesses each neighbor's next move (slow / keep / speed up)
   - blends all neighbors into one **64-number traffic summary**, giving more weight to the ones that matter (attention)
2. **Decider (private to the company):**
   - joins self (64) + traffic (64) = 128 numbers
   - outputs **preferences** for the 3 choices, e.g. slow 10%, keep 30%, speed up 60%
   - also outputs one **expectation** number ("how well is this going for me?"), used only for learning in Loop 2

**The network always produces a decision.** Nothing that follows can add or force a choice.

#### Stage 3: Check
Two checkers can only **cross options off**, in this fixed order:

1. **Credit check** (only when two drones from different companies are in a predicted conflict at a merge or crossing: within 500 m within the next 60 s, to tune) [PROPOSED]:
   - both companies offer credits; higher offer goes first and pays; tie goes to the drone closer to the crossing
   - **won:** nothing removed
   - **lost:** "speed up" removed (the drone must yield)
   - **no conflict:** no bid, nothing removed
2. **Safety check** (always, every step) [PROPOSED]:
   - removes any option that could bring the drone within 100 m of a drone or 500 m of the helicopter (details in Section 5)
   - applies **even if the drone won the bid**
3. **Fallback:** if every option was removed, the drone slows down.

Examples (brain says slow 10%, keep 30%, speed up 60%):

| Situation | Options left | Likely choice |
|---|---|---|
| No conflict, nothing unsafe | slow, keep, speed up | speed up |
| Lost the bid | slow, keep | keep |
| Won the bid, but speeding up is unsafe | slow, keep | keep (safety beats the bid) |
| Everything unsafe | none | slow down (fallback) |

**Rule to remember:** the brain proposes; the bid and safety checks can only say "not that one."

#### Stage 4: Act
The remaining preferences are rescaled to add to 100%, a choice is picked, and BlueSky moves every aircraft forward 3 seconds.

#### Stage 5: Score
Each drone gets a score for this step [FROM PAPER: Sharifi et al. reward, 5 parts]:
- **penalty for getting too close:** −1 if under 100 m; a smaller, scaled penalty between 100 and 500 m
- **penalty for unsafe speeds** (too close to its minimum or maximum)
- **small penalty for changing action**, which discourages jerky flying
- **bonus for completing the delivery**
- **small penalty every step**, which encourages finishing quickly

**Credits never count in the score** [PROPOSED]. Otherwise drones might learn to chase credits instead of flying well.

**Loop 1 in one line:** look, summarize, decide, get checked, move, get scored.

---

### Loop 2: one practice run (episode)

#### Part A: Fly the run
1. All 20 drones (10 per company) start at their hubs at slightly random times: 35 + 5k seconds, k random from 0 to 10 [FROM PAPER: Sharifi et al.]. This makes every run a bit different.
2. Loop 1 repeats every 3 seconds, about 240 steps for a 12-minute run.
3. The run ends when every drone has delivered, got too close (and been removed), or run out of time (18 min).

#### Part B: Keep a private diary
For each of its drones at each step, a company records **what the drone saw, what it did, and its score**. Company A records only A's drones. **No company sees another's diary.**

#### Part C: Review and improve
After the run, each company reviews its own diary:

1. **Better or worse than expected?** For each move, compare the drone's expectation number with what actually happened next.

   | Moment | Expected | What happened | Verdict |
   |---|---|---|---|
   | Sped up near B7 | going fine | got too close | worse than expected |
   | Slowed for the helicopter | a bit bad | passed safely, on time | better than expected |

2. **Adjust knobs:** better-than-expected moves become more likely in similar situations; worse ones become less likely. The expectation number is corrected too.
3. **Small, careful steps:** PPO limits how much habits can change per review (clip 0.2), so one unlucky run cannot make drones reckless.
4. **Several passes:** the diary is reviewed 8 times in batches of 512 moments [FROM PAPER: Sharifi et al.].
5. **Fix neighbor guesses:** compare guessed next moves with what neighbors actually did; correct the guessing part [FROM PAPER: Brittain and Wei 2022].

**Both parts of the network change** (summarizer and decider), using only the company's own diary. So between sharing rounds, A's and B's summarizers slowly drift apart.

#### Over many runs
| After | Typical behavior |
|---|---|
| Run 1 | Random knobs; erratic flying; many near-misses |
| A few hundred runs | Drones start slowing near crossings |
| Thousands of runs | Smooth, safe, efficient crossings |

Sharifi et al. trained for 2,500 runs per setup, which took more than 7 hours on an RTX 3090 [FROM PAPER].

**Loop 2 in one line:** fly, record privately, review, improve a little, repeat.

---

### Loop 3: the sharing round (every 50 runs)

**Purpose:** pool traffic lessons across companies without sharing secrets, and decide who earns credits.

**Analogy:** driving schools send a neutral examiner their updated "road knowledge notes." The examiner checks them, grades how useful each school's notes were, merges them, gives credits by grade, and sends the merged notes back.

The 50-run interval follows Chen et al. 2023 [FROM PAPER]. [PROPOSED] for our setting, to tune.

#### Step 1: Send changes
Each company computes **change = current summarizer knobs minus the version it received last round**, and sends only that.

| Sent | Never sent |
|---|---|
| Summarizer changes | Diary (what drones saw, did, scored) |
| | Decider |
| | Delivery hubs and routes |

#### Step 2: Check for cheating
The referee flags a company's changes if they are:
- nearly empty or a copy of last round (possible free riding)
- pointing in a very different direction from the others
- paired with a sudden jump in grade

Flagged changes are held back for one round. (Details in Section 6.)

#### Step 3: Grade on a secret exam (Shapley value)
The referee holds a **secret exam**: a fixed set of tricky situations (dense merges, simultaneous arrivals at the crossing, mixed fleets, helicopter crossings). Companies never see it. Part of it is redrawn each period.

The referee builds the summarizer four ways (with 2 companies) and counts near-misses on the exam. In the count, near-misses under 100 m count fully and those under 500 m count 0.1 each (weight to tune).

| Summarizer built with | Near-miss count (example) |
|---|---|
| No new changes (last round's version) | 20 |
| Only A's changes | 15 |
| Only B's changes | 12 |
| Both | 9 |

Fair share of the improvement (Shapley value):
- **A:** alone 20 → 15 (5 fewer); after B 12 → 9 (3 fewer); average **4**
- **B:** alone 20 → 12 (8 fewer); after A 15 → 9 (6 fewer); average **7**
- Check: 4 + 7 = 11 = total improvement (20 → 9)

With 2 companies there are 4 combinations to test; with 3 companies, 8. Small enough to compute exactly.

**Smoothing:** running grade = 0.8 × old grade + 0.2 × this round's grade. Shapley grades are known to jump around between rounds [FROM PAPER: Geimer et al., IJCNN 2025].

**Hypothesis to test:** the slower fleet meets harder conflicts, so its lessons may be more valuable and earn higher grades.

#### Step 4: Merge
Three ways tested [PROPOSED]:

| Rule | How changes are combined | Question it answers |
|---|---|---|
| F1 | Equal weight | Does simply sharing make things fairer? |
| F2 | More weight to the company suffering more delay (q-FFL idea) | Does helping the worse-off company help more? |
| F3 | More weight to higher-graded company | Does favoring useful contributions build a better summarizer? |

#### Step 5: Hand out credits
New credits split by smoothed grade: company k gets (new credits) × (its grade) / (sum of grades).
Example: 100 credits, grades A = 4, B = 7 → A ≈ 36, B ≈ 64.

#### Step 6: Send back
Each company **replaces** its summarizer with the merged one and **keeps its own decider**, then returns to Loop 2.

**Watch out:** each decider was used to its company's old summarizer, so after the swap its inputs look slightly different (like a translator getting a new dictionary). It adapts over the next runs. If performance drops sharply after each round, share more often or blend the new summarizer in gradually. Monitor this early.

**Loop 3 in one line:** share summarizer changes, check them, grade them on a secret exam, merge them, reward with credits, send back.

---

### Loop 4: the credit cycle

**Purpose:** stop the "rich get richer" problem. Without it, an early top contributor could hoard credits and win every crossing forever.

**Analogy:** "go first" tokens at a busy junction. You earn them by maintaining the road. You hand one over when you go first. Handed-over tokens go into a jar that is shared out again.

#### Parts
1. **Wallets:** one per company, shared by its drones. Credits cannot be bought, sold, or transferred.
2. **Spending** (during runs, in Loop 1): only the winner of a crossing pays its offer.
   - Basic version [PROPOSED]: fixed offer rule (offer more when running late).
   - Stretch version: the decider learns how much to offer.
   - An empty wallet means offering 0 and usually yielding. The drone can still fly.
3. **Pool:** spent credits go here. They are not destroyed.
4. **Giveback** at the end of each period. Two rules tested [PROPOSED]:

   | Rule | How | Effect |
   |---|---|---|
   | Equal | Same share to every company | Simple; nobody falls far behind. A related karma study found equal redistribution reached maximum welfare in its case study [FROM PAPER: Elokda et al., multi-karma] |
   | Need-based | More to the company with more delay | Stronger push to fairness; may weaken the reward for helping |

5. **Cap:** no company may hold more than a set share of all credits (start at 60%). Excess returns to the pool.

#### Example over one period (made-up numbers)
| Moment | A wallet | B wallet | Pool |
|---|---|---|---|
| Start (after Loop 3 gave A 36, B 64) | 36 | 64 | 0 |
| A wins 5 crossings, pays 15 | 21 | 64 | 15 |
| B wins 10 crossings, pays 40 | 21 | 24 | 55 |
| Equal giveback (27.5 each) | 48.5 | 51.5 | 0 |
| Cap check (60% of 100 = 60): both under | 48.5 | 51.5 | 0 |

B helped more and won more crossings, but A was not left with nothing. Priority keeps circulating.

#### Cycle
```
earn (Loop 3) → spend at crossings (Loop 1) → pool → giveback + cap (Loop 4) → earn again
```

#### Why this is central to the project
| Setup | Expectation |
|---|---|
| K1: credits by grade, no giveback, no cap | Top contributor gets stronger over time |
| K2: full Loop 4 | Helping still rewarded; nobody locks in priority |

If K2 is fairer than K1 without losing safety, Loop 4 works.

**Loop 4 in one line:** earned credits are spent to go first, spent credits go into a pool, and the pool is shared back with a cap, so priority circulates.

---

## 4. The drone's brain in detail

### 4.1 One network, two parts
Each company has **one network**, used by all its drones (each drone runs a copy). It has two connected parts trained together:

| Part | Job | Shared? |
|---|---|---|
| Summarizer | Understand self, neighbors, and traffic | Yes, merged across companies in Loop 3 |
| Decider | Turn understanding into preferences | No, always private |

With 2 companies there are **2 networks** in total. The referee has none.

| Part | Company A vs Company B |
|---|---|
| Summarizer | Same after each sharing round; drifts slightly between rounds |
| Decider | Always different |

### 4.2 What already exists vs what is ours

| Element | Exists? | Source |
|---|---|---|
| Building blocks (layers, attention) | Yes | PyTorch library |
| Overall design (attention summarizer + decider) | Yes | Sharifi et al. 2026 |
| Neighbor-guessing part | Yes | Brittain and Wei 2022 |
| Shared/private split | **Ours** | For federation |
| Extra inputs (company, bid, manned flag) | **Ours** | For credits and helicopter |
| Ready-trained network to download | **No** | Sharifi released no code; Brittain and Wei's code availability unconfirmed |

We write the network ourselves following the papers, then train it from scratch.

### 4.3 Step-by-step with numbers

**What a layer does** (tiny example, 2 inputs, 1 output):
```
output = (knob1 × 0.3) + (knob2 × 0.4) + knob3
       = (2.0 × 0.3) + (−1.0 × 0.4) + 0.1 = 0.3
(negative results become 0)
```
A 64-unit layer does this 64 times with different knobs.

**Step 1: Self-summary.** 4 facts → layer (64 units) → **64 numbers**.

Why expand 4 to 64?
- the 64 numbers capture **combinations** (e.g., "fast and close to the crossing" means "arriving soon")
- attention compares self and neighbors number by number, so **both must be the same size**
- at the decision step, self (64) and traffic (64) get an **equal say**
- 64 itself is a design choice copied from Sharifi et al. for comparability; 32 or 128 would also work

**Step 2: Neighbor summaries.** Each neighbor's facts → layer (64 units) → 64 numbers. The same knobs are used for every neighbor, so any number of neighbors works.

**Step 3: Guess each neighbor's next move** [FROM PAPER: Brittain and Wei]. A small part (three 128-unit layers) outputs 3 percentages per neighbor:

| Neighbor | Slow | Keep | Speed up |
|---|---|---|---|
| B7 | 10% | 80% | 10% |
| H | 0% | 100% | 0% |

The guess is attached to that neighbor's summary (64 + 3), then squeezed back to 64. It is trained by comparing guesses with what neighbors actually did. In their paper this guessing raised accuracy to about 90% and cut loss-of-separation events from 28 to 4 with five agent types.

**Step 4: Attention (focus).** Compare self-summary with each neighbor summary to get importance scores, then convert to shares adding to 100%:

| Neighbor | Raw score | Share |
|---|---|---|
| B7 | 2.0 | 73% |
| H | 1.0 | 27% |

```
traffic summary = 0.73 × (B7 summary) + 0.27 × (H summary)   → 64 numbers
```
Always 64 numbers, whether there is 1 neighbor or 8. Sharifi et al. use a 64 × 64 attention module [FROM PAPER].

**End of summarizer (shared part).**

**Step 5: Decider (private part).** Self (64) + traffic (64) = 128 → two 128-unit layers → outputs:
- **3 preference scores**, turned into percentages (e.g., 10% / 30% / 60%)
- **1 expectation number** (e.g., 0.8 = "fairly good"), used only for learning

### 4.4 Network diagram
```
Self facts (4) ───► FC 64 ─────────────────────────────────────────────┐
                                                                        │
Each neighbor (4 + 3 extra) ──► FC 64 ──► guess head (3 × FC 128 → 3%)  │
                                   │              │                     │
                                   └── join (64+3) ──► FC 64            │
                                                    │                   │
                             Attention (64×64), self as the "question" ◄┘
                                                    │
                                       traffic summary (64)
            ═════════════ SHARED SUMMARIZER ENDS ═════════════
                     join self (64) + traffic (64) = 128
                                     │
                              FC 128 → FC 128
                                │           │
                     preferences (3)    expectation (1)
            ═════════════ PRIVATE DECIDER ═════════════
```

### 4.5 Training settings [FROM PAPER: Sharifi et al.]
| Setting | Value |
|---|---|
| Learning rate | 0.0001 |
| Entropy coefficient (encourages exploring) | 0.001 |
| PPO clip | 0.2 |
| Batch size | 512 |
| Passes per review | 8 |
| Optimizer | Adam |
| Advantage estimate | GAE |

Brittain and Wei also add the guessing loss to the training loss (total = policy + value + guess) [FROM PAPER].

---

## 5. The safety shield and the helicopter

### 5.1 Priority order (fixed, top wins) [PROPOSED]
1. **Helicopter:** drones always yield (US rule 14 CFR 107.37 requires small drones to yield to all aircraft) [FROM PAPER/REGULATION].
2. **Safety shield:** blocks any unsafe option.
3. **Credits:** decide who goes first among safe options only.
4. **Network:** chooses freely among what remains.

### 5.2 How the shield decides [PROPOSED]
- Looks ahead 30 seconds (to tune).
- For each of the drone's options, predicts where it would be.
- Assumes every nearby aircraft does the **worst thing it physically can** (max speed, worst direction).
- Removes any option that could bring the drone within **100 m of a drone** or **500 m of the helicopter**.
- If all options are removed: slow down.

### 5.3 What the guarantee covers
Safe separation is guaranteed **only if**:
- positions are known accurately (drones broadcast position, as FAA Remote ID requires)
- no aircraft exceeds the assumed maximum speed
- slowing down is always physically possible

We state these assumptions openly. This follows the shielding approach of ElSayed-Aly et al. (AAMAS 2021) and addresses the gap found in the Drones 2026 review: none of its 44 studies gave formally assured separation from crewed aircraft [FROM PAPER].

### 5.4 The helicopter [PROPOSED]
- Scripted (not a learner): fixed path across the delivery corridors, never changes course.
- Start with one crossing per run.
- Never bids for credits; always has priority.
- **[OPEN]** If speed changes alone cannot clear a crossing helicopter, add a "hold pattern" action.
- **[OPEN]** Core or stretch goal: mentor to decide.

---

## 6. Catching cheaters

### 6.1 Cheats we test by playing the cheater [PROPOSED]
| Cheat | What the cheater does | Goal |
|---|---|---|
| A1: Free riding | Sends nearly empty or recycled changes | Get the merged summarizer for free |
| A2: Exam gaming | Tunes changes to look good on exam-like situations | Inflate grade and credits |
| A3 (stretch): Rival slowdown | Crafts changes that make rivals' drones more cautious | Win crossings without paying |

### 6.2 Defenses [PROPOSED]
1. **Secret, rotating exam:** a grade that collapses on the new exam draw is flagged.
2. **Suspicious-change check:** changes very different from everyone else's, or sudden grade jumps, are held back one round.
3. **Smoothing and cap:** one round of cheating cannot buy much.
4. **Shadow test:** the referee also tests on the normal training scenario and compares.

Why this is needed: when companies report or influence their own contribution scores, selfish ones can manipulate them [FROM PAPER: arXiv 2602.21721]; honest companies with unusual data can also look like free riders [FROM PAPER: FRIDA].

### 6.3 What we measure
- extra credits a cheater gains
- change in fairness and safety under attack
- how many rounds until each defense flags the cheater

### 6.4 Stretch: route leakage
Shared changes can leak training data in federated RL [FROM PAPER: RGIA 2025; Li et al. 2023]. Test whether a rival can work out another company's hubs and routes from its summarizer changes, and whether sharing only the summarizer, or adding noise, prevents it.

---

## 7. View 2: What the parts are (components)

| # | Component | What it is | Loops | Tool | Owner |
|---|---|---|---|---|---|
| 1 | Simulator | Moves all aircraft; the "video game" of the sky | 1 | BlueSky (existing, open source) | Member 1 configures |
| 2 | Wrapper | Connects BlueSky to the networks: hands each drone what it sees, takes back actions; handles changing numbers of drones | 1 | Our code (PettingZoo-style); BlueSky-Gym as a possible starting point | Member 1 |
| 3 | Scenario | Routes, crossings, fleets, helicopter path, solo-run setups | 1 | Our code | Member 1 |
| 4 | Network | Summarizer + decider per company | 1, 2 | PyTorch | Member 2 |
| 5 | Trainer | Review-and-improve (PPO), diaries | 2 | Our code (possibly based on CleanRL) | Member 2 |
| 6 | Referee | Cheating checks, exam grading (Shapley), merging | 3 | Our code | Member 3 |
| 7 | Credit ledger | Wallets, bids, pool, giveback, cap | 1, 4 | Our code | Member 3 |
| 8 | Safety shield | Look-ahead checker | 1 | Our code | Member 4 |
| 9 | Measurement | Logs near-misses, times, fairness, credits; graphs and statistics | All | TensorBoard or Weights & Biases; pandas, SciPy, matplotlib | Member 4 |

**Where it runs:** one computer with a GPU, one program. Companies and referee are separate parts of the code that only exchange what they are allowed to. Optionally, parallel copies of the simulator speed up training (Brittain and Wei used 75 parallel workers with Ray [FROM PAPER]).

### 7.1 Is BlueSky enough?
Yes, for our questions, which are about positions, timing, near-misses, delay and fairness. Using it keeps results comparable with Sharifi et al. and Brittain and Wei.

| BlueSky does not model | Matters? |
|---|---|
| Detailed drone physics | No (we control speed only) |
| Wind | Slightly; state as limitation |
| Battery drain | No (missions under 18 min) |
| Buildings | No (fixed corridors) |
| Radio loss, position errors | Matters for the shield; can add noise as a robustness test |
| Built-in multi-agent RL interface | Yes; we build the wrapper (budget weeks 1 to 3) |

BlueSky-Gym (TU Delft, MIT license, v0.2.0, June 2025) provides Gymnasium environments built on BlueSky, including a merging environment. Its multi-agent support is unconfirmed; check before relying on it.

Optional: a tiny pure-Python copy of the scenario for fast debugging of credits, merging and shield logic. Final results always from BlueSky.

---

## 8. What data goes where (privacy map)

| Data | Company A | Company B | Referee |
|---|---|---|---|
| A's diary (what A's drones saw, did, scored) | ✅ | ❌ | ❌ |
| A's decider | ✅ | ❌ | ❌ |
| A's hubs and routes | ✅ | ❌ | ❌ |
| A's summarizer changes | ✅ | ❌ | ✅ |
| Merged summarizer | ✅ | ✅ | ✅ |
| Credit wallets and bids | ✅ own | ✅ own | ✅ all |
| Positions and speeds of nearby aircraft | ✅ (broadcast, as Remote ID) | ✅ | ✅ |
| Secret exam | ❌ | ❌ | ✅ |

---

## 9. All settings in one place

| Setting | Value | Source |
|---|---|---|
| Simulator | BlueSky | Sharifi et al.; Brittain and Wei |
| Location | Frisco, Dallas | Sharifi et al. |
| Routes | 4, about 10.33 km each; merges WP3, WP7; crossing WP9 | Sharifi et al. |
| Companies | 2 (3 if compute allows) | Ours |
| Drones per company | 10 | Sharifi et al. |
| Strong fleet X | 0 to 44.88 m/s, ±1.71 m/s², sensing 1000 m | Sharifi et al. |
| Weak fleet Y | 0 to 30.12 m/s, ±1.02 m/s², sensing 750 m | Sharifi et al. |
| Step | 3 s | Sharifi et al. |
| Max run time | 18 min | Sharifi et al. |
| NMAC / LoWC | 100 m / 500 m | Sharifi et al. |
| Actions | slow, keep, speed up | Sharifi et al. |
| Sharing interval | every 50 runs (to tune) | Chen et al. |
| Smoothing | 0.8 old + 0.2 new | Ours |
| Exam weight for LoWC | 0.1 (to tune) | Ours |
| Conflict detection | within 500 m within 60 s (to tune) | Ours |
| Credit cap | 60% (to tune) | Ours |
| Shield look-ahead | 30 s (to tune) | Ours |
| Shield distances | 100 m drones, 500 m helicopter | Ours, based on thresholds above |
| Network sizes | FC 64 encoders, 64×64 attention, 2 × FC 128 decider | Sharifi et al. |
| Guess head | 3 × FC 128 → 3 outputs | Brittain and Wei |
| Training | lr 1e-4, entropy 1e-3, clip 0.2, batch 512, 8 passes, Adam, GAE | Sharifi et al. |
| Runs per setup | 2,500 (Sharifi); ours to tune | Sharifi et al. |
| Evaluation | 300 runs with learning frozen | Sharifi et al. |
| Seeds | 3 per setup (Sharifi used 5) | Ours |

---

## 10. Known risks in the architecture

| Risk | Where | Mitigation |
|---|---|---|
| Decider confused after summarizer swap | Loop 3, step 6 | Share more often; blend gradually; monitor |
| Shapley grades unstable | Loop 3, step 3 | Smoothing |
| Honest unusual company looks like a free rider | Loop 3, step 2 | Hold back, do not punish; combine several checks |
| Speed-only actions cannot clear the helicopter | Loop 1 | Add hold-pattern action [OPEN] |
| Shield too cautious, drones barely move | Loop 1 | Tune look-ahead and assumptions |
| No multi-agent wrapper ready | Component 2 | Budget weeks 1 to 3 |
| Training slow (7+ hours per run) | Loop 2 | Parallel simulators; fewer seeds for secondary setups |
| Summarizer changes still leak secrets | Loop 3 | Stretch test; state as limitation |

---

## 11. Open decisions

| # | Decision | Who |
|---|---|---|
| 1 | Helicopter and shield: core or stretch? | Mentor |
| 2 | Add a hold-pattern action? | Team, after early tests |
| 3 | Custom PPO vs CleanRL base | Member 2 |
| 4 | Use BlueSky-Gym or build wrapper from scratch | Member 1, after checking multi-agent support |
| 5 | Equal vs need-based giveback as the main version | Team, after experiments |
| 6 | Sharing interval (50 runs or other) | Member 3, after early tests |
| 7 | GPU access for about 300 GPU-hours | Team |
| 8 | Check whether Brittain and Wei's code is on GitHub (marcbrittain) | Member 2 |

---

## 12. Common confusions, answered

**Is it two networks?**
One network per company, with two parts (summarizer and decider) trained together. With 2 companies, 2 networks total.

**Does winning a bid let a drone do something the network didn't suggest?**
No. The bid only removes "speed up" from the loser. The winner keeps the network's own preferences.

**Does winning a bid override safety?**
No. The safety check runs after the bid and removes unsafe options regardless.

**Why is my own summary 64 numbers if I only have 4 facts?**
To capture combinations of facts, to match neighbor summaries for attention, and to give self and traffic an equal say. 64 is copied from Sharifi et al.

**Do the networks already exist?**
The design exists in papers. The trained network does not. We build it in PyTorch and train it from scratch.

**What does the referee share back?**
Only the merged summarizer and credits. Never another company's diary or decider.

**Do credits affect learning?**
No. Credits are not in the score. They only affect who goes first at crossings.

---

## 13. References

1. I. Sharifi, H. T. Kim, M. H. Ahmed, M. Ghasemi, P. Wei. Separation Assurance between Heterogeneous Fleets of Small Unmanned Aerial Systems via Multi-Agent Reinforcement Learning. arXiv:2605.01041, 2026 (preprint).
2. M. Brittain, P. Wei. Scalable Autonomous Separation Assurance With Heterogeneous Multi-Agent Reinforcement Learning. IEEE T-ASE 19(4), 2022. doi:10.1109/TASE.2022.3151607
3. J. Chen et al. Model-aided Federated Reinforcement Learning for Multi-UAV Trajectory Planning in IoT Networks. IEEE GLOBECOM Workshops 2023. arXiv:2306.02029
4. J. Samu, C. Yang, K. R. Poddar. Optimization and Tactical Deconfliction for Drone Search-and-Rescue in Low-Altitude Airspace: A Systematic Literature Review. Drones 10(8):596, 2026.
5. E. Elokda et al. CARMA: Fair and Efficient Bottleneck Congestion Management via Nontradable Karma Credits. Transportation Science, 2025. arXiv:2208.07113
6. E. Elokda et al. Coupled Resource Allocations with Multi-Karma Economies. arXiv:2412.17002
7. A. Geimer, B. Fiz, R. State. On the Volatility of Shapley-Based Contribution Metrics in Federated Learning. IJCNN 2025.
8. Private and Robust Contribution Evaluation in Federated Learning. arXiv:2602.21721
9. FRIDA: Free-Rider Detection using Privacy Attacks. arXiv:2410.05020
10. Gradient Inversion in Federated Reinforcement Learning (RGIA). arXiv:2512.00303
11. M. Li, W. Ding, D. Zhao. Your Room is not Private: Gradient Inversion Attack on Reinforcement Learning. arXiv:2306.09273
12. M. ElSayed-Aly et al. Safe Multi-Agent Reinforcement Learning via Shielding. AAMAS 2021.
13. T. Li et al. Fair Resource Allocation in Federated Learning (q-FFL). ICLR 2020 (to verify).
14. J. M. Hoekstra, J. Ellerbroek. BlueSky ATC Simulator Project. ICRAT 2016.
15. BlueSky-Gym: Reinforcement Learning Environments for Air Traffic Applications. SESAR Innovation Days 2024. https://pypi.org/project/bluesky-gym
16. 14 C.F.R. 107.37, Operation near aircraft; right-of-way rules.
