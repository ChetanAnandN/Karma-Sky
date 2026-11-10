import pytest

from karmasky.eval.metrics import calculate_metrics
from karmasky.eval.plots import (
    plot_credit_balances,
    plot_delay_by_company,
    plot_nmac_by_setup,
)
from karmasky.eval.stats import compare_to_baseline, holm_correction, mann_whitney_comparison
from karmasky.interfaces import Action, FlightLog, StepLog


def test_metrics_hand_calculated_example():
    steps = [
        {"company": "X", "flags": ["NMAC"]},
        {"company": "Y", "flags": ["LoWC", "shield"]},
    ]
    flights = [
        {"company": "X", "start_s": 0, "end_s": 120, "solo_time_s": 100},
        {"company": "Y", "start_s": 0, "end_s": 150, "solo_time_s": 100},
    ]
    result = calculate_metrics(steps, flights)
    assert result["safety"]["nmac_count"] == 1
    assert result["safety"]["lowc_count"] == 1
    assert result["companies"]["X"]["normalized_delay"] == pytest.approx(0.2)
    assert result["companies"]["Y"]["normalized_delay"] == pytest.approx(0.5)
    assert result["fairness"]["normalized_delay_gap"] == pytest.approx(0.3)
    assert result["fairness"]["worst_off_delay"] == pytest.approx(0.5)
    assert result["fairness"]["sharifi_ft_percent"] == pytest.approx(80.0)


def test_metrics_accept_project_log_dataclasses():
    steps = [
        StepLog(
            0, "X1", "X", (0.0, 0.0), Action.HOLD, 100.0, ["NMAC", "LoWC", "shield"]
        ),
        StepLog(1, "Y1", "Y", (1.0, 1.0), Action.SLOW, 90.0, []),
    ]
    flights = [
        FlightLog("X1", "X", 0.0, 120.0, 100.0),
        FlightLog("Y1", "Y", 0.0, 150.0, 100.0),
    ]

    result = calculate_metrics(steps, flights)

    assert result["safety"]["nmac_count"] == 1
    assert result["safety"]["lowc_count"] == 1
    assert result["companies"]["X"]["normalized_delay"] == pytest.approx(0.2)
    assert result["companies"]["Y"]["travel_time_mean_s"] == pytest.approx(150.0)


def test_incomplete_flight_is_not_used_in_mean():
    result = calculate_metrics(
        [],
        [
            {"company": "X", "start_s": 0, "end_s": 100, "solo_time_s": 80},
            {"company": "X", "start_s": 0, "end_s": None, "solo_time_s": 80},
        ],
    )
    assert result["companies"]["X"]["completed_flights"] == 1
    assert result["companies"]["X"]["incomplete_flights"] == 1
    assert result["companies"]["X"]["travel_time_mean_s"] == pytest.approx(100)


def test_missing_solo_time_excludes_only_normalized_delay():
    result = calculate_metrics(
        [],
        [{"company": "X", "start_s": 0, "end_s": 100}],
    )

    assert result["companies"]["X"]["travel_time_mean_s"] == pytest.approx(100)
    assert result["companies"]["X"]["normalized_delay"] is None


def test_invalid_flight_duration_raises():
    with pytest.raises(ValueError):
        calculate_metrics(
            [], [{"company": "X", "start_s": 10, "end_s": 5, "solo_time_s": 8}]
        )


def test_zero_solo_time_is_rejected():
    with pytest.raises(ValueError, match="solo_time_s must be greater than zero"):
        calculate_metrics(
            [], [{"company": "X", "start_s": 0, "end_s": 100, "solo_time_s": 0}]
        )


@pytest.mark.parametrize("company", [None, ""])
def test_missing_company_is_rejected(company):
    with pytest.raises(ValueError, match="non-empty 'company'"):
        calculate_metrics(
            [{"company": company, "flags": []}],
            [],
        )


def test_safety_events_are_deduplicated_when_ids_exist():
    result = calculate_metrics(
        [
            {"company": "X", "flags": ["NMAC"], "encounter_id": "e1"},
            {"company": "Y", "flags": ["NMAC"], "encounter_id": "e1"},
            {"company": "X", "flags": ["LoWC"], "event_id": "e2"},
            {"company": "X", "flags": ["LoWC"], "event_id": "e2"},
            {"company": "Y", "flags": ["NMAC"]},
            {"company": "Y", "flags": ["NMAC"]},
        ],
        [],
    )

    assert result["safety"]["nmac_count"] == 3
    assert result["safety"]["lowc_count"] == 1
    assert result["safety"]["nmac_by_company"] == {"X": 1, "Y": 3}
    assert result["safety"]["lowc_by_company"] == {"X": 1}
    assert result["safety"]["unique_identified_safety_events"] == 2


def test_holm_correction():
    corrected = holm_correction({"a": 0.01, "b": 0.03, "c": 0.04})
    assert corrected == {
        "a": pytest.approx(0.03),
        "b": pytest.approx(0.06),
        "c": pytest.approx(0.06),
    }


def test_mann_whitney_reports_effect_size():
    result = mann_whitney_comparison([4, 5, 6], [1, 2, 3], name_a="F1", name_b="B1")
    assert result["rank_biserial_effect"] == pytest.approx(1.0)
    assert 0 <= result["p_value"] <= 1


def test_compare_to_baseline_returns_holm_p_values():
    results = compare_to_baseline(
        {"B1": [1, 2, 3, 4], "F1": [5, 6, 7, 8], "K2": [4, 5, 6, 7]},
        baseline="B1",
    )
    assert len(results) == 2
    assert all("p_value_holm" in row for row in results)
    assert all("significant_after_holm" in row for row in results)


def test_plots_render_and_save_all_three_outputs(tmp_path):
    metrics = {
        "companies": {"X": {"normalized_delay": 0.2}},
        "safety": {"nmac_count": 1, "lowc_count": 2},
    }

    delay_path = tmp_path / "delay.png"
    safety_path = tmp_path / "safety.png"
    credit_path = tmp_path / "credit.png"
    delay_fig = plot_delay_by_company({"B1": metrics}, output_path=delay_path)
    safety_fig = plot_nmac_by_setup({"B1": metrics}, output_path=safety_path)
    credit_fig = plot_credit_balances(
        [
            {"time_s": 60, "company": "X", "balance": 2},
            {"time_s": 0, "company": "X", "balance": 1},
        ],
        output_path=credit_path,
    )

    assert list(delay_fig.axes[0].lines[0].get_ydata()) == [0.2]
    assert [bar.get_height() for bar in safety_fig.axes[0].patches] == [1, 2]
    assert list(credit_fig.axes[0].lines[0].get_xdata()) == [0.0, 60.0]
    assert all(
        path.stat().st_size > 0 for path in (delay_path, safety_path, credit_path)
    )
