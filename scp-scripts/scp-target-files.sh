#!/bin/bash

echo "Number of parameters: $#: " $#
echo "Parameters: $*: " $*

mkdir target-files/;

echo "Sleeping..."
date
sleep 1		#1 for 1s, 1m for 1 min, 1h for 1 hour
echo "Wakeup...DATE:"
date

for arg in $*
do
	echo "arg: $arg"
	sudo sshpass -p 'password' scp marco@yourserver:/jobs/xx/builds/$arg/archive/out/target/product/xxxx/obj/PACKAGING/target_files_intermediates/* target-files/
	date
done

#if [ -d "$1" ];then
#    rm -rf "$1"
#fi
