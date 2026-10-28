from ..report import Diagnosis
from .base import Plan


def text_only_plan(d: Diagnosis) -> Plan:
    """Nessun codice: solo strato di risorse, come fa già Paper2Agent."""
    return Plan(
        strategy="text_only",
        produces="risorse MCP: testo del paper, supplementari, tabelle",
        validation="domande di sintesi con risposta nota",
        steps=["estrai testo e tabelle", "registra come risorse MCP", "nessun tool"],
    )
