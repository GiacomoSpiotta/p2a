from ..report import Diagnosis
from .base import Plan


def stepwise_plan(d: Diagnosis) -> Plan:
    """Script con passi separabili: tool per i passi che generalizzano, più un tool
    che riesegue il resto."""
    return Plan(
        strategy="stepwise",
        produces="tool per i passi con input e output chiari; un tool `run_rest` per la parte legata al paper",
        validation="test per passo dove esiste un output intermedio; confronto finale con figure e tabelle del paper",
        steps=[
            "esegui lo script sui dati originali e registra ogni file letto e scritto",
            "segmenta per confini di I/O: ogni tratto tra una lettura e una scrittura è un passo candidato",
            "per ogni passo, chiedi: ha senso su dati diversi? se sì, tool con parametri; se no, resta in `run_rest`",
            "test: il passo riproduce l'output intermedio originale",
        ],
    )
