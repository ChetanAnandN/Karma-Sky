"""Smoke test: the package and every placeholder module import.

Owner: Team lead. Uses the standard library only, so it runs before BlueSky or torch are installed.
"""

import importlib

import pytest

MODULES = [
    "karmasky",
    "karmasky.interfaces",
    "karmasky.env.scenario",
    "karmasky.env.bluesky_wrapper",
    "karmasky.env.observations",
    "karmasky.env.rewards",
    "karmasky.env.helicopter",
    "karmasky.agents.summarizer",
    "karmasky.agents.decider",
    "karmasky.agents.ppo",
    "karmasky.agents.buffer",
    "karmasky.federation.referee",
    "karmasky.federation.aggregation",
    "karmasky.federation.shapley",
    "karmasky.federation.exam_suite",
    "karmasky.federation.integrity",
    "karmasky.karma.ledger",
    "karmasky.karma.bidding",
    "karmasky.safety.shield",
    "karmasky.attacks.free_rider",
    "karmasky.attacks.exam_gaming",
    "karmasky.eval.metrics",
    "karmasky.eval.stats",
    "karmasky.eval.plots",
]


@pytest.mark.parametrize("name", MODULES)
def test_module_imports(name):
    importlib.import_module(name)
