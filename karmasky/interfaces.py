"""Typed contracts between KarmaSky modules (03_GETTING_STARTED.md, Section 4).

These placeholders let the four members work in parallel. Agree on them in the Week 1
team meeting before writing module code. Arrays are typed as plain sequences here so
this file imports with the standard library only; implementations may use numpy arrays
or torch tensors with the same shapes.

Owner: all members (agreed in the Week 1 team meeting); Team lead keeps it up to date.
TODO: fill D_OWN and D_NB (see below) and confirm every contract.
Status: placeholder, no implementation yet.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import IntEnum
from typing import Dict, List, Literal, Mapping, Optional, Sequence, Tuple

DroneId = str
CompanyId = str

# TODO: per-drone feature sizes. 03 Section 4 says these follow Sharifi et al. and
# Brittain and Wei; Member 2 fills them in. Sharifi et al. Sec. III-C.1 lists 4 ownship
# features (distance to next waypoint, speed, heading, acceleration) and 4 per intruder
# (ownship-to-intruder distance, speed, heading, acceleration). Check against privacy
# fix 2 in 06_DESIGN_UPDATES.md (relative inputs only) before fixing the numbers.
D_OWN: Optional[int] = None
D_NB: Optional[int] = None


# env -> agents: obs[drone_id] = {"own": array(d_own), "neighbors": array(n, d_nb), "mask": array(n)}
@dataclass
class Observation:
    own: Sequence[float]                 # length D_OWN
    neighbors: Sequence[Sequence[float]]  # n x D_NB, n varies per step
    mask: Sequence[bool]                 # length n; True where a neighbor slot is real


Observations = Dict[DroneId, Observation]


# agents -> env: action[drone_id] in {0: slow, 1: hold, 2: speed up} plus scores[drone_id] (3 numbers)
class Action(IntEnum):
    SLOW = 0
    HOLD = 1
    SPEED_UP = 2


ActionScores = Tuple[float, float, float]


@dataclass
class AgentOutput:
    action: Action
    scores: ActionScores


AgentOutputs = Dict[DroneId, AgentOutput]


# env -> safety: positions, velocities, max speed and acceleration of every aircraft
@dataclass
class AircraftState:
    position: Tuple[float, ...]   # TODO: frame and units (2D or 3D) to be agreed by Members 1 and 4
    velocity: Tuple[float, ...]
    max_speed: float              # m/s
    max_accel: float              # m/s^2
    manned: bool = False          # True for the manned helicopter ([OPEN] M3 in 07)


AircraftStates = Dict[DroneId, AircraftState]


# safety -> agents/env: allowed[drone_id] = [bool, bool, bool]  (slow, hold, speed up)
AllowedActions = Tuple[bool, bool, bool]
AllowedMap = Dict[DroneId, AllowedActions]


# karma -> env: priority[drone_id] in {"go", "yield", None} for each open contest
Priority = Optional[Literal["go", "yield"]]
PriorityMap = Dict[DroneId, Priority]


# agents -> federation: summarizer.state_dict() changes since last round.
# Only the shared parts (neighbor encoder, attention, intent head) per 06 Update 2;
# which parts are shared is still [OPEN] (T3 in 07).
@dataclass
class SharedUpdate:
    company: CompanyId
    round_index: int
    delta: Mapping[str, Sequence[float]]   # parameter name -> flattened change; TODO: tensor type


# federation -> agents: merged summarizer weights
@dataclass
class MergedWeights:
    round_index: int
    weights: Mapping[str, Sequence[float]]  # parameter name -> flattened values; TODO: tensor type


# federation -> karma: contribution score per company -> credits minted
@dataclass
class ContributionScores:
    round_index: int
    raw: Dict[CompanyId, float]        # this round's Shapley value
    smoothed: Dict[CompanyId, float]   # after 0.8 / 0.2 smoothing


# env -> eval: per-step log and per-flight log
@dataclass
class StepLog:
    time_s: float
    drone: DroneId
    company: CompanyId
    position: Tuple[float, ...]
    action: Action
    min_distance_m: float
    flags: List[str] = field(default_factory=list)  # e.g. "NMAC", "LoWC", "shield", "contest"; TODO: fix the list


@dataclass
class FlightLog:
    drone: DroneId
    company: CompanyId
    start_s: float
    end_s: Optional[float]   # None if the flight did not finish
    solo_time_s: Optional[float]
