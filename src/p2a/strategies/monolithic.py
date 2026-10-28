from ..report import Diagnosis
from .base import Plan


def monolithic_plan(d: Diagnosis) -> Plan:
    """Sequenza unica: un solo tool che riesegue l'analisi, con i valori cablati
    esposti come parametri. È il caso più semplice e il più trascurato."""
    return Plan(
        strategy="monolithic",
        produces="un tool `reproduce(data_path, **params)` che riesegue tutto",
        validation="gli output (file, numeri, figure) corrispondono a quelli originali",
        steps=[
            "esegui lo script sui dati originali e salva tutti gli output",
            "sostituisci i percorsi assoluti con parametri; elenca le costanti cablate e esponile come parametri con default",
            "incapsula in una funzione; input e output su file",
            "test: rieseguendo con i default si ottengono gli output originali",
            "registra come tool MCP unico, con la lista dei parametri nella docstring",
        ],
    )
