#!/bin/sh
#######################################################################
# Mannaggiatore automatico per VUA depressi
# idea originale by Alexiobash dallo script incazzatore.sh
# ampliata, riscritta e mantenuta da Pietro "Legolas" Suffritti
# convertita in mannaggia.sh rel 0.2
# patcher e contributors:
# Marco Placidi, Maurizio "Tannoiser" Lemmo, Matteo Panella
# Mattia Munari
# thanks to : Veteran Unix Admins group on Facebook
#######################################################################

#######################################################################
# Automatic saint invocation for depressed VUA
# Copyright (C) 2014 Alexiobash
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#######################################################################

v="rel0.2"
audioflag=false
spm=1
spmflag=false
nds=-1
pot=-1
ndsflag=false
wallflag=false
oneshotflag=false
DELSTRING1="</FONT>"
DELSTRING2="</b>"

# Defining help page
mannaggia_help() {
	echo "mannaggia - Automatic saint invocation for depressed VUA (v. $v)
Usage: $0 [--audio] [--wall] [--spm <n>] [--nds <n>] [--oneshot] [--help]

Options:
	--audio   	active mplayer to evoke saints;
	--wall    	sent output in broadcast (using wall);
	         	WARNING: if you can't use root permissions, deflag -n;
	--spm <n> 	number of saints-per-minute;
	--nds <n>	number-de-saints to evoke (loop as default);
	--oneshot 	evoke only one saint (overriding --nds);
	--help    	show this help page.

Bugs or enchantement:
	https://github.com/LegolasTheElf/mannaggia/issues

License:
	GNU General Public License Version 3"
}

# Reading args from command line
while [ $# -gt 0 ]; do
	case $1 in
		# Read audio arg
		--audio)
			audioflag=true
			;;
		# Read wall arg
		--wall)
			wallflag=true
			;;
		# Set saints-per-minute
		--spm)
			spm=$((60 / $"2"))
			shift
			;;
		--oneshot)
			oneshotflag=true
			nds=1
			;;
		# Set number-de-saints (overrided by --oneshot)
		--nds)
			$oneshotflag || nds="$2"
			shift
			;;
		--help)
			mannaggia_help
			exit 0
			;;
		(-*)
			echo "$0 [ERROR]: Unrecognized option $1" 1>&2;
			exit 1
			;;
		(*)
			echo "$0 [ERROR]: Unknown option"
			mannaggia_help
			exit 2
			;;
	esac
	shift
done

while [ "$nds" != 0 ]; do
	# shellcheck disable=SC2019
	MANNAGGIA="Mannaggia $(curl -s "www.santiebeati.it/$(</dev/urandom tr -dc A-Z|head -c1)/"|grep tit|cut -d'>' -f 4-9|shuf -n1 |awk -F "$DELSTRING1" '{print$1$2}'|awk -F "$DELSTRING2" '{print$1}')"
	MANNAGGIAURL="http://translate.google.com/translate_tts?tl=it&q=$MANNAGGIA"

	if [ "$wallflag" = true ]; then
		pot=$(( nds % 50 ))
		if [ "$pot" = 0 ]; then
			echo "systemd merda, poettering vanaglorioso fonte di danni, ti strafulmini santa cunegonda bipalluta protrettice dei VUA"
		else
			# Warning: if you cant use root permissions you mast
			# remove the -n flag from the next line
			echo "$MANNAGGIA" | sudo wall -n
		fi
	else
		echo "$MANNAGGIA" > /dev/stdout
	fi

	$audioflag && mplayer -really-quiet -ao alsa "$MANNAGGIAURL" 2>/dev/null

	sleep "$spm"
	nds=$((nds - 1))
done
