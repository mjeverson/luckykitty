#!/bin/bash

cd /home/pi/Documents/Projects/pithon/luckykitty/_python

if [ -z "$1" ]; then
  echo "No argument passed"
  python3 lucky-kitty.py -p -f
else
  echo "Argument passed: $1"
  python3 lucky-kitty.py -p -f --win="$1"
fi

