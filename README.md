Tagz
====
Tagging app for all kinds of things (books, quotes, persons).

0.1: Vtag with a Web Frontend
-----------------------------
* [DONE] hosting with bitbucket
* [DONE] rename the dirs
* [DONE] load fixture data into database
* [DONE] setup virtualenv: source ~/.venv/tagz/bin/activate
* [DONE] switch to postgres (for heroku)
* [DONE] setup DATABASE_URL correctly on Heroku 
* [DONE] setup DATABASE_URL locally
* [DONE] load data into heroku
* [DONE] get it deployed to heroku and working
* [DONE] timestamps for ref creation
* [DONE] customize the admin
* [DONE] View: tags alphabetically
* [DONE] View: references by ref
* [DONE] View: index 
* [DONE] View: All Tags: for each show list of refs
* [DONE] View: Single Tag: for each show other tags on that ref
* get views working on Heroku


Questions
---------
* what can be computed in a template?  
  * (len(items))
  * can I access a dictionary?  do i have to always zip?
* if I didn't specify Procfile web, would I have o started it manually?
* how to deploy my support libs (Vtag, Bible libs)
* how to organize HTML, css, javascript

Future Features
---------------
* create a Bible sort order
* show full book names not the abbreviations
* add book type filters: OT/NT / Pauline, etc -- SimpleListFilter
* [template??] so admin columns not so wide
* timestamps of modifications and history view
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



