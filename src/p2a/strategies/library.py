from ..report import Diagnosis
from .base import Plan


def library_plan(d: Diagnosis) -> Plan:
    """Libreria con tutorial: delega a Paper2Agent così com'è."""
    return Plan(
        strategy="library",
        produces="tool MCP riutilizzabili, uno per operazione del tutorial",
        validation="test sugli esempi del tutorial (numeri entro il 3%, figure per hash)",
        steps=[
            "installa l'ambiente dai file di installazione",
            "esegui i tutorial e salva gli output di riferimento",
            "estrai le funzioni con i valori cablati esposti come parametri",
            "genera e ripeti i test fino a sei tentativi; scarta quello che non passa",
            "assembla il server MCP",
        ],
    )
