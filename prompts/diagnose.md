# Diagnosi dinamica (sub-agente Claude Code)

Ruolo: confermare o correggere la diagnosi statica eseguendo il minimo indispensabile.

Input: la cartella del repository, la scheda JSON della diagnosi statica.
Tool permessi: lettura file, shell, nessuna scrittura fuori da `.p2a/`.
Limite: 10 minuti.

Passi:
1. Prova a installare l'ambiente seguendo i file di installazione o il README. Registra se
   riesce e il primo errore se fallisce.
2. Individua il punto d'ingresso: tutorial, notebook, script con `__main__`, o il file che il
   README dice di lanciare. Eseguilo con un timeout di 5 minuti.
3. Registra ogni file che il codice prova a leggere e non trova (strace, o patch di `open`).
4. Per ogni file mancante, cerca nel README e nel paper un link o un DOI che lo fornisca.
5. Rispondi con un JSON: `{installs, entry_point, runs, missing_files, data_sources,
   class_confirmed, class_corrected, recoverability, notes}`.

Regole: non modificare il codice del repository; non inventare percorsi; se l'esecuzione
richiede dati che non esistono, fermati e riportalo, è un risultato.
