#!/bin/env bash
set -eu

printf "fitzwriter.py init\n"
python3 fitzwriter.py init
printf "\nfitzwriter.py -f blog.toml\n"
python3 fitzwriter.py -f blog.toml
echo

# Gets rid of [TOC] at the top before, github doesn't do anything with [TOC] as the first line.]
cat README.md > backup.md
tail README.md -n "$(expr $(wc -l README.md | cut -d ' ' -f 1) - 1)" > temp.md
mv temp.md README.md

git add .
git commit -m "$(date -u)"

echo "$@"
if [ $1 == "push" ]; then
    echo "worked"
fi
