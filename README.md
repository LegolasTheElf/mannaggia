mannaggia.sh
=========

Automatic saint invocation for depressed Veteran Unix Admins,

it's developed in italian, it can be easily adapted in other languages.

requires mplayer to use the --audio parameters



Questo script provvede a nominare tutti i santi per voi quando vi sentite depressi.

Prerequisiti:
* mplayer per potere usare il parametro --audio

parametri da command line:
* --audio : attiva mplayer per fargli pronunciare i santi
* --spm <n> : numero di santi per minuto
* --wall : invia l'output a tutte le console : attenzione , se non siete root o sudoers disattivare il flag -n
* --shutdown : se si e' root spegne il computer dopo aver finito di invocare sant (dipende da --nds)
* --off : equivalente a --nds 1 --shutdown

Rilasciato sotto Licenza GNU-GPL v.3

idea originale by Alexiobash dallo script incazzatore.sh

ampliata, riscritta e mantenuta da Pietro "Legolas" Suffritti

convertita in mannaggia.sh rel 0.2

Collaborators:
* Enrico "Henryx" Bianchi
* Alessandro "Aleskandro" Di Stefano
* Davide "kk0nrad" Corrado

patcher e contributors:
* Marco Placidi
* Maurizio "Tannoiser" Lemmo
* Matteo Panella
* Mattia Munari
* Paolo Fabbri

thanks to : Veteran Unix Admins group on Facebook

mannaggia_py.py
=========
# Mannaggiatore Automatico - Python Edition

Conversione dello script bash `mannaggia.sh` in un'applicazione Python con interfaccia grafica, effettuat tramite Claude.ai .

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


