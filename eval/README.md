# Evaluation sample

`sample.csv`: one paper per row, with `paper_id, repo_url, paper2agent_outcome` where the
outcome is `converted` or `failed` according to the Paper2Agent repository
(https://github.com/jmiao24/Paper2Agent, 100 computational-biology papers and 10 non-biology ones).

Run: for each row, clone the repo, `p2a diagnose`, save the card to `results/<paper_id>.json`.

Numbers to report:
1. distribution of classes and missing items;
2. among the 26 failed papers, how many yield a useful artifact under the assigned strategy;
3. time and cost per repository.
