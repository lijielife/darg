#! /bin/bash
set -xe

if [ ! -d "scripts" ]; then
  echo 'this script must be executed from project root'
fi

export DEBIAN_FRONTEND=noninteractive; export DBUS_SESSION_BUS_ADDRESS=/dev/null
export INSTAPAGE_TOKEN=''
export INSTAPAGE_ACCESS_TOKEN=''
export LC_ALL=en_US.UTF-8

echo 'WARNING setting empty raven dsn, you wont have sentry tracking...'
export RAVEN_DSN=''
export RAVEN_DSN_PUBLIC=''

sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 1397BC53640DB551
sudo apt-get update
sudo apt-get -q -y install python-virtualenv python-dev google-chrome-stable firefox xvfb wamerican exim4

sudo -u postgres psql -c "CREATE ROLE darg WITH password 'darg' LOGIN;" 
sudo -u postgres psql -c "ALTER ROLE darg WITH CREATEDB;"
sudo -u postgres psql -c "CREATE DATABASE darg WITH OWNER darg;"

sudo debconf-set-selections conf/exim4_internet_site_debconf.conf
sudo dpkg-reconfigure exim4-config -fnoninteractive
sudo -- sh -c "echo 'helo_allow_chars=_' > /etc/exim4/exim4.conf.localmacros" && sudo -- sh -c "sed -i 's/local/internet/g' /etc/exim4/update-exim4.conf.conf" && sudo update-exim4.conf
sudo cat /etc/exim4/update-exim4.conf.conf && sudo exim -bP
# sudo hostname -f
sudo /etc/init.d/exim4 restart
sudo exim -bP
# pwd; sudo cat /var/log/exim4/mainlog

LATEST=$(wget -q -O - http://chromedriver.storage.googleapis.com/LATEST_RELEASE)
wget http://chromedriver.storage.googleapis.com/$LATEST/chromedriver_linux64.zip && unzip chromedriver_linux64.zip -d site/
rm chromedriver_linux64.zip

virtualenv .ve
source .ve/bin/activate
pip install -r requirements.txt
pip install -r requirements_ci.txt
python ./scripts/minify_static.py
cd site
cp project/settings/dev_local.dist.py project/settings/dev_local.py
python manage.py collectstatic --noinput --settings=project.settings.dev
python manage.py migrate --settings=project.settings.dev
