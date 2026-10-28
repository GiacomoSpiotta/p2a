# p2a: diagnosi prima dell'agentificazione

Concept per un contributo sopra Paper2Agent (Miao et al., Nature 2026): invece di chiedere a
ogni repository scientifico di comportarsi come una libreria con tutorial, lo si diagnostica
prima e si sceglie una strategia per la forma che ha davvero.

La strategia completa è in `docs/strategia.md`.

## Cosa c'è

- `src/p2a/diagnose.py`: diagnosi statica, legge i file e produce i segnali. Nessuna esecuzione.
- `src/p2a/classify.py`: regole che assegnano una classe (`library`, `stepwise`, `monolithic`,
  `missing_data`, `text_only`) e le mancanze.
- `src/p2a/strategies/`: un piano per classe. Sono stub: dicono cosa produrre e come validarlo.
- `src/p2a/report.py`: la scheda JSON, che è il dato del progetto.
- `prompts/diagnose.md`: prompt del sub-agente per la diagnosi dinamica (Claude Code).
- `eval/`: campione e numeri da riportare.

## Uso

```
uv venv && source .venv/bin/activate
uv pip install -e .
p2a diagnose /percorso/di/un/repo
p2a diagnose /percorso/di/un/repo --json
pytest
```

## Prossimi passi

1. Far girare la diagnosi statica sui 110 repository del campione di Paper2Agent.
2. Implementare la diagnosi dinamica come sub-agente.
3. Implementare la strategia `monolithic`, che è la più semplice.
