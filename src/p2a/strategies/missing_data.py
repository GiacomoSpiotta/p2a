from ..report import Diagnosis
from .base import Plan


def missing_data_plan(d: Diagnosis) -> Plan:
    """Il codice c'è, i dati no: prova a recuperarli; se non ci riesci, prova che
    il codice gira su dati sintetici con lo stesso schema."""
    return Plan(
        strategy="missing_data",
        produces="dati recuperati e montati, oppure un generatore di dati sintetici con lo schema inferito dal codice",
        validation="esecuzione senza errori; forma dell'output coerente (dimensioni, segno, ordine di grandezza) con figure e tabelle del paper",
        steps=[
            "elenca i file che il codice legge e non trova (diagnosi dinamica)",
            "cerca nel paper e nel README citazioni di dati: DOI, Zenodo, Figshare, Dataverse, GEO/SRA, Hugging Face",
            "risolvi e scarica; verifica che i nomi e le colonne combacino con quelli attesi dal codice",
            "se non recuperabile: inferisci lo schema dalle letture nel codice e genera un dato sintetico piccolo",
            "esegui; se gira, procedi con la strategia strutturale (library, stepwise o monolithic) marcando i test come 'solo esecuzione'",
        ],
    )
