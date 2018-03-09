#!/bin/bash

BOLD="\033[4;34m"
NORMAL="\033[0m"
RESULT="\033[1;31m"
function usage() {
	echo "Sample Usage:"
	echo "$0 -k <key (1-25)> -i <input file>"
	exit -1
}

FILE=""
KEY=0

function caesar() {
	echo -e "${BOLD}Original${NORMAL}"
	while read LINE; do echo $LINE; done < $2
	echo -e "${BOLD}Key${NORMAL}"
	echo $KEY

	echo -e ">> ${RESULT}$(tr 'A-Z' 'a-z' < $2  | tr 'a-z' $( echo {a..z} | sed -r 's/ //g' | sed -r "s/(.{$1})(.*)/\2\1/" ))${NORMAL}"
}
while getopts :i:k:h opt; do
	case $opt in
		i ) 	FILE=$OPTARG;;
		k ) 	KEY=$OPTARG;;
		\? ) 	echo "Invalid option: -$OPTARG" >&2; usage;;
		h )	usage;;
	esac
done
shift $((OPTIND -1))

if [ ! -f ${FILE} ]; then echo "${FILE} does not exist"; exit -1; fi
if [[ $(wc -l <${FILE}) -ge 2 ]]; then echo "File must contain just one line of text"; exit -1; fi
case $KEY in
	''|*[!0-9]*) echo "Key has to be within range 1-26" ;;
	*) caesar $KEY ${FILE};;
esac

