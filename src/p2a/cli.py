"""Usage: p2a diagnose <repo_folder> [--json]

Prints the diagnosis card and the plan of the assigned strategy.
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
        print(f"not a folder: {root}")
        return 2

    signals = diagnose_static(root)
    d = classify(root.name, signals)
    plan = plan_for(d)

    if "--json" in argv:
        print(json.dumps({"diagnosis": asdict(d), "plan": asdict(plan)}, indent=2))
        return 0

    print(f"repository:  {d.repo}")
    print(f"class:       {d.primary_class}   recoverability: {d.recoverability}")
    print(f"missing:     {', '.join(d.missing) or 'none'}")
    print("why:")
    for r in d.rationale:
        print(f"  - {r}")
    print(f"\nstrategy:    {plan.strategy}")
    print(f"produces:    {plan.produces}")
    print(f"validation:  {plan.validation}")
    print("steps:")
    for i, step in enumerate(plan.steps, 1):
        print(f"  {i}. {step}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
