#!/bin/bash

function usage() {
	echo "$0 <path to zlib image>";
	exit
}

if [[ $# -eq 1 ]]; then
	#echo "Num of args: $#"
	[[ -e $1 ]] && od -A d -t x1 $1 | grep '1f 8b 08 00' && echo -e "Next step would be 'dd if=vmlinuz bs=1 skip=24584 | zcat > vmlinux'\n";
else	
	usage
	exit
fi
