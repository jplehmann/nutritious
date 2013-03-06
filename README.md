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
* [DONE] turn bible sources into a package as a support lib
* [DONE] create API for my support libs
* [DONE] show scripture on the tag page
* [DONE] detail view for references
* get views working on Heroku (also pybible)


Questions
---------
* how to organize HTML, css, javascript

Future Features
---------------
* upgrade to django 1.5
* style views with CSS
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

Way Future
----------
* show related tags (lexically, semantically)
* move bible-specific functionality into plugins



