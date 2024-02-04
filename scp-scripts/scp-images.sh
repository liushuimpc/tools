#!/bin/bash

echo "Number of parameters: $#: " $#
echo "Parameters: $*: " $*

mkdir images;
mkdir ota-packages/;

echo "Sleeping..."
date
sleep 1		#1 for 1s, 1m for 1 min, 1h for 1 hour
echo "Wakeup...DATE:"
date

for arg in $*
do
	echo "arg: $arg"
	mkdir -p images/$arg
	sudo sshpass -p 'password' scp marco@yourserver:/jobs/xx/builds/$arg/archive/* images/$arg/
	sudo sshpass -p 'password' scp marco@yourserver:/jobs/xx/builds/$arg/archive/out/target/product/xxxx/* ota-packages/
	date
done

#if [ -d "$1" ];then
#    rm -rf "$1"
#fi
