"""Rules that turn signals into a class and a list of missing items.

The rules are deliberately simple and readable: they are a starting point for the
static diagnosis. The dynamic diagnosis (with an agent) confirms or corrects them.
"""

from .report import Signals, Diagnosis

CLASSES = ("library", "stepwise", "monolithic", "missing_data", "text_only")


def classify(repo: str, s: Signals) -> Diagnosis:
    why: list[str] = []
    missing: list[str] = []

    code_files = sum(v for k, v in s.languages.items() if k != "notebook")
    if code_files == 0 and s.notebooks == 0:
        return Diagnosis(repo, s, "text_only", ["code"], "none",
                         ["no code file or notebook"])

    installable = bool(s.install_files)
    has_examples = bool(s.tutorial_files) or s.notebooks > 0
    if not installable:
        missing.append("install_spec")
        why.append("no install file (pyproject, requirements, DESCRIPTION...)")
    if not has_examples:
        missing.append("examples")
        why.append("no tutorial, notebook or example")
    if s.data_files == 0 and not s.data_links:
        missing.append("data")
        why.append("no data in the repo and no link to external data")
    elif s.data_files == 0 and s.data_links:
        why.append(f"external data referenced ({len(s.data_links)} links): to be verified")
    if s.absolute_paths > 0:
        missing.append("portable_paths")
        why.append(f"{s.absolute_paths} hard-coded absolute paths")

    # Structure: library, separable steps or monolith.
    scripts = s.functions_per_script
    n_scripts = len(scripts)
    avg_funcs = (sum(scripts.values()) / n_scripts) if n_scripts else 0.0
    many_funcs = sum(1 for v in scripts.values() if v >= 3)

    if installable and has_examples and (many_funcs >= 2 or s.has_tests):
        primary = "library"
        why.append("installable, with examples and code organized in functions")
    elif many_funcs >= 1 or s.uses_argparse or s.config_files:
        primary = "stepwise"
        why.append("separable steps: functions, argparse or config files")
    else:
        primary = "monolithic"
        why.append(f"unstructured script (average {avg_funcs:.1f} functions per file)")

    if "data" in missing and primary != "text_only":
        primary = "missing_data"

    if primary == "library" and not missing:
        recoverability = "high"
    elif primary in ("stepwise", "monolithic") and "data" not in missing:
        recoverability = "medium"
    else:
        recoverability = "low"

    return Diagnosis(repo, s, primary, missing, recoverability, why)
