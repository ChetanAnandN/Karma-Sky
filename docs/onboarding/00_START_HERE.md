# KarmaSky: Start Here

**Read this file first.** It tells you what the project is in one minute, which files exist, and the order to read them.

> Status tags used in every file:
> - **[FROM PAPER]** taken from a published paper, with citation
> - **[PROPOSED]** our plan, not yet tested
> - **[OPEN]** not decided yet
> - **[FOR REVIEW]** borrowed building block, still being discussed with the team and mentor, not confirmed

---

## The project in one minute

**Title [PROPOSED]:** KarmaSky: Contribution-Earned Priority for Fair Shared Learning Between Competing Drone Delivery Operators

**Mentor's original idea:** a federated multi-agent reinforcement learning framework for UAV and manned aerial vehicle delivery networks.

**The problem:** Several delivery companies fly drones in the same city airspace. Each company trains its own AI to avoid collisions. A 2026 study (Sharifi et al.) showed that when a company with strong, fast drones shares the sky with a company with weaker, slower drones, the weaker company ends up yielding more and getting delayed more. Nobody tracks this unfairness.

**What we build (all in simulation, no physical drones):**
1. **Shared learning between rival companies.** Companies improve their collision-avoidance AI together without sharing raw flight data (federated learning).
2. **Contribution scoring.** A neutral referee measures how much each company's update actually improved safety for everyone.
3. **Karma credits.** Companies earn credits for helpful contributions and spend them to get priority at busy crossings. Credits cannot be bought.
4. **Safety shield.** A hard rule layer that blocks any move that would come too close to another drone or a manned helicopter. Safety always beats credits.
5. **Integrity checks.** Detect companies that try to cheat the scoring.

**The main question:** Can shared learning plus earned priority make the airspace fairer for the weaker company without making it less safe?

---

## Files in this folder

| File | What it is | Who should read it |
|---|---|---|
| `00_START_HERE.md` | This file | Everyone, first |
| `01_PROJECT_IN_PLAIN_WORDS.md` | Full explanation with no AI/ML background needed | Everyone |
| `02_HOW_THE_SYSTEM_WORKS.md` | The 4 loops, the two-part brain, step by step | Everyone, then reread by your module owner |
| `03_GETTING_STARTED.md` | Setup, repo structure, coding rules, first week tasks | Everyone before writing code |
| `04_TEAM_ROLES_AND_TASKS.md` | Who does what, week by week checklists | Everyone |
| `05_READING_LIST.md` | Papers in priority order, with links and what to look for | Everyone |
| `06_DESIGN_UPDATES.md` | Changes agreed after the brief was written (bid before think, privacy fixes) | Everyone, important |
| `07_OPEN_DECISIONS_AND_MENTOR_QUESTIONS.md` | Things not decided yet, and questions for the mentor | Team lead, everyone before mentor meetings |
| `08_FAQ_AND_GLOSSARY.md` | Common confusions and every term explained | Keep open while reading |
| `09_EXPERIMENT_PLAN.md` | Every experiment, metric and statistical test | Members 2, 3, 4 |

**Older, longer files (also shared):**

| File | Notes |
|---|---|
| [`KarmaSky_Project_Brief.md`](../design/KarmaSky_Project_Brief.md) | Full master brief, 17 sections. Section 14 lists the 5 FOR REVIEW building blocks |
| [`KarmaSky_Architecture.md`](../design/KarmaSky_Architecture.md) | Detailed architecture. Note: places bidding inside the Check stage; `06_DESIGN_UPDATES.md` overrides this |
| [`KarmaSky_EL_Phase1.pptx`](../presentations/KarmaSky_EL_Phase1.pptx) | Phase-1 presentation |
| [`MASTER_PLAN.md`](../plan/MASTER_PLAN.md) | Whole-project plan: priority tiers, phases and gates |
| KarmaSky: Methodology (Claude Doc) | Methodology document |

If any older file disagrees with `06_DESIGN_UPDATES.md`, the updates file wins.

---

## Reading order

**Day 1 (about 2 hours)**
1. This file
2. `01_PROJECT_IN_PLAIN_WORDS.md`
3. `08_FAQ_AND_GLOSSARY.md` (skim, then keep open)

**Day 2 (about 3 hours)**
4. `02_HOW_THE_SYSTEM_WORKS.md`
5. `06_DESIGN_UPDATES.md`
6. `04_TEAM_ROLES_AND_TASKS.md` (find your role)

**Day 3 onward**
7. `03_GETTING_STARTED.md` and do the Week 1 setup
8. `05_READING_LIST.md`: read the 3 core papers first, then the ones tagged for your role

---

## Five rules for the whole team

1. **Simulation only.** Everything runs in the BlueSky simulator. Never claim real-world results.
2. **Never call borrowed work ours.** The 5 building blocks (MARL base, federated RL, karma credits, Shapley scoring, safety shields) are other people's work. Our contribution is combining them for competing operators and the fairness questions we answer.
3. **No invented numbers.** Every number in the report comes from our runs or a cited paper. If we do not know, we write "to be measured".
4. **Safety beats everything.** In code and in the report: manned aircraft first, then shield, then credits, then the AI's choice. Credits never enter the reward.
5. **Reproduce before you add.** We first reproduce the Sharifi baseline. Nothing new is added until the baseline works.
