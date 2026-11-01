# Design Updates (overrides older files)

These changes were agreed in discussion after `KarmaSky_Project_Brief.md`, `KarmaSky_Architecture.md` and the Phase-1 PPT were written. **Where they disagree, this file wins.** All items are **[PROPOSED]** until the mentor confirms.

---

## Update 1: Bid happens before Think

**Old (Architecture md):** Look → Think → Check (bid resolved inside Check) → Act → Score

**New:** Look → **Bid** → Think → Check → Act → Score

**Why:** the contest and its result depend only on positions, not on the brain's output, so it is cleaner to resolve it first. The result is still **applied** in Check, as one of the filters that remove options.

**What does not change:** the brain always runs, every step. The bid and shield never choose an action; they only remove options.

---

## Update 2: Privacy leak fixes (shared updates can reveal routes)

**The problem (raised by the team):** a company's shared update is learned from its own flights. With only 2 companies and plain averaging, Company A can compute Company B's update exactly:

> B's update = 2 × merged update − A's update

Research on gradient inversion (Li, Ding, Zhao; RGIA) shows such updates can be used to reconstruct parts of the training data, which here could mean routes or hub locations.

**Fixes [PROPOSED]:**

| # | Fix | Effect |
|---|---|---|
| 1 | **Share less.** Keep the own-state encoder private. Share only the neighbor encoder, attention and intent head (the parts about *other* drones) | Parts that learn your own routes never leave the company |
| 2 | **Relative inputs only.** Observations use relative distances and bearings, never absolute coordinates or hub positions | Even the shared parts never see map positions directly |
| 3 | **3 or more companies** in at least one experiment (X+Y+Y) | Subtraction trick no longer isolates one company |
| 4 | **Noise (differential privacy)** on shared updates, as an optional setting | Harder to reconstruct anything; may cost some performance, which we measure |
| 5 | **Referee sees updates, companies see only the merged result** | Companies cannot read each other's individual updates |

**Consequence:** the **route-leakage test moves from stretch goal to core**. We run a simple attack: from the shared updates, try to guess the other company's routes or merge points, and report how well it works with and without the fixes.

**Note:** fix 1 changes what "summarizer" means in other files. Read "summarizer (shared)" as "the neighbor/traffic parts of the summarizer". The own-state encoder joins the private decider side. This is **[OPEN]** until tested: sharing less might also reduce the benefit of federation, which is itself a result worth reporting.

---

## Update 3: What data is shared, final table

| Data | Leaves the company? | Who sees it |
|---|---|---|
| Raw flight logs (diary) | No | Company only |
| Private decider and own-state encoder | No | Company only |
| Changes to shared neighbor/attention/intent parts | Yes, every 50 episodes | Referee only |
| Merged shared parts | Yes | All companies |
| Contribution scores and credit balances | Yes | All companies (transparency) **[OPEN]** |
| Bids at a contest | Yes | Referee; result shared with both drones |
| Live positions during flight | Yes (as today with transponders / Remote ID) | Nearby drones and referee |

---

## Update 4: Where the brain lives

- **Simulation:** one brain per company on one computer; all 10 drones are processed together in one batch.
- **Real world (vision, not built):** trained copy on every drone, no in-flight learning; company servers retrain from logs; referee would be a UTM provider such as Digital Sky; link loss means "assume you lost the bid and yield".

---

## Files still to be updated with these changes

- [ ] [`KarmaSky_Architecture.md`](../design/KarmaSky_Architecture.md): Loop 1 order, privacy section
- [ ] [`KarmaSky_Project_Brief.md`](../design/KarmaSky_Project_Brief.md): Sections 6, 7, 13 (route leakage to core), 15
- [ ] [`KarmaSky_EL_Phase1.pptx`](../presentations/KarmaSky_EL_Phase1.pptx): Loop 1 diagram, data-flow slide
