# Campione di valutazione

`sample.csv`: un paper per riga, con `paper_id, repo_url, paper2agent_outcome` dove
l'esito è `converted` o `failed` secondo il repository di Paper2Agent
(https://github.com/jmiao24/Paper2Agent, 100 paper di biologia computazionale e 10 non biologici).

Corsa: per ogni riga, clona il repo, `p2a diagnose`, salva la scheda in `results/<paper_id>.json`.

Numeri da riportare:
1. distribuzione delle classi e delle mancanze;
2. tra i 26 falliti, quanti producono un artefatto utile con la strategia assegnata;
3. tempo e costo per repository.
