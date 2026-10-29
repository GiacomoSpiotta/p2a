# Test plan: p2a against the Paper2Agent skill

## Goal

Measure two things that the Paper2Agent paper does not report:

1. why the papers it fails to convert fail, with counts per cause;
2. how many of those papers yield a usable artifact once a strategy matched to the
   repository shape is applied, and at which level of validation.

We do not try to beat Paper2Agent on the papers it already converts.

## What is compared

| | Baseline | Ours |
| --- | --- | --- |
| System | Paper2Agent skill, `skills/paper2agent/paper2mcp`, pinned commit | p2a diagnosis + strategy per class, on top of the same skill |
| Host | Claude Code, same version for both | same |
| Model | one model, fixed for the whole study, recorded by exact ID | same |
| Input | repository URL and paper PDF | same |
| Output | MCP server ZIP, `reports/agent-runs.json` with exclusions | diagnosis card, MCP server or reproduce tool, validation level |

Pin the skill commit, the host version and the model ID in `eval/config.json` before the
first run. If any of them changes, the baseline is rerun.

## Sample

- S1: the 100 computational-biology papers from the Paper2Agent sweep.
- S2: the 10 non-biology papers (grf, SAELens, Binoculars, SAM2, TabPFN, GenericML,
  CausalImpact, Nashpy, emcee, conformal-selection).
- Source of the list: supplementary tables shipped in the skill
  (`paper2agent-paper/assets/supp_table/`). If the list is not there, ask the authors; as a
  last resort, rebuild the sampling (bioRxiv, bioinformatics category, backwards from
  December 2025, no quality filter) and state that the sample differs.

Each paper gets a row in `eval/sample.csv`: `paper_id, repo_url, commit, paper_pdf,
paper2agent_outcome_reported`.

Repositories are pinned to the commit at the time of the study; a repository that has
changed since the paper is flagged, not excluded.

## Phases

### Phase 0: setup (no LLM cost)

- Clone every repository at the pinned commit.
- Run `p2a diagnose` on all 110. Save `.pipeline/diagnosis.json` per repository.
- Output: distribution of provisional classes and missing items. This is the first table and
  costs nothing.

### Phase 1: baseline on the failed set

- Run the Paper2Agent skill on the 26 papers reported as failed, plus 10 reported as
  converted, chosen at random as a control.
- Record per paper: outcome (converted, partial, failed), number of tools proposed and
  validated, exclusion reasons from `agent-runs.json`, wall time, dollar cost.
- Check that the 10 controls still convert. If several do not, the repository or the model
  has drifted, and the comparison is reported against this new baseline, not the paper's.

### Phase 2: diagnosis against exclusions

- For the 26 failed papers, compare the p2a class and missing items with the skill's own
  exclusion reasons.
- Output: agreement table (class vs reason), and the cases where the static diagnosis is
  wrong. Fix the rules, rerun Phase 0. Repeat once at most.

### Phase 3: strategies on the failed set

- Apply the assigned strategy to each of the 26: `monolithic` reproduce tool,
  `missing_data` recovery, `stepwise` on the undocumented part, `text_only` for the rest.
- Record the validation level reached (see below), time and cost.

### Phase 4: full sweep (optional, budget permitting)

- Baseline and ours on all 110. Only if Phases 1 to 3 show a difference worth the cost.

### Phase R (optional): reference check on the sample, no code execution

- For each of the 110 papers, extract the reference list and the in-text citation contexts.
- Existence: resolve each reference by DOI, then by title search (Crossref, OpenAlex,
  Semantic Scholar). Record found / not found / ambiguous.
- Claim support: for a random sample of 5 citations per paper, retrieve the cited work's
  abstract or full text when open, and have a fresh agent judge whether the cited passage
  supports the sentence it is attached to; a second agent re-judges blind; disagreements go
  to a human.
- Output: per paper, the number of unresolved references and of unsupported citations; over
  the sample, the two rates with denominators. Compare the existence rate with CiteAudit's
  reported numbers to check the method.
- Cost: no code execution; one short LLM call per sampled citation. Runs within the
  subscription limits in a few hours.

## Validation levels

Every artifact is scored on one scale, for both systems:

| Level | Meaning |
| --- | --- |
| L0 | nothing usable produced |
| L1 | resource layer only (text and supplements queryable) |
| L2 | code runs on synthetic data with the inferred schema; no scientific check |
| L3 | code runs on recovered or original data; output shape consistent with the paper |
| L4 | outputs match the original ones within tolerance (numbers within 3%, figures by perceptual hash), as in Paper2Agent |
| L5 | L4, and the tool runs on at least one new dataset with a different shape without agent-written code |

Paper2Agent's "converted" is L4. The honest claim for ours is the count per level.

## Metrics

Primary:

- `cause_distribution`: count of the 26 per cause (static class confirmed by the dynamic
  diagnosis and by the skill's exclusions).
- `recovered_by_level`: among the 26, number reaching L1, L2, L3, L4, L5 with ours, against
  the baseline (expected: all L0 or L1).

Secondary:

- cost and wall time per paper, both systems;
- for the 10 controls: baseline still converts (yes/no), and ours does not degrade them
  (same tools, same tests pass);
- diagnosis accuracy: static class vs dynamic class vs skill exclusion reason.

## Runs and repeats

- One run per paper for the sweep; three runs on a 10-paper subset (5 failed, 5 controls) to
  measure variance. Report mean and spread on that subset.
- A run that times out (set the same limit for both systems, 2 hours) is a failure, not a retry.

## Cost control

- Paper says about 14 dollars and 45 minutes per paper. Budget for Phases 1 to 3:
  36 papers x 2 systems, about 50 machine hours. On a Claude subscription the cost is the
  usage limit, not dollars: spread runs over days. Record tokens per run and report the
  dollar equivalent at API list price, so the number is comparable with the paper's.
- Set a hard spend cap per run through the host and stop at the cap.
- Phase 0 and the diagnosis agreement tables need no LLM budget.

## What counts as a result

- A table of the 26 by cause. Even if nothing is recovered, this is new.
- Any paper moved from L0/L1 to L3 or above is a recovered paper; report the list, not only
  the count.
- Any control that degrades under ours is reported as a regression.

## Risks

- The paper list is not public: the sample has to be rebuilt and is not the same.
- The skill has changed since the paper: the baseline numbers differ from 74/100 and the
  comparison is against the rerun, which must be said.
- Model drift between runs: fix the model ID; if the provider retires it, rerun the baseline.
- Data recovery touches external services (Zenodo, GEO, Hugging Face): record the download
  date and the file hashes.
- Security: both systems execute repository code. Run everything in a disposable container
  with no credentials beyond the model key.

## Deliverables

- `eval/config.json`: pinned commit, host version, model ID, time limit, spend cap.
- `eval/sample.csv`: the 110 rows.
- `eval/results/<paper_id>/`: diagnosis card, baseline report, our report, validation level.
- `eval/summary.md`: the tables above, with denominators.
