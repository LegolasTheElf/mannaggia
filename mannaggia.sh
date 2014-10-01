#!/bin/sh
############################################################
# Mannaggiatore automatico per VUA depressi
# idea originale by Alexiobash dallo script incazzatore.sh
# ampliata, riscritta e mantenuta da Pietro "Legolas" Suffritti
# convertita in mannaggia.sh rel 0.2
# patcher e contributors:
# Marco Placidi, Maurizio "Tannoiser" Lemmo, Matteo Panella
# Mattia Munari
# thanks to : Veteran Unix Admins group on Facebook
# released under GNU-GPLv3
############################################################
# parametri da command line:
# --audio : attiva mplayer per fargli pronunciare i santi
# --spm <n> : numero di santi per minuto
# --wall : invia l'output a tutte le console : attenzione , se non siete root o sudoers disattivare il flag -n
# --nds <n> : numero di santi da invocare (di default continua all'infinito)

audioflag=false
spm=1
spmflag=false
nds=-1
pot=-1
ndsflag=false
wallflag=false
DELSTRING1="</FONT>"
DELSTRING2="</b>"

USAGE="USAGE: $0 [--audio] [--wall] [--spm <n>] [--nds <n>]"

# lettura parametri da riga comando

while [ $# -gt 0 ]
do
    case $1 in
    # leggi dai parametri se c'e' l'audio
    --audio) audioflag=true ;;
    # leggi dai parametri se c'e' da mandare i commenti su wall
    --wall) wallflag=true ;;
    # imposta i santi per minuto
    --spm) spm=$((60 / $"2")) ; shift;;
    # imposta il numero di santi da ciclare
    --nds) nds="$2" ; shift;;
    (-*) echo "$0: error - unrecognized option $1" 1>&2; exit 1;;
    (*) echo "Unknown option"; echo $USAGE; exit 2;;
    esac
    shift
done

while [ "$nds" != 0 ]
do
    # shellcheck disable=SC2019
    MANNAGGIA="Mannaggia $(curl -s "www.santiebeati.it/$(</dev/urandom tr -dc A-Z|head -c1)/"|grep tit|cut -d'>' -f 4-9|shuf -n1 |awk -F "$DELSTRING1" '{print$1$2}'|awk -F "$DELSTRING2" '{print$1}')"
    MANNAGGIAURL="http://translate.google.com/translate_tts?tl=it&q=$MANNAGGIA"
    
    if [ "$wallflag" = true ]
    then
        pot=$(( nds % 50 ))
        if [ "$pot" = 0 ]
        then
            echo "systemd merda, poettering vanaglorioso fonte di danni, ti strafulmini santa cunegonda bipalluta protrettice dei VUA"
        else
            # attenzione: se non siete root o sudoers dovete togliere dalla riga successiva "sudo" e "-n"
            echo "$MANNAGGIA" | sudo wall -n
        fi
    else
        echo "$MANNAGGIA" > /dev/stdout
    fi

    if [ "$audioflag" = true ]
    then
        mplayer -really-quiet -ao alsa "$MANNAGGIAURL" 2>/dev/null
    fi

    sleep "$spm"
    nds=$((nds - 1))
done
