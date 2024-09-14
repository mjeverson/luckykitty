#!/bin/bash

cd /home/pi/Documents/Projects/pithon/luckykitty/_python

if [ -z "$1" ]; then
  python3 lucky-kitty.py -p -f
else
  python3 lucky-kitty.py -p -f -w "$1"
fi

