"""Statistical comparisons for KarmaSky evaluation results."""

from __future__ import annotations

import math
from collections.abc import Mapping, Sequence
from typing import Any

from scipy.stats import mannwhitneyu


def _clean_sample(values: Sequence[float], name: str) -> list[float]:
    cleaned: list[float] = []
    for value in values:
        try:
            number = float(value)
        except (TypeError, ValueError) as exc:
            raise ValueError(f"{name} contains a non-numeric value: {value!r}") from exc
        if not math.isfinite(number):
            raise ValueError(f"{name} contains a non-finite value: {value!r}")
        cleaned.append(number)
    if not cleaned:
        raise ValueError(f"{name} must contain at least one observation")
    return cleaned


def mann_whitney_comparison(
    group_a: Sequence[float],
    group_b: Sequence[float],
    *,
    name_a: str = "A",
    name_b: str = "B",
    alternative: str = "two-sided",
) -> dict[str, Any]:
    """Compare two independent samples and report rank-biserial effect size.

    A positive rank_biserial means values in group A tend to be larger than B;
    a negative value means values in A tend to be smaller than B.
    """
    a = _clean_sample(group_a, name_a)
    b = _clean_sample(group_b, name_b)
    if alternative not in {"two-sided", "less", "greater"}:
        raise ValueError("alternative must be 'two-sided', 'less' or 'greater'")

    result = mannwhitneyu(a, b, alternative=alternative, method="auto")
    u_value = float(result.statistic)
    rank_biserial = (2.0 * u_value / (len(a) * len(b))) - 1.0

    return {
        "group_a": name_a,
        "group_b": name_b,
        "n_a": len(a),
        "n_b": len(b),
        "u_statistic": u_value,
        "p_value": float(result.pvalue),
        "median_a": float(sorted(a)[len(a) // 2]) if len(a) % 2 else float(
            (sorted(a)[len(a) // 2 - 1] + sorted(a)[len(a) // 2]) / 2.0
        ),
        "median_b": float(sorted(b)[len(b) // 2]) if len(b) % 2 else float(
            (sorted(b)[len(b) // 2 - 1] + sorted(b)[len(b) // 2]) / 2.0
        ),
        "rank_biserial_effect": rank_biserial,
        "alternative": alternative,
    }


def holm_correction(p_values: Mapping[str, float]) -> dict[str, float]:
    """Return Holm-adjusted p-values, preserving the input keys.

    Holm controls family-wise error when several hypotheses are tested.
    """
    if not p_values:
        return {}

    checked: list[tuple[str, float]] = []
    for name, value in p_values.items():
        p = float(value)
        if not math.isfinite(p) or not 0.0 <= p <= 1.0:
            raise ValueError(f"p-value for {name!r} must be between 0 and 1")
        checked.append((name, p))

    ordered = sorted(checked, key=lambda item: item[1])
    total = len(ordered)
    adjusted: dict[str, float] = {}
    running_max = 0.0
    for index, (name, p_value) in enumerate(ordered):
        candidate = min(1.0, (total - index) * p_value)
        running_max = max(running_max, candidate)
        adjusted[name] = running_max
    return {name: adjusted[name] for name, _ in checked}


def compare_to_baseline(
    results_by_setup: Mapping[str, Sequence[float]],
    *,
    baseline: str = "B1",
    metric_name: str = "metric",
    alpha: float = 0.05,
) -> list[dict[str, Any]]:
    """Compare each setup with a baseline and apply Holm correction.

    Each sequence should contain per-evaluation-episode observations for the
    same metric. Do not pass only one aggregate mean per setup.
    """
    if baseline not in results_by_setup:
        raise KeyError(f"Baseline {baseline!r} was not found in results_by_setup")
    if not 0.0 < alpha < 1.0:
        raise ValueError("alpha must be between 0 and 1")

    comparisons: list[dict[str, Any]] = []
    raw_p: dict[str, float] = {}
    for setup, values in results_by_setup.items():
        if setup == baseline:
            continue
        result = mann_whitney_comparison(
            values,
            results_by_setup[baseline],
            name_a=setup,
            name_b=baseline,
        )
        result["metric"] = metric_name
        comparisons.append(result)
        raw_p[setup] = result["p_value"]

    adjusted = holm_correction(raw_p)
    for result in comparisons:
        result["p_value_holm"] = adjusted[result["group_a"]]
        result["significant_after_holm"] = result["p_value_holm"] < alpha
        result["alpha"] = alpha
    return comparisons
