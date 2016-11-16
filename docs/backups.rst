Backups
=======

We are using the `Django Database Backup <https://django-dbbackup.readthedocs.io/en/stable/>`_ for backups. Please read their docs for more details.

Configuration
-------------

In order to be able to store backups at Dropbox, you need to provide your `access token <https://blogs.dropbox.com/developers/2014/05/generate-an-access-token-for-your-own-account/>`_.

.. code-block :: shell
    export DROPBOX_ACCESS_TOKEN=<YOUR TOKEN>
    source .ve/bin/activate
    python ./site/manage.py dbbackup
    python ./site/manage.py mediabackup


Nightly backups
--------

project/tasks.py contains the backup task definition.
