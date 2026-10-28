from ..report import Diagnosis
from .base import Plan


def text_only_plan(d: Diagnosis) -> Plan:
    """No code: resource layer only, as Paper2Agent already does."""
    return Plan(
        strategy="text_only",
        produces="MCP resources: paper text, supplements, tables",
        validation="synthesis questions with known answers",
        steps=["extract text and tables", "register as MCP resources", "no tools"],
    )
