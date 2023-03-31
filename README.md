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
* --saintoftheday : NEW FEATURE!!, variante che invoca biastime e improperi verso i santi del giorno
  
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
