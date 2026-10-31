# p2a: diagnose before agentifying

**Find out why a scientific code repository can't be turned into an AI tool, and what to do about it.**

## The idea in one minute

[Paper2Agent](https://github.com/jmiao24/Paper2Agent) (Miao et al., *Nature* 2026) takes the code
published with a scientific paper and turns it into tools an AI assistant can use. It works well
when the code looks like a clean software library with tutorials. On 100 computational-biology
papers it succeeded on 74. The other 26 were set aside without a diagnosis.

They fail for very different reasons:

| Why it fails | Share of the 26 |
| --- | --- |
| There is no runnable code at all | 34% |
| The data or trained models the code needs are missing | 31% |
| The software environment won't install or run | 23% |
| The code is one long script that only works for that one paper | 12% |

Treating all of these the same way wastes effort. **p2a looks at a repository first, works out
what kind it is and what is missing, and then picks a strategy that fits.** A one-off analysis
script doesn't need to become a library. It just needs to be rerunnable with its settings exposed.

## How it sorts repositories

| Type | What it looks like | What p2a aims to produce |
| --- | --- | --- |
| `library` | Installable package with tutorials | Reusable tools (Paper2Agent already handles this) |
| `stepwise` | Scripts or notebooks with separable steps | A tool for each reusable step, plus one that reruns the rest |
| `monolithic` | One long script with hard-coded values | A single `reproduce(data)` tool with those values made adjustable |
| `missing_data` | Code is there, data or models are not | Recover them from DOI, Zenodo, GEO, Hugging Face…, or fall back to synthetic data |
| `text_only` | No code, only the paper | A searchable layer over the paper and its supplements |

A repository can belong to more than one type. p2a reports a main type plus a list of what is
missing.

## Try it

You need Python 3.10 or newer.

```
git clone git@github.com:GiacomoSpiotta/p2a.git
cd p2a
python -m venv .venv && source .venv/bin/activate
pip install -e .

p2a diagnose /path/to/some/repository          # readable summary
p2a diagnose /path/to/some/repository --json   # machine-readable card
```

The diagnosis only reads files. It never runs the code it inspects. Example output:

```
repository:  p2a
class:       stepwise   recoverability: medium
missing:     examples
why:
  - no tutorial, notebook or example
  - separable steps: functions, argparse or config files

strategy:    stepwise
produces:    tools for the steps with clear inputs and outputs; one `run_rest` tool for the paper-specific part
```

## Project status

This is an **early research prototype**.

- ✅ Static diagnosis and classification
- 🚧 Strategies are outlined but not implemented yet. `monolithic` comes first.
- 🔜 Dynamic diagnosis: actually try to install and run the code, with an AI agent
- 🔜 Run on the full Paper2Agent sample and publish the breakdown of failure causes

The full reasoning is in [`docs/strategy.md`](docs/strategy.md), and the test plan is in
[`docs/test-plan.md`](docs/test-plan.md).

## Repository layout

- `src/p2a/`: the diagnosis (`diagnose.py`), the classification rules (`classify.py`), one plan per type (`strategies/`) and the output card (`report.py`)
- `prompts/`: instructions for the AI agent that will run the dynamic diagnosis
- `eval/`: the evaluation sample and the numbers to report
- `tests/`: unit tests (`pytest`)

## Contributing

Feedback is very welcome, especially from people who have tried to reuse code from a paper and
got stuck. Open an issue with the repository link and what went wrong. Each case like that is a
data point for this project.
