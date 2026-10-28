# p2a: diagnose before agentifying

Concept for a contribution on top of Paper2Agent (Miao et al., Nature 2026): instead of
asking every scientific repository to behave like a library with tutorials, diagnose it first
and pick a strategy for the shape it actually has.

The full strategy is in `docs/strategy.md`.

## What is here

- `src/p2a/diagnose.py`: static diagnosis, reads the files and produces signals. Nothing is executed.
- `src/p2a/classify.py`: rules that assign a class (`library`, `stepwise`, `monolithic`,
  `missing_data`, `text_only`) and the list of missing items.
- `src/p2a/strategies/`: one plan per class. Stubs: they say what to produce and how to validate it.
- `src/p2a/report.py`: the JSON card, which is the project's data.
- `prompts/diagnose.md`: prompt for the dynamic-diagnosis sub-agent (Claude Code).
- `eval/`: sample and the numbers to report.

## Usage

```
uv venv && source .venv/bin/activate
uv pip install -e .
p2a diagnose /path/to/a/repo
p2a diagnose /path/to/a/repo --json
pytest
```

## Next steps

1. Run the static diagnosis over the 110 repositories of the Paper2Agent sample.
2. Implement the dynamic diagnosis as a sub-agent.
3. Implement the `monolithic` strategy, which is the simplest.
