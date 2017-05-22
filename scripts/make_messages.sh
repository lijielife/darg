#!/bin/bash

cd "$(dirname "$0")/../site"
./manage.py makemessages --settings=project.settings.dev -e html,txt,py --all -d django
./manage.py makemessages --settings=project.settings.dev -e js --all -d djangojs
