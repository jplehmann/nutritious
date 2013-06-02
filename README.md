Nutritious
==========
Nutritious is a Django-based web application for browsing and tagging textual content.  It generalizes beyond "delicious"-style tagging of webpages to within-document bookmark-like tags on arbitrary collections of text (e.g., a quotations library).  It also provides navigation within these resources as well as regex-based search.

A live demo can be seen at [nutritious.herokuapps.com][1].

Features
--------
* Browsing of textual resources.
* Search by keyword/regex, textbite reference, or tag name (#tag).
* Highlighted context expansion.
* RESTful access to textual resources and tag data
* Create/delete/rename of tags and their references.
* Import and export of tag data from/to TSV.
* User accounts (though currently admin creates new users).
* Unauthenticated read-only access to "guest" account.
* Hotkeys for search (Ctrl-S) and copying (Ctrl-C) and tagging (Ctrl-T) of selected lines.
* Integration tests with Angular Scenario Test Runner.

Details
-------
Nutritious enables the browsing and tagging of [Textbites][2] resources. Textbites provides a Python API for a textual resource. 

* Tag data are persisted in a Postgres DB.
* Textbites are currently limited to static resources.

[1]: http://nutritious.herokuapps.com
[2]: http://github.com/jplehmann/textbites

Dependencies
------------
* Django (1.4.4)
* AngularJS
* Twitter Bootstrap
* LESS CSS

Usage
-----
Installing Nutritious should be mostly similar to any Django app, but here are some tips.

Installing locally:

* Install pip and ideally virtualenv. 
* Install dependences through pip.
* Install the LESS CSS compiler (`npm install -g less`)
* Setup a postgres database.
  * Install postgres.
  * Create nutritious database.
  * Run ./manage.py with syncdb and migrate.
* Using the admin interface create "guest" user.
* Set environment variables NUTRITIOUS_SECRET_KEY, NUTRITIOUS_TESTING_PW, NUTRITIOUS_DATABASE_URL

Deploying to Heroku:
 
* For LESS CSS, configure buildpack as a 'multi':
   * `heroku config:add BUILDPACK_URL=https://github.com/ddollar/heroku-buildpack-multi.git`
* Sync and migrate the database using `heroku run python manage.py ...`.
* Set passwords in environment variables with `heroku config:add XXX=YYY`

