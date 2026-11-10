"""KarmaSky evaluation metrics.

Accepts StepLog/FlightLog dataclass instances from karmasky.interfaces or
plain dictionaries (for example, rows loaded from CSV).

Important counting convention:
The current StepLog interface has no encounter/event ID, so flagged records
cannot be reliably deduplicated unless logs provide an optional encounter_id
or event_id.
"""

from __future__ import annotations

import math
from collections import defaultdict
from collections.abc import Iterable, Mapping
from typing import Any


def _get(record: Any, key: str, default: Any = None) -> Any:
    """Read a field from either a mapping/CSV row or a dataclass object."""
    if isinstance(record, Mapping):
        return record.get(key, default)
    return getattr(record, key, default)


def _as_float(value: Any, field_name: str, *, allow_none: bool = False) -> float | None:
    if value is None or value == "":
        if allow_none:
            return None
        raise ValueError(f"Missing required numeric field: {field_name}")
    try:
        number = float(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(f"Field {field_name!r} must be numeric; got {value!r}") from exc
    if not math.isfinite(number):
        raise ValueError(f"Field {field_name!r} must be finite; got {value!r}")
    return number


def _flags(value: Any) -> set[str]:
    """Normalize flags from a list or CSV text such as 'NMAC|shield'."""
    if value is None or value == "":
        return set()
    if isinstance(value, str):
        parts = value.replace(";", "|").replace(",", "|").split("|")
    else:
        parts = value
    return {str(item).strip().upper() for item in parts if str(item).strip()}


def _company_name(record: Any, record_type: str) -> str:
    value = _get(record, "company")
    company = "" if value is None else str(value).strip()
    if not company:
        raise ValueError(f"Every {record_type}-log row must contain a non-empty 'company'")
    return company


def _event_id(record: Any) -> str | None:
    for key in ("encounter_id", "event_id"):
        value = _get(record, key)
        if value is not None and str(value).strip():
            return str(value).strip()
    return None


def calculate_metrics(step_logs: Iterable[Any], flight_logs: Iterable[Any]) -> dict[str, Any]:
    """Calculate safety, efficiency and fairness metrics from raw logs.

    Expected StepLog fields: time_s, drone, company, flags. Optional
    encounter_id/event_id values deduplicate repeated safety records.
    Expected FlightLog fields: drone, company, start_s, end_s, solo_time_s.

    Incomplete flights (end_s is None) are counted but excluded from travel-time
    averages. Normalized delay is calculated from the same completed flights
    that have a valid positive solo_time_s value. Rows without encounter IDs
    are counted as per-drone step-log records because StepLog has no event ID.
    """
    steps = list(step_logs)
    flights = list(flight_logs)

    nmac_by_company: dict[str, int] = defaultdict(int)
    lowc_by_company: dict[str, int] = defaultdict(int)
    shield_by_company: dict[str, int] = defaultdict(int)
    step_count_by_company: dict[str, int] = defaultdict(int)
    counted_safety_events: set[tuple[str, str]] = set()
    counted_safety_events_by_company: set[tuple[str, str, str]] = set()
    identified_nmac_count = 0
    identified_lowc_count = 0
    unidentified_nmac_count = 0
    unidentified_lowc_count = 0
    companies: set[str] = set()

    for row in steps:
        company = _company_name(row, "step")
        companies.add(company)
        step_count_by_company[company] += 1
        row_flags = _flags(_get(row, "flags", []))
        event_id = _event_id(row)
        for flag, aliases, counts_by_company in (
            ("NMAC", {"NMAC"}, nmac_by_company),
            ("LOWC", {"LOWC", "LOWC_EVENT"}, lowc_by_company),
        ):
            if row_flags.intersection(aliases):
                event_key = (flag, event_id) if event_id is not None else None
                if event_key is None:
                    counts_by_company[company] += 1
                    if flag == "NMAC":
                        unidentified_nmac_count += 1
                    else:
                        unidentified_lowc_count += 1
                else:
                    company_event_key = (company, flag, event_id)
                    if company_event_key not in counted_safety_events_by_company:
                        counts_by_company[company] += 1
                        counted_safety_events_by_company.add(company_event_key)
                    if event_key not in counted_safety_events:
                        if flag == "NMAC":
                            identified_nmac_count += 1
                        else:
                            identified_lowc_count += 1
                        counted_safety_events.add(event_key)
        if "SHIELD" in row_flags or "SHIELD_INTERVENTION" in row_flags:
            shield_by_company[company] += 1

    shared_times: dict[str, list[float]] = defaultdict(list)
    paired_shared_times: dict[str, list[float]] = defaultdict(list)
    solo_times: dict[str, list[float]] = defaultdict(list)
    completed_by_company: dict[str, int] = defaultdict(int)
    incomplete_by_company: dict[str, int] = defaultdict(int)

    for row in flights:
        company = _company_name(row, "flight")
        companies.add(company)

        start = _as_float(_get(row, "start_s"), "start_s")
        end = _as_float(_get(row, "end_s"), "end_s", allow_none=True)
        solo = _as_float(_get(row, "solo_time_s"), "solo_time_s", allow_none=True)
        if solo is not None and solo <= 0:
            raise ValueError(f"solo_time_s must be greater than zero; got {solo}")

        if end is None:
            incomplete_by_company[company] += 1
            continue
        if end < start:
            raise ValueError(
                f"Flight end_s ({end}) is earlier than start_s ({start}) for company {company!r}"
            )

        duration = end - start
        completed_by_company[company] += 1
        shared_times[company].append(duration)
        if solo is not None:
            paired_shared_times[company].append(duration)
            solo_times[company].append(solo)

    company_metrics: dict[str, dict[str, Any]] = {}
    normalized_delays: dict[str, float] = {}
    mean_shared_times: dict[str, float] = {}

    for company in sorted(companies):
        shared_values = shared_times.get(company, [])
        paired_shared = paired_shared_times.get(company, [])
        solo_values = solo_times.get(company, [])
        mean_shared = sum(shared_values) / len(shared_values) if shared_values else None
        mean_paired_shared = (
            sum(paired_shared) / len(paired_shared) if paired_shared else None
        )
        mean_solo = sum(solo_values) / len(solo_values) if solo_values else None
        normalized_delay = None
        if mean_paired_shared is not None and mean_solo is not None:
            normalized_delay = (mean_paired_shared - mean_solo) / mean_solo
            normalized_delays[company] = normalized_delay
        if mean_shared is not None:
            mean_shared_times[company] = mean_shared

        total_steps = step_count_by_company.get(company, 0)
        shield_count = shield_by_company.get(company, 0)
        company_metrics[company] = {
            "completed_flights": completed_by_company.get(company, 0),
            "incomplete_flights": incomplete_by_company.get(company, 0),
            "travel_time_mean_s": mean_shared,
            "solo_time_mean_s": mean_solo,
            "normalized_delay": normalized_delay,
            "nmac_count": nmac_by_company.get(company, 0),
            "lowc_count": lowc_by_company.get(company, 0),
            "shield_interventions": shield_count,
            "shield_intervention_rate": shield_count / total_steps if total_steps else None,
        }

    delays = list(normalized_delays.values())
    delay_gap = max(delays) - min(delays) if len(delays) >= 2 else None
    worst_off_delay = max(delays) if delays else None

    # Sharifi's Ft is kept separate from normalized-delay fairness. It is
    # calculated from mean shared travel times for exactly two companies.
    ft = None
    ft_companies: list[str] = []
    if len(mean_shared_times) == 2:
        ft_companies = sorted(mean_shared_times)
        time_a = mean_shared_times[ft_companies[0]]
        time_b = mean_shared_times[ft_companies[1]]
        denominator = max(time_a, time_b)
        if denominator > 0:
            ft = (1.0 - abs(time_a - time_b) / denominator) * 100.0

    total_steps = len(steps)
    total_shield = sum(shield_by_company.values())
    return {
        "safety": {
            "nmac_count": identified_nmac_count + unidentified_nmac_count,
            "lowc_count": identified_lowc_count + unidentified_lowc_count,
            "shield_interventions": total_shield,
            "shield_intervention_rate": total_shield / total_steps if total_steps else None,
            "nmac_by_company": dict(sorted(nmac_by_company.items())),
            "lowc_by_company": dict(sorted(lowc_by_company.items())),
            "counting_unit": (
                "unique identified safety events when encounter_id/event_id is present; "
                "otherwise flagged per-drone step-log records"
            ),
            "unique_identified_safety_events": len(counted_safety_events),
            "company_event_counts_are_inclusive": True,
            "company_count_note": (
                "An identified event involving multiple companies is counted once per "
                "involved company, while the overall count remains unique."
            ),
        },
        "companies": company_metrics,
        "fairness": {
            "normalized_delay_gap": delay_gap,
            "worst_off_delay": worst_off_delay,
            "sharifi_ft_percent": ft,
            "ft_company_order": ft_companies,
        },
        "metadata": {
            "step_log_rows": total_steps,
            "flight_log_rows": len(flights),
            "ft_note": "Ft is calculated only when exactly two companies have completed-flight travel times.",
        },
    }
