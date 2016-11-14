Das Aktienregister.
==========================

Develop: [![Build Status](https://semaphoreci.com/api/v1/projects/e5b958e0-838d-4565-b8f5-4bea164a65ee/435885/badge.svg)](https://semaphoreci.com/vbnet/aktienregister)  

CapTable
===========================
This app provides an easy to user interface to have a simple CapTable (incl. options, ESOP etc.). Means enter company data, enter shareholders, have transactions for shareholders, print CapTable, edit company core data, enter capital increases. Supports a mulitple asset types for a company (named/registered share OR bearer share).

SetUp
===========================

First: current version requires PostgreSQL 9.4 (because of `jsonb` fiel implementation is required.

For general setup here is a copy of the build commands for latest `Ubuntu LTS`:
```
export DEBIAN_FRONTEND=noninteractive
export INSTAPAGE_TOKEN='REPLACEME'
export INSTAPAGE_ACCESS_TOKEN='REPLACEME'
export RAVEN_DSN=
export RAVEN_DSN_PUBLIC=
export DROPBOX_ACCESS_TOKEN=
export DROPBOX_ROOT_PATH=
export LC_ALL=en_US.UTF-8
sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 1397BC53640DB551
sudo apt-get update
sudo apt-get -q -y install python-virtualenv python-dev google-chrome-stable firefox xvfb wamerican exim4
virtualenv .ve
source .ve/bin/activate
pip install -r requirements.txt
pip install -r requirements_ci.txt
sudo -u postgres psql -c "CREATE ROLE darg WITH password 'darg' LOGIN;" 
sudo -u postgres psql -c "ALTER ROLE darg WITH CREATEDB;"
sudo -u postgres psql -c "CREATE DATABASE darg WITH OWNER darg;"
python ./minify_static.py
cd site
cp project/settings/dev_local.dist.py project/settings/dev_local.py
python manage.py collectstatic --noinput --settings=project.settings.dev
python manage.py migrate --settings=project.settings.dev
```

For a build shortcut feel free to call `./scripts/build.sh` from projects home directory.

Please also put latest chromedriver into `site` directory as executable. App should then be up and running.

See https://github.com/patroqueeet/darg/blob/develop/dev_commands.md for details about compiling etc. Make sure `bower` and `npm` installs in `darg.js` are being run befor development start.

Finally add Secret Key to Django settings. Use http://www.miniwebtool.com/django-secret-key-generator/ for generation and add to your `site/project/settings/dev_local.py`. Although we have provided a default one into `dev_local.dist.py`.

Frontend Development
====================
follow above instructions for setup. to run the app run:
```
python manage.py runserver 0.0.0.0:8000 --settings=project.settings.dev
```

access `localhost:8000` on your local machine to open the app. Run dev commands as documented inside `/dev_commands.md` to compile sass files into css. Refresh your browser to see latest code changes. Follow file structure for sass files under `site/static/sass` to place your changes. main file is `screen.sass` with all imports. see `_breakpoints.sass` for media queries and `_settings.sass` for constant definition. integrate your code with identical look and feel of the existing code.

Browser compatibility: respect our user base:

<img width="458" alt="screenshot 2016-11-07 17 12 00" src="https://cloud.githubusercontent.com/assets/2073086/20130732/1f4f942e-a659-11e6-84f8-52554f8b8144.png">

For Sass install please follow these dependencies:

<img width="369" alt="screenshot 2016-11-10 13 39 24" src="https://cloud.githubusercontent.com/assets/2073086/20177090/3ace0508-a74b-11e6-9a66-e751092c00d4.png">

**IMPORTANT for python newbies:** For any shell you are using to run a python command you must activate your virtualenv first `source .ve/bin/activate` befor running the command.

Tests
=======

Running all of them:
```
cd site
./manage.py test --settings=project.settings.dev --with-progressive --keepdb
```
`--with-progressive`, `--keepdb` are optional

Development Guidelines
=========================

Please work with pull requests (fork before). Every Pull request must contain:
* code change
  * maintain current code pattern (comments, code structure) - it should not be possible to see who coded what
  * use as much existing pattern as possible
  * must be production ready, there is no QA, we expect your code to work out of the box with all technical risk handled
  * don't add any technical debt. deliver perfect. do it now.
  * work with linting for all languages. if you improve existing code, make a separate commit for it
  * we currently target clients with the following structure: Minimum Case: 2 shareholders, one operator, 1000 shares, no options => the app must be VERY simple and easy to use for them (Challenge: simplicity); Maximum Case: 10000 shareholders, 5 operators, 10.000.000 shares, 1.000.000 options => app must provide professional configurable interface reacting very fast on any click (challenge: performance)
* tests (prefer fast unittests but make sure you cover the risk added by your code, in case of doubt add selenium based test).
* proper commit message (read http://chris.beams.io/posts/git-commit/)

Debugging:
* if a ticket reports a bug, write a failing test to reproduce the issue. then fix the issue and commit working test and fix at once.

Collab guidelines:
* ask before you code, if you don't you will fail and your pull request will be rejected

Recommended `.vimrc` for coding is:
```
" Pathogen load
filetype off

call pathogen#infect()
call pathogen#helptags()

filetype plugin indent on
syntax on

" http://stackoverflow.com/questions/1523482/vimrc-configuration-for-python
autocmd BufRead *.py set smartindent cinwords=if,elif,else,for,while,try,except,finally,def,class
set tabstop=4
set shiftwidth=4
set expandtab
set autoindent
set smartindent
syntax on
set listchars=tab:>-
set listchars+=trail:.
set ignorecase
set smartcase

" disable rope
let g:pymode_rope = 0
" ignore pep 8 errors
let g:pep8_ignore="E401"
let g:pymode_lint_config = '$HOME/pylint.rc'

" shortcuts
nmap j <Esc>:tabprev<CR>
nmap k <Esc>:tabnext<CR>
```
using plugins `python-mode`, `pathogen`, `vim-isort`.

Please note that `Isort` must handle the import formatting.

For debugging we replaced `pdb` with `pdb++` and also provide `FunctionalTestCase._screenshot()` and `FunctionalTestCase._handle_exception()` for Selenium Test debugging/failure handling.


Licence
-------------------------

This software is handled by GNU GENERAL PUBLIC LICENSE v2.0. Means most importantly all changes and additions must be shared publicly too.
