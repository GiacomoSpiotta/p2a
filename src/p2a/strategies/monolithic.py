from ..report import Diagnosis
from .base import Plan


def monolithic_plan(d: Diagnosis) -> Plan:
    """Single sequence: one tool that reruns the analysis, with hard-coded values
    exposed as parameters. The simplest case and the most neglected."""
    return Plan(
        strategy="monolithic",
        produces="one `reproduce(data_path, **params)` tool that reruns everything",
        validation="outputs (files, numbers, figures) match the original ones",
        steps=[
            "run the script on the original data and save every output",
            "replace absolute paths with parameters; list the hard-coded constants and expose them as parameters with defaults",
            "wrap in a function; file-based inputs and outputs",
            "test: rerunning with the defaults yields the original outputs",
            "register as a single MCP tool, with the parameter list in the docstring",
        ],
    )
