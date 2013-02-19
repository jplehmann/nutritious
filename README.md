Tagz
====
Tagging app for all kinds of things (books, quotes, persons).

0.1: Vtag with a Web Frontend
-----------------------------
* [DONE] hosting with bitbucket
* [DONE] rename the dirs
* [DONE] load fixture data into database
* setup virtualenv
* [PARTIAL] get it deployed to heroku and working
  * https://devcenter.heroku.com/articles/django
* View: All Tags: for each show list of refs
  * View
  * Template
* View: Single Tag: for each show other tags on that ref
  * View
  * Template

Questions
---------
* how to deploy my support libs (Vtag, Bible libs)
* how to organize HTML, css, javascript

Future Features
---------------
* auto-complete style box for searching on tags/refs
* integrate and style with bootstrap
* authentication to require login
* multi-user: data stored separately for each user
* restful paths to tags and references
* general search box that searches both tags and references, or one or the other
* integrate/display scripture
* generalize to (books, quotes, persons)

Future Tech Stories
-------------------
* install sublime text2 and django plugins
  * CurrentScope, Djaneiro, SublimeCodeIntel, and SublimeLinter 
  * http://sontek.net/blog/detail/turning-vim-into-a-modern-python-ide#django
* switch database to Postgres or MongoDB
* deploy my support libs (Vtag, Bible libs)
* create API for my support libs

Way Future
----------
* show related tags (lexically, semantically)
* move bible-specific functionality into plugins



