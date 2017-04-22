#!/bin/bash
echo 'installing JS dependencies..'
cd darg.js
npm install
bower install
cd -
./scripts/install_karma.sh
echo 'finished installing JS deps inside darg.js'
