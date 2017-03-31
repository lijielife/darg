#!/bin/bash

set -e

echo 'run JS tests with karma...'
cd darg.js

# prepare app
grunt coffee
grunt concat

# run test
./node_modules/.bin/karma start karma.ci.conf.js
cd ..
echo 'JS tests finished'
