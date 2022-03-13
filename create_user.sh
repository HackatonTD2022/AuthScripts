#!/usr/bin/env bash

if [ $# -eq 0 ]
  then
    echo "No arguments supplied"
    exit 1
fi

echo "Creating user $1"
useradd -m -G authless $1 
echo -e "$2\n$2" | passwd $1

echo "User $1 created successfuly"

exit 0
