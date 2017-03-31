#!/bin/bash

set -e

echo 'run JS tests with karma...'
cd darg.js
./node_modules/.bin/karma start karma.ci.conf.js
cd ..
echo 'JS tests finished'
