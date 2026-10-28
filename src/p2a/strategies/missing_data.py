from ..report import Diagnosis
from .base import Plan


def missing_data_plan(d: Diagnosis) -> Plan:
    """Code is there, data is not: try to recover it; if that fails, show the code
    runs on synthetic data with the same schema."""
    return Plan(
        strategy="missing_data",
        produces="recovered and mounted data, or a synthetic data generator with the schema inferred from the code",
        validation="runs without errors; output shape (dimensions, sign, order of magnitude) consistent with the paper's figures and tables",
        steps=[
            "list the files the code reads and cannot find (dynamic diagnosis)",
            "search the paper and the README for data citations: DOI, Zenodo, Figshare, Dataverse, GEO/SRA, Hugging Face",
            "resolve and download; check that names and columns match what the code expects",
            "if not recoverable: infer the schema from the reads in the code and generate a small synthetic dataset",
            "run; if it runs, continue with the structural strategy (library, stepwise or monolithic) marking the tests as 'execution only'",
        ],
    )
