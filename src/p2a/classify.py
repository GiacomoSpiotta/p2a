"""Regole che trasformano i segnali in una classe e in una lista di mancanze.

Le regole sono volutamente semplici e leggibili: sono un punto di partenza per la
diagnosi statica. La diagnosi dinamica (con agente) le conferma o le corregge.
"""

from .report import Signals, Diagnosis

CLASSES = ("library", "stepwise", "monolithic", "missing_data", "text_only")


def classify(repo: str, s: Signals) -> Diagnosis:
    why: list[str] = []
    missing: list[str] = []

    code_files = sum(v for k, v in s.languages.items() if k != "notebook")
    if code_files == 0 and s.notebooks == 0:
        return Diagnosis(repo, s, "text_only", ["code"], "none",
                         ["nessun file di codice o notebook"])

    installable = bool(s.install_files)
    has_examples = bool(s.tutorial_files) or s.notebooks > 0
    if not installable:
        missing.append("install_spec")
        why.append("nessun file di installazione (pyproject, requirements, DESCRIPTION...)")
    if not has_examples:
        missing.append("examples")
        why.append("nessun tutorial, notebook o esempio")
    if s.data_files == 0 and not s.data_links:
        missing.append("data")
        why.append("nessun dato nel repo e nessun link a dati esterni")
    elif s.data_files == 0 and s.data_links:
        why.append(f"dati esterni referenziati ({len(s.data_links)} link): da verificare")
    if s.absolute_paths > 0:
        missing.append("portable_paths")
        why.append(f"{s.absolute_paths} percorsi assoluti cablati")

    # Struttura: libreria, passi separabili o monolite.
    scripts = s.functions_per_script
    n_scripts = len(scripts)
    avg_funcs = (sum(scripts.values()) / n_scripts) if n_scripts else 0.0
    many_funcs = sum(1 for v in scripts.values() if v >= 3)

    if installable and has_examples and (many_funcs >= 2 or s.has_tests):
        primary = "library"
        why.append("installabile, con esempi e codice organizzato in funzioni")
    elif many_funcs >= 1 or s.uses_argparse or s.config_files:
        primary = "stepwise"
        why.append("passi separabili: funzioni, argparse o file di configurazione")
    else:
        primary = "monolithic"
        why.append(f"script senza struttura (media {avg_funcs:.1f} funzioni per file)")

    if "data" in missing and primary != "text_only":
        primary = "missing_data"

    if primary == "library" and not missing:
        recoverability = "high"
    elif primary in ("stepwise", "monolithic") and "data" not in missing:
        recoverability = "medium"
    else:
        recoverability = "low"

    return Diagnosis(repo, s, primary, missing, recoverability, why)
