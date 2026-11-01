# Open Decisions and Mentor Questions

Bring this to every mentor meeting. Move items to "Decided" with the date and who decided.

---

## Questions for the mentor

| # | Question | Why it matters | Options |
|---|---|---|---|
| M1 | Is the refined scope (fairness + earned priority via karma credits) acceptable, compared with the original wording "federated MARL framework for UAV and manned aerial vehicle delivery networks"? | Defines the whole project | Approve / narrow to pure FedMARL / other |
| M2 | Did "manned aerial vehicle delivery" mean manned aircraft that also deliver (mixed fleet), or manned aircraft drones must avoid? | Changes the helicopter part | Mixed fleet / avoid-only |
| M3 | Is the manned helicopter + safety shield core or stretch? | 2 to 3 weeks of work | Core / stretch |
| M4 | Is a mechanism-design angle (credits, incentives) acceptable in this course, or should the focus stay on RL? | Grading fit | Keep / reduce |
| M5 | Are 2 to 3 companies enough, or do evaluators expect more? | Compute and Shapley cost | 2 / 3 / more |
| M6 | Can the department provide GPU time (about 300 GPU-hours estimated)? | Without it we cut seeds and episodes | Lab / cloud / reduce scope |
| M7 | Is simulation-only acceptable for the final evaluation? | Expectations | Yes (normal in this field) / needs hardware demo |
| M8 | Is a paper submission a goal? | Changes how carefully we run statistics and write | Yes / no |

## Technical decisions for the team

| # | Decision | Options | Owner | Status |
|---|---|---|---|---|
| T1 | Copy Sharifi's design exactly, or change it? | Exact (comparable) / modified | Member 2 | [OPEN], lean exact |
| T2 | Federation interval | 50 episodes / tune | Member 3 | [OPEN] |
| T3 | Which summarizer parts are shared (privacy update) | All / neighbor + attention + intent only | Members 2, 3 | [OPEN], see `06` |
| T4 | Credit redistribution | Uniform / need-based | Member 3 | [OPEN] |
| T5 | Bidding rule | Fixed rule (e.g. bid more when more delayed) / learned | Member 3 | [OPEN], lean fixed |
| T6 | Credit cap | 60% / other | Member 3 | [PROPOSED] 60% |
| T7 | Shapley utility | Safety only / safety + efficiency | Member 3 | [OPEN] |
| T8 | Contest definition | Within 500 m within 60 s | Members 1, 3 | [PROPOSED] |
| T9 | Are scores and balances visible to all companies? | Yes / no | Team | [OPEN] |
| T10 | Differential privacy noise | Off / one noise level / sweep | Member 3 | [OPEN] |
| T11 | Review of the 5 borrowed building blocks | See brief Section 14 | All | [FOR REVIEW] |

## Verification to-dos

- [ ] Read arXiv 2511.11616 and 2605.20625 for overlap
- [ ] Verify q-FFL citation
- [ ] Check BlueSky-Gym multi-agent support
- [ ] Check for Brittain and Wei public code
- [ ] Confirm links in `05_READING_LIST.md`
- [ ] Add team names to PPT title slide

## Decided

| Date | Decision | By |
|---|---|---|
| | | |
