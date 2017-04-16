#!/bin/bash

source .ve/bin/activate
cd site
celery worker -c 1 -A project -l DEBUG -B
