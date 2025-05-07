# Mannaggiatore Automatico - Python Edition

Conversione dello script bash `mannaggia.sh` in un'applicazione Python con interfaccia grafica.

## Requisiti

- Python 3.6+
- Tkinter (incluso nella maggior parte delle distribuzioni Python)
- Beautiful Soup 4
- Requests
- mplayer (per la funzionalità audio)

## Installazione

1. Assicurati di avere Python 3 installato:
   ```
   python3 --version
   ```

2. Installa le dipendenze Python:
   ```
   pip install -r requirements.txt
   ```

3. Per la funzionalità audio, installa mplayer:
   ```
   sudo apt-get install mplayer
   ```

## Utilizzo

Esegui il programma con:
```
python3 mannaggia.py
```

Per eseguire con permessi di amministratore (necessari per le funzioni wall e shutdown):
```
sudo python3 mannaggia.py
```

## Funzionalità

- **Audio (TTS)**: Attiva la riproduzione audio delle frasi tramite Google TTS
- **Wall**: Invia l'output a tutti i terminali (richiede permessi di root)
- **Santi per minuto**: Imposta quanti santi invocare al minuto
- **Numero di santi**: Imposta quanti santi invocare in totale (-1 per infinito)
- **Spegni al termine**: Spegne il sistema quando il conteggio raggiunge lo zero (richiede permessi di root)
- **OFF**: Shortcut per invocare un santo e spegnere (richiede permessi di root)

## Licenza

Rilasciato sotto GNU-GPLv3, come lo script originale.

## Crediti

Questa è una conversione del codice originale `mannaggia.sh`.

Progetto originale:
- Idea originale by Alexiobash dallo script incazzatore.sh
- Ampliata, riscritta e mantenuta da Pietro "Legolas" Suffritti
- Convertita in mannaggia.sh rel 0.2
- Collaborators: Enrico "Henryx" Bianchi, Alessandro "Aleskandro" Di Stefano, Davide "kk0nrad" Corrado
- Patcher e contributors: Marco Placidi, Maurizio "Tannoiser" Lemmo, Matteo Panella, Mattia Munari
- Thanks to: Veteran Unix Admins group on Facebook
