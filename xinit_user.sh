#!/usr/bin/env bash

if [ $# -eq 0 ]
  then
    echo "No arguments supplied"
    exit 1
fi

if grep "$1" /etc/passwd >/dev/null 2>&1; then
  su - $1 -c "startx -- :0 vt7"
  exit 0
else
  echo "User not found"
  exit 2
fi
