#!/bin/bash
set -xe

if [ ! -d "scripts" ]; then
  echo 'this script must be executed from project root'
fi

source .ve/bin/activate

git pull --no-edit && pip install -r requirements.txt | grep -v "Requirement already satisfied" || true

echo "Creating fresh DB and media backups..."
# needs to be run from site dir
cd site
./manage.py dbbackup
./manage.py mediabackup
cd ..

python ./scripts/minify_static.py && ./site/manage.py migrate && ./site/manage.py collectstatic --noinput

echo "touching to reload uwsgi..."
touch "/tmp/$USER-master.pid"

echo "restarting supervisor..."
./scripts/restart_supervisor.sh

echo "...done"
