#!/bin/sh

if [ -z "$1" ]; then
  echo "Usage: $0 <user>@<host>"
  exit 1
fi

rsync -avz \
  --delete \
  --exclude {'.git', '.ruff_cache', '__pycache__', '.python-version', '.DS_Store', '*.session', '*_test.py'} \
  . \
  $1:/root/app