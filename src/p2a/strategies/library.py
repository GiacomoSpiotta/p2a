from ..report import Diagnosis
from .base import Plan


def library_plan(d: Diagnosis) -> Plan:
    """Library with tutorials: delegate to Paper2Agent as is."""
    return Plan(
        strategy="library",
        produces="reusable MCP tools, one per tutorial operation",
        validation="tests on the tutorial examples (numbers within 3%, figures by perceptual hash)",
        steps=[
            "install the environment from the install files",
            "run the tutorials and save the reference outputs",
            "extract the functions with hard-coded values exposed as parameters",
            "generate and rerun tests up to six attempts; drop what does not pass",
            "assemble the MCP server",
        ],
    )
