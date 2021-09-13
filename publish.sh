#!/bin/env bash
set -eu

printf "fitzwriter.py init\n"
python3 fitzwriter.py init
printf "\nfitzwriter.py -f blog.toml\n"
python3 fitzwriter.py -f blog.toml
echo

git add .
if [ $# -eq 0 ]; then
    exit 0
fi


if [ "$1" == "push" ]; then
    git commit -m "$(date -u)"
    git push -u origin master
    echo "worked"
fi
