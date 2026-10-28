# Strategia: diagnosi prima dell'estrazione

## Problema

Paper2Agent (Miao et al., Nature 2026) converte un repository scientifico in un server MCP
con una sola strategia: estrai funzioni riutilizzabili dai tutorial eseguibili, testale sugli
esempi, scarta quello che non passa. Su 100 paper di biologia computazionale ne converte 74.
I 26 restanti vengono scartati senza una diagnosi: non si sa perché falliscono né quanto manca.

Le cause dichiarate sono quattro: codice eseguibile assente, dati o modelli non disponibili,
ambiente non ricostruibile, script non generalizzabili. La pipeline tratta tutte allo stesso
modo, cioè chiede a ogni repository di comportarsi come una libreria con tutorial.

## Idea

Mettere un passo di diagnosi prima dell'estrazione e scegliere la strategia in base al
risultato. Il repository non deve essere una libreria: deve essere quello che è.

Non si tocca l'estrazione di Paper2Agent per le librerie (funziona). Si aggiunge quello che
manca per le altre forme.

## Classi

| Classe | Riconoscimento | Cosa si produce | Validazione |
| --- | --- | --- | --- |
| `library` | pacchetto installabile, API, tutorial o notebook con output | tool riutilizzabili (Paper2Agent) | test sugli esempi del tutorial |
| `stepwise` | script o notebook con passi separabili (funzioni, celle con output intermedi) | tool per i passi che generalizzano, più un tool che riesegue il resto | test per passo dove c'è un output intermedio; confronto finale con le figure |
| `monolithic` | sequenza unica, valori cablati, nessun passo ha senso da solo | un solo tool `reproduce(data)` con i valori cablati esposti come parametri | confronto degli output con quelli originali |
| `missing_data` | il codice c'è ma punta a dati o modelli non presenti né scaricabili | recupero da DOI, Zenodo, Figshare, GEO, Hugging Face; in fallback dati sintetici con lo stesso schema | esecuzione senza errori, controllo sulla forma dell'output |
| `text_only` | nessun codice | strato di risorse (testo e supplementari interrogabili) | domande di sintesi |

Le classi non sono esclusive: un repository può essere `stepwise` e `missing_data` insieme.
La diagnosi restituisce una classe principale più le mancanze.

## Diagnosi

Due livelli, in ordine di costo.

1. **Statica** (secondi, nessun LLM): segnali letti dai file. Presenza di pyproject, setup,
   requirements, environment.yml, DESCRIPTION, Dockerfile; notebook e tutorial; test; percorsi
   assoluti cablati; URL e DOI di dati nel README; uso di argparse o file di configurazione;
   linguaggi. Produce un profilo e una classe provvisoria.
2. **Dinamica** (minuti, con agente): tentativo di installazione, esecuzione del tutorial o
   dello script principale, lista dei file che il codice prova a leggere e non trova. Conferma
   o corregge la classe e stima la recuperabilità.

L'output è una scheda JSON per repository (`report.py`). La scheda è il dato: aggregata su
un campione di paper dà la distribuzione delle cause, che oggi non esiste in letteratura.

## Valutazione

Campione: i 100 paper di biologia computazionale e i 10 non biologici del repository di
Paper2Agent (lista già pubblica), più un campione indipendente se serve.

Tre numeri da riportare:

1. distribuzione delle classi e delle mancanze sul campione;
2. quanti dei 26 falliti producono qualcosa di utile con la strategia assegnata (un tool
   che riesegue, dati recuperati, almeno un passo estratto), contro zero di oggi;
3. costo in tempo e dollari rispetto al tentativo unico.

Risultato onesto da dichiarare: i tool riproducono gli output originali e girano su dati
nuovi. Non si dimostra che siano corretti sui dati nuovi.

## Cosa resta fuori

- Setup dell'ambiente: dieci sistemi esistono già, i fallimenti residui sono strutturali.
- Generazione di codice dal testo del paper: rischio alto, benchmark già affollati.
- R e Bioconductor: estensione naturale, ma dopo.

## Ordine di lavoro

1. Diagnosi statica e scheda JSON (questo repository, oggi).
2. Diagnosi dinamica come sub-agente Claude Code (`prompts/diagnose.md`).
3. Strategia `monolithic`: la più semplice, la più trascurata.
4. Strategia `missing_data`: risoluzione DOI e dati sintetici.
5. Corsa sul campione e tabella dei risultati.
