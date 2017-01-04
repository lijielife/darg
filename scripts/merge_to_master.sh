#!/bin/bash
set -xe

if [ ! -d "scripts" ]; then
  echo 'this script must be executed from project root'
fi

echo "merge-to-master: $1"

git checkout master && git merge develop --no-edit && ./scripts/gitversioning.sh $1 && git push && git checkout develop && git push
