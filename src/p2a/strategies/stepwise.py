from ..report import Diagnosis
from .base import Plan


def stepwise_plan(d: Diagnosis) -> Plan:
    """Script with separable steps: tools for the steps that generalize, plus one
    tool that reruns the rest."""
    return Plan(
        strategy="stepwise",
        produces="tools for the steps with clear inputs and outputs; one `run_rest` tool for the paper-specific part",
        validation="per-step tests where an intermediate output exists; final comparison against the paper's figures and tables",
        steps=[
            "run the script on the original data and record every file read and written",
            "segment on I/O boundaries: each stretch between a read and a write is a candidate step",
            "for each step ask: does it make sense on different data? if yes, a tool with parameters; if not, it stays in `run_rest`",
            "test: the step reproduces the original intermediate output",
        ],
    )
