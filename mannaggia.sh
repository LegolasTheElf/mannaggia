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

# @TODO Translating number-de-saint into something more better

v=0.2
audioflag=false
spm=1
spmflag=false
nds=-1
pot=-1
ndsflag=false
wallflag=false
oneshot=false
DELSTRING1="</FONT>"
DELSTRING2="</b>"

# Defining help page
mannaggia_help() {
	echo "mannaggia - Automatic saint invocation for depressed VUA (v. $v)
Usage: mannaggia.sh [OPTIONS] ..

Options:
	--audio   	active mplayer to evoke saints;
	--spm <n> 	number of saint-per-minute;
	--wall    	sent output in broadcast (using wall);
	         	WARNING: if you can't use root permissions, deflag -n;
	--nds <n>	number-de-saint to evoke (loop as default);
	--oneshot 	evoke only one saint (overriding --nds).

Bugs or enchantement:
	https://github.com/LegolasTheElf/mannaggia/issues

License:
	GNU General Public License Version 3"
}

# Reading args from command line
for parm in "$@"; do

	# Read help arg
	if [ "$parm" = "--help" ]; then
		mannaggia_help
		exit
	fi

	# Read audio arg
	[ "$parm" = "--audio" ] && audioflag=true

	# Read wall arg
	[ "$parm" = "--wall" ] && wallflag=true

	# If spmflag, set saints/minute and reset the flag
	if [ "$spmflag" = true ]; then

		# Jump if oneshot arg
		if [ "$oneshot" = true ]; then
			spmflag=false
			continue
		fi

		if [ $parm -lt 1 ]; then
			spm=1
			spmflag=false
		else
			spm=$((60 / parm))
			spmflag=false
		fi
	fi

	# Read oneshot arg
	if [ "$parm" = "--oneshot" ]; then
		nds=1
		oneshot=true
	fi

	# Read saints-per-minute arg and set the spmflag flag
	[ "$parm" = "--spm" ] && spmflag=true

	# If ndsflag, set max number of saints to evoke
	if [ "$ndsflag" = true ]; then
		nds="$parm"
		ndsflag=false
	fi

	# Read number-de-saints arg and set the ndsflag flag
	[ "$parm" = "--nds" ] && ndsflag=true
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

	[ "$audioflag" = true ] && mplayer -really-quiet -ao alsa "$MANNAGGIAURL" 2>/dev/null

	sleep "$spm"
	nds=$((nds - 1))
done
