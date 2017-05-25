#!/bin/bash
set -xe

if [ ! -d "scripts" ]; then
  echo 'this script must be executed from project root'
fi

source .ve/bin/activate

git pull --no-edit && pip install -r requirements.txt | grep -v "Requirement already satisfied" || true

echo "Creating fresh DB and media backups..."

skip_backup=false
while getopts ":s" opt; do
  case $opt in
    s)
      skip_backup=true
      ;;
    \?)
      echo "Invalid option: -$OPTARG" >&2
      ;;
  esac
done

# needs to be run from site dir
if [ "$skip_backup" = true ] ; then
  echo "BACKUP SKIPPED"
else
  cd site
  ./manage.py dbbackup
  ./manage.py mediabackup
  cd ..
fi

python ./scripts/minify_static.py && ./site/manage.py migrate && ./site/manage.py collectstatic --noinput

echo "touching to reload uwsgi..."
touch "/tmp/$USER-master.pid"

echo "restarting supervisor..."
./scripts/restart_supervisor.sh

echo "...done"
