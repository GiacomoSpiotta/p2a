"""One strategy per class. Each strategy takes a diagnosis and produces a plan.

Strategies are stubs: they describe what to produce and how to validate it.
The actual execution (extraction, tests, MCP server) is the project's next step.
"""

from ..report import Diagnosis
from .base import Plan
from .library import library_plan
from .stepwise import stepwise_plan
from .monolithic import monolithic_plan
from .missing_data import missing_data_plan
from .text_only import text_only_plan

STRATEGIES = {
    "library": library_plan,
    "stepwise": stepwise_plan,
    "monolithic": monolithic_plan,
    "missing_data": missing_data_plan,
    "text_only": text_only_plan,
}


def plan_for(d: Diagnosis) -> Plan:
    return STRATEGIES[d.primary_class](d)
