"""Uso: p2a diagnose <cartella_repo> [--json]

Stampa la scheda di diagnosi e il piano della strategia assegnata.
"""

import sys
from pathlib import Path
from dataclasses import asdict
import json

from .diagnose import diagnose_static
from .classify import classify
from .strategies import plan_for


def main(argv: list[str] | None = None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    if len(argv) < 2 or argv[0] != "diagnose":
        print(__doc__)
        return 2
    root = Path(argv[1]).resolve()
    if not root.is_dir():
        print(f"non è una cartella: {root}")
        return 2

    signals = diagnose_static(root)
    d = classify(root.name, signals)
    plan = plan_for(d)

    if "--json" in argv:
        print(json.dumps({"diagnosis": asdict(d), "plan": asdict(plan)}, indent=2, ensure_ascii=False))
        return 0

    print(f"repository: {d.repo}")
    print(f"classe:     {d.primary_class}   recuperabilità: {d.recoverability}")
    print(f"mancanze:   {', '.join(d.missing) or 'nessuna'}")
    print("perché:")
    for r in d.rationale:
        print(f"  - {r}")
    print(f"\nstrategia:  {plan.strategy}")
    print(f"produce:    {plan.produces}")
    print(f"validazione:{plan.validation}")
    print("passi:")
    for i, step in enumerate(plan.steps, 1):
        print(f"  {i}. {step}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
