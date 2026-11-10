"""Run the Member 4 evaluation modules on clearly labelled sample data.

From the repository root:
    python examples/run_demo.py
"""

import csv
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PROJECT_ROOT = ROOT.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from karmasky.eval.metrics import calculate_metrics
from karmasky.eval.plots import (
    plot_credit_balances,
    plot_delay_by_company,
    plot_nmac_by_setup,
)
from karmasky.eval.stats import compare_to_baseline

RESULTS = ROOT / "demo_results"


def read_csv(path: Path):
    with path.open("r", newline="", encoding="utf-8") as file:
        return list(csv.DictReader(file))


steps = read_csv(ROOT / "sample_step_logs.csv")
flights = read_csv(ROOT / "sample_flight_logs.csv")
credits = read_csv(ROOT / "sample_credit_logs.csv")
metrics = calculate_metrics(steps, flights)

RESULTS.mkdir(exist_ok=True)
(RESULTS / "sample_metrics.json").write_text(
    json.dumps(metrics, indent=2), encoding="utf-8"
)

# A single sample setup is enough to demonstrate the plotting functions.
# Actual comparisons require logs from B1, F1, F2, K2, etc.
plot_delay_by_company({"SAMPLE_ONLY": metrics}, output_path=RESULTS / "delay_by_company.png")
plot_nmac_by_setup({"SAMPLE_ONLY": metrics}, output_path=RESULTS / "safety_events.png")
plot_credit_balances(credits, output_path=RESULTS / "credit_balances.png")

# Synthetic demonstration arrays only; these are not experiment results.
demo_results = {
    "SYNTHETIC_BASELINE": [0.42, 0.39, 0.45, 0.41, 0.44, 0.40],
    "SYNTHETIC_SETUP_A": [0.34, 0.36, 0.33, 0.35, 0.37, 0.32],
    "SYNTHETIC_SETUP_B": [0.28, 0.31, 0.29, 0.30, 0.27, 0.32],
}
comparisons = compare_to_baseline(
    demo_results,
    baseline="SYNTHETIC_BASELINE",
    metric_name="synthetic_metric",
)
(RESULTS / "demo_statistics.json").write_text(
    json.dumps(comparisons, indent=2), encoding="utf-8"
)

print("SAMPLE-ONLY metrics:")
print(json.dumps(metrics, indent=2))
print(f"\nDemo outputs saved in: {RESULTS}")
print("The sample numbers are for code testing only, not KarmaSky experiment results.")
