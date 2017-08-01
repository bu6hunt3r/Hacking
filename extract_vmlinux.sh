#!/bin/bash

function usage() {
	echo "$0 <path to zlib image>";
	exit
}

if [[ $# -eq 1 ]]; then
	#echo "Num of args: $#"
	od -A d -t x1 $1 | grep '1f 8b 08 00'
else	
	usage
	exit
fi
