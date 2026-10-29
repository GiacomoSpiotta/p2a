# Strategy: diagnose before extracting

## Problem

Paper2Agent (Miao et al., Nature 2026) turns a scientific repository into an MCP server with
a single strategy: extract reusable functions from the executable tutorials, test them on the
tutorial's own examples, drop whatever fails. On 100 computational-biology papers it converts
74. The remaining 26 are discarded with no diagnosis: nobody knows why they fail or how much
is missing.

The stated causes are four: no executable code, data or models unavailable, environment that
cannot be rebuilt, scripts that do not generalize. The pipeline treats all of them the same
way, i.e. it asks every repository to behave like a library with tutorials.

## What the Paper2Agent repository already does (checked October 2026)

The repository is no longer the Python orchestrator described in the paper's Methods. It is a
skill for Claude Code or Codex (`skills/paper2agent/`) with three parts:

- `paper2mcp`: repository to MCP server. Sub-agents are markdown instruction files. Three
  routes by interface: Python library, R package, command line (CLI).
- `paper2skill`: paper PDF to a skill bundle, i.e. the text and supplements layer.
- `reports/agent-runs.json`: recorded workflow state with assignments, file hashes and
  **exclusions with reasons**.

Consequences for this concept:

- R is covered by a route; it is no longer an open gap.
- The CLI route covers scripts run from the command line with documented examples and real
  data. It does not cover scripts without a documented interface, and it explicitly refuses to
  substitute missing domain data with random tables: such tools are marked blocked and excluded.
- Every excluded tool already carries a reason. Measuring the distribution of failure causes
  can start from those records instead of from scratch.

So the open classes are `monolithic` (analysis scripts with no interface) and `missing_data`
(code present, data or models absent). The `library` class and the documented half of
`stepwise` are theirs.

## Idea

Add a diagnosis step before extraction and pick the strategy from its result. The repository
does not have to be a library: it has to be what it is.

Paper2Agent's extraction for libraries is left untouched (it works). What is added is what is
missing for the other shapes.

## Classes

| Class | How it is recognized | What is produced | Validation |
| --- | --- | --- | --- |
| `library` | installable package, API, tutorial or notebook with outputs | reusable tools (Paper2Agent) | tests on the tutorial examples |
| `stepwise` | script or notebook with separable steps (functions, cells with intermediate outputs) | tools for the steps that generalize, plus one tool that reruns the rest | per-step tests where an intermediate output exists; final comparison against the paper's figures |
| `monolithic` | single sequence, hard-coded values, no step makes sense on its own | one tool `reproduce(data)` with hard-coded values exposed as parameters | outputs compared against the original ones |
| `missing_data` | code is there but points at data or models that are neither present nor downloadable | recovery from DOI, Zenodo, Figshare, GEO, Hugging Face; fallback to synthetic data with the same schema | runs without errors, output shape checked |
| `text_only` | no code | resource layer (paper text and supplements, queryable) | synthesis questions |

Classes are not exclusive: a repository can be `stepwise` and `missing_data` at once. The
diagnosis returns a primary class plus the list of what is missing.

## Diagnosis

Two levels, in order of cost.

1. **Static** (seconds, no LLM): signals read from the files. Presence of pyproject, setup,
   requirements, environment.yml, DESCRIPTION, Dockerfile; notebooks and tutorials; tests;
   hard-coded absolute paths; data URLs and DOIs in the README; use of argparse or config
   files; languages. Produces a profile and a provisional class.
2. **Dynamic** (minutes, with an agent): try to install, run the tutorial or the main script,
   list the files the code tries to read and cannot find. Confirms or corrects the class and
   estimates recoverability.

The output is one JSON card per repository (`report.py`), written to `.pipeline/diagnosis.json` next to Paper2Agent's own `.pipeline/language.json`. The card is the data: aggregated
over a sample of papers it gives the distribution of failure causes, which does not exist in
the literature today.

## Evaluation

Sample: the 100 computational-biology papers and the 10 non-biology papers from the
Paper2Agent repository (the list is public), plus an independent sample if needed.

Three numbers to report:

1. distribution of classes and of missing items over the sample;
2. how many of the 26 failed papers yield something useful under the assigned strategy
   (a tool that reruns, recovered data, at least one extracted step), against zero today;
3. time and dollar cost compared with the single-attempt pipeline.

Honest result to state: the tools reproduce the original outputs and run on new data. They
are not shown to be correct on new data.

## Extension: a verification report, not another AI reviewer

Human reviewers read and judge. Elsevier's checklist asks whether the literature is current
and appropriate, whether the methods allow replication, and whether references are "current
and relevant". NeurIPS scores quality, clarity, significance and originality; reproducibility
sits under clarity, and code is inspected at the reviewer's discretion, in a container, as
untrusted. No reviewer runs the code, checks that a reference exists, or checks that a cited
passage supports the claim it is cited for.

Automated reviewers cover the same ground as humans, and worse: they catch 68-72% of
injected reasoning and claim errors (Benchmarking Agentic Review Systems, 2026) but write
59% fewer weaknesses than humans and do not separate good papers from weak ones (Unveiling
the Merits and Defects of LLMs in Automatic Review Generation, 2025). The 2026 benchmark
states that it does not evaluate whether systems run code or check references. That is the
gap: verification with executable evidence, as a report attached to the human review.

Three modules, each with its own evidence and its own benchmark:

| Module | Question | Evidence | Existing benchmark |
| --- | --- | --- | --- |
| References | Does every cited work exist? Does the cited passage support the claim? | resolved DOI or record; matched passage or "not supported" | CiteAudit (arXiv:2602.23452) covers existence only; claim support is open |
| Literature | Do "first to", "no prior work on" claims hold against a systematic search? | list of candidate prior works not cited | none found; hardest to evaluate |
| Code | Does the code run, reproduce, generalize? | diagnosis card and validation level L0-L5 | this project |

Order: code first (already in progress, clearest benchmark), references second (benchmark
exists, the claim-support check is the new part), literature last. Keep the modules separate:
each is a paper on its own. The combined report is the certificate that Paper2Agent's
"agent availability" section hints at, extended from code to references and literature.

## Out of scope

- Environment setup: ten systems already exist and the residual failures are structural.
- Code generation from the paper text: high risk, benchmarks already crowded.
- R and Bioconductor: natural extension, but later.

## Order of work

1. Static diagnosis and JSON card (this repository, today).
2. Aggregate the `exclusions` of Paper2Agent runs over the sample into the same card: first distribution of causes.
3. Dynamic diagnosis as a Claude Code sub-agent (`prompts/diagnose.md`).
4. `monolithic` strategy: the simplest and the most neglected.
5. `missing_data` strategy: DOI resolution and synthetic data.
6. Package the whole thing as a skill alongside `paper2mcp`, so it runs in the same host.
7. Run over the sample and report the table.
