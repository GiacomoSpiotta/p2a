"""Scheda di diagnosi di un repository.

La scheda è il dato principale del progetto: aggregata su un campione di paper
dà la distribuzione delle cause di fallimento.
"""

from dataclasses import dataclass, field, asdict
import json


@dataclass
class Signals:
    """Segnali letti dai file del repository, senza eseguire nulla."""

    languages: dict[str, int] = field(default_factory=dict)
    install_files: list[str] = field(default_factory=list)
    has_dockerfile: bool = False
    has_tests: bool = False
    notebooks: int = 0
    tutorial_files: list[str] = field(default_factory=list)
    entry_scripts: list[str] = field(default_factory=list)
    uses_argparse: bool = False
    config_files: list[str] = field(default_factory=list)
    absolute_paths: int = 0
    data_files: int = 0
    data_links: list[str] = field(default_factory=list)
    functions_per_script: dict[str, int] = field(default_factory=dict)


@dataclass
class Diagnosis:
    repo: str
    signals: Signals
    primary_class: str
    missing: list[str]
    recoverability: str
    rationale: list[str]

    def to_json(self) -> str:
        return json.dumps(asdict(self), indent=2, ensure_ascii=False)
