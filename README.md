obento
======

A simple python/django search multiplexing backend for use in a bento-style
frontend.  


requirements
============

Developed using Python 2.7, Django 1.5, and PostgreSQL 9.1 on Ubuntu 12.04.


Installation Instructions
=========================

PART I - Basic server requirements
----------------------------------

1. Install Apache and other dependencies

        $ sudo apt-get install apache2 libapache2-mod-wsgi libaio-dev python-dev python-profiler postgresql postgresql-contrib libpq-dev git libxml2-dev libxslt-dev solr-jetty openjdk-6-jdk

2. Set up Postgresql

    Create a user for django (and make a note of the password you create).  A name for MYDBUSER might be something like ```obentouser_m1``` (m1 for milestone 1)

        $ sudo -u postgres createuser --createdb --no-superuser --no-createrole --pwprompt MYDBUSER

    Create a database for the obento application.  A name for MYDBNAME might be something like ```obi_m1```

        $ sudo -u postgres createdb -O MYDBUSER MYDBNAME


PART II - Set up project environment
------------------------------------

1. Install virtualenv

        $ sudo apt-get install python-setuptools
        $ sudo easy_install virtualenv

2. Create a directory for your projects (replace &lt;OBENTO_HOME&gt; with 
your desired directory path and name: for instance ```/obento``` or 
```/home/&lt;username&gt;/obento```)

        $ mkdir <OBENTO_HOME>
        $ cd <OBENTO_HOME>

3. Pull down the project from github

        (GW staff only)
        $ git clone git@github.com:gwu-libraries/obento.git

        (everyone else)
        $ git clone https://github.com/gwu-libraries/obento.git

4. Create virtual Python environment for the project

        $ cd <OBENTO_HOME>/obento
        $ virtualenv --no-site-packages ENV

5. Activate your virtual environment

        $ source ENV/bin/activate

6. Install django, tastypie, and other python dependencies

        (ENV)$ pip install -r requirements.txt
        
   If the previous step encounters problems installing pytz, then it can be installed as follows

        easy_install --upgrade pytz

7. Set up Solr via jetty

    Edit ```/etc/default/jetty``` to set ```NO_START=0```, set
    ```JAVA_HOME=/usr/lib/jvm/java-6-openjdk-amd64```, and consider
    changing ```JETTY_PORT``` to a port that won't be publicly exposed.
    In development and testing, exposing Solr might be helpful; never 
    expose it in production.

    Copy the solr ```schema.xml``` for obento into system-wide solr config
    (making a backup of the original if you like):

        $ sudo cp /etc/solr/conf/schema.xml /etc/solr/conf/schema.xml.orig
        $ sudo cp obi/obi/schema.xml /etc/solr/conf/schema.xml

    Start jetty:

        sudo service jetty start
    

PART III - Configure your installation
--------------------------------------

1. Copy the local settings template to an active file

        $ cd obento/obi/obi
        $ cp local_settings.py.template local_settings.py

2. Update the values in the ```local_settings.py``` file:  for the database, ```NAME```, ```USER```, and ```PASSWORD``` to the database you created above, and set ```ENGINE``` to 'postgresql_psycopg2'; also, set a ```SECRET_KEY```.  Ensure that the port number in ```SOLR_URL``` matches ```JETTY_PORT``` configured earlier in ```/etc/default/jetty```.

        $ vim local_settings.py

3. Copy the WSGI file template to an active file

        $ cp wsgi.py.template wsgi.py

4. Update the wsgi.py file. (Change the value of ENV to your environment path)

        $ vim wsgi.py
        
5. Initialize database tables. WARNING: Be sure you are still using your virtualenv. DO NOT create a superuser when prompted!

        (ENV)$ cd <OBENTO_HOME>/obento/obi
        (ENV)$ python manage.py syncdb

    If you encounter an authentication error with postgresql edit your local_settings.py file and set HOST = 'localhost'

    If you encounter an error during the above command that ends with:

        TypeError: decode() argument 1 must be string, not None

    Then you need to add location values to your profile. Open your .bashrc file in an editor:

        $ vim ~/.bashrc

    Enter the following values at the end of the file and save.

        export LC_ALL=en_US.UTF-8
        export LANG=en_US.UTF-8

    Now, reload your bashrc changes

        source ~/.bashrc

    Now, rerun the syncdb command

6. Migrate the database to the latest updates

        $ python manage.py migrate



Part IV - Load some data
------------------------

To load GW's list of databases from libguides, first configure 
```local_settings.py``` with a list of libguides page sids.

Then, to load/parse/add databases from these pages to the database:

        $ ./manage.py load_databases

To test that that worked, try querying the html or json view:

        http://example.com/databases_html?q=proquest
        http://example.com/databases_json?q=proquest

To index the list of databases in Solr:

        $ ./manage.py index_all

Test that that worked with this path:

        http://example.com/databases_solr_html?q=proquest
        http://example.com/databases_solr_json?q=proquest

To load the Excel-formatted extract of journal titles:

        $ ./manage.py load_journals <JOURNALS_EXCEL_FILE>

To test that that worked, try querying the html or json view:

        http://example.com/journals_html?q=american
        http://example.com/journals_json?q=american

