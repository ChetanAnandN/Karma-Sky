"""Standard KarmaSky plots: delay, safety events and credit balances."""

from __future__ import annotations

import math
from collections.abc import Mapping
from pathlib import Path
from typing import Any

import matplotlib.pyplot as plt


def _save(fig: Any, output_path: str | Path | None) -> None:
    if output_path is not None:
        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(path, dpi=160, bbox_inches="tight")


def plot_delay_by_company(
    experiment_metrics: Mapping[str, Mapping[str, Any]],
    *,
    output_path: str | Path | None = None,
):
    """Plot normalized delay for each company across experiment setups.

    experiment_metrics format: {"B1": calculate_metrics(...), "F1": ...}
    """
    if not experiment_metrics:
        raise ValueError("experiment_metrics cannot be empty")

    setups = list(experiment_metrics)
    companies = sorted(
        {
            company
            for result in experiment_metrics.values()
            for company in result.get("companies", {})
        }
    )
    if not companies:
        raise ValueError("No company metrics found in experiment_metrics")

    fig, ax = plt.subplots(figsize=(9, 5))
    for company in companies:
        values = [
            experiment_metrics[setup].get("companies", {}).get(company, {}).get(
                "normalized_delay"
            )
            for setup in setups
        ]
        ax.plot(setups, values, marker="o", linewidth=2, label=company)

    ax.set_title("Normalized delay by company")
    ax.set_xlabel("Experiment setup")
    ax.set_ylabel("Normalized delay (fraction; lower is better)")
    ax.axhline(0, linewidth=0.8)
    ax.grid(True, alpha=0.3)
    ax.legend(title="Company")
    fig.tight_layout()
    _save(fig, output_path)
    return fig


def plot_nmac_by_setup(
    experiment_metrics: Mapping[str, Mapping[str, Any]],
    *,
    output_path: str | Path | None = None,
):
    """Plot NMAC and LoWC flagged-record counts for each setup."""
    if not experiment_metrics:
        raise ValueError("experiment_metrics cannot be empty")
    setups = list(experiment_metrics)
    nmac = [
        experiment_metrics[s].get("safety", {}).get("nmac_count", 0) for s in setups
    ]
    lowc = [
        experiment_metrics[s].get("safety", {}).get("lowc_count", 0) for s in setups
    ]

    positions = list(range(len(setups)))
    width = 0.38
    fig, ax = plt.subplots(figsize=(9, 5))
    ax.bar([p - width / 2 for p in positions], nmac, width, label="NMAC")
    ax.bar([p + width / 2 for p in positions], lowc, width, label="LoWC")
    ax.set_xticks(positions, setups)
    ax.set_title("Safety event records by setup")
    ax.set_xlabel("Experiment setup")
    ax.set_ylabel("Flagged per-drone step-log records")
    ax.grid(axis="y", alpha=0.3)
    ax.legend()
    fig.tight_layout()
    _save(fig, output_path)
    return fig


def plot_credit_balances(
    credit_logs: Any,
    *,
    output_path: str | Path | None = None,
):
    """Plot credit balances over time.

    credit_logs may be a pandas DataFrame or iterable of dict/dataclass rows
    with fields: time_s, company, balance. Member 3 must provide this log;
    it is not part of the current StepLog/FlightLog interface yet.
    """
    if hasattr(credit_logs, "to_dict"):
        records = credit_logs.to_dict(orient="records")
    else:
        records = list(credit_logs)
    if not records:
        raise ValueError("credit_logs cannot be empty")

    grouped: dict[str, list[tuple[float, float]]] = {}
    for row in records:
        if isinstance(row, Mapping):
            time_value, company, balance = row.get("time_s"), row.get("company"), row.get("balance")
        else:
            time_value = getattr(row, "time_s", None)
            company = getattr(row, "company", None)
            balance = getattr(row, "balance", None)
        if time_value is None or company is None or balance is None:
            raise ValueError("Each credit row needs time_s, company and balance")
        company_name = str(company).strip()
        if not company_name:
            raise ValueError("Each credit row needs a non-empty company")
        try:
            time_s, credit_balance = float(time_value), float(balance)
        except (TypeError, ValueError) as exc:
            raise ValueError("Credit time_s and balance must be numeric") from exc
        if not math.isfinite(time_s) or not math.isfinite(credit_balance):
            raise ValueError("Credit time_s and balance must be finite")
        grouped.setdefault(company_name, []).append((time_s, credit_balance))

    fig, ax = plt.subplots(figsize=(9, 5))
    for company, values in sorted(grouped.items()):
        values.sort(key=lambda pair: pair[0])
        ax.plot(
            [pair[0] for pair in values],
            [pair[1] for pair in values],
            marker="o",
            label=company,
        )
    ax.set_title("Karma credit balances over time")
    ax.set_xlabel("Simulation time (seconds)")
    ax.set_ylabel("Credit balance")
    ax.grid(True, alpha=0.3)
    ax.legend(title="Company")
    fig.tight_layout()
    _save(fig, output_path)
    return fig
