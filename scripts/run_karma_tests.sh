#!/bin/bash

echo 'run JS tests with karma...'
cd darg.js
karma start karma.ci.conf.js
cd ..
echo 'JS tests finished'
