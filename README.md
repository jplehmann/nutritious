Tagz
====
Tagging app for all kinds of things (books, quotes, persons).

Can search a reference scope with q=
* Even regex support (encode + as %2b)
  * http://127.0.0.1:8000/tagz/lib/NASB/Luke?q=hi\w%2bt


Questions
---------


Priorities?
-----------
Higher:
1. integrate tagz into references
  - show tags on references
  - tags pages go to references
2. ability to add/edit a tag (same screen)
3. search for a tag
  - search with autocompletion


* more important to stay general to do other kinds of books, or to 
  be able to do more with this vertical?
--> Seems fairly easy to generalize a bit, and then get books and quotes in here.
    books: same a top level, just doesn't have any chapters
      - so allow tags of top level resources
    quotation:
      - a 'bible' (volume?) would have a bunch of quote references
      - like a book: author, date?, text

* do we really need "resource" separate from the top level ref?
--> this would simplify the implementation
  - why not make it a ref as well?
  - get rid of 
  - then add reference as a method of the root reference class
  * except for the Views implementation, we put a lot of logic at the top,
    so would have to see if I can put that in the root reference..
    (Maybe break them apart at this point)

Study my view and see how many attributes it has... 
  Each reference:
    - has a displayable / pretty form
    - is searchable
    - might have children
    - might have text

TODO: Might be better to retrun None rather than throwing, as this would make
it easier to inspect hte refs dynamically...

would like ability to get parents() including root reference()

* add name, type to resource

Todo
----
* button to click for context (+/- 3): -> parent -> children, if current is indexed
* tests for view/controllers: input mock resources and intercept template call
* setup angular
* setup LESS
* select search highlights all 
* widen context +-3 (say of single verse, or chapter and highlight)
* think about how to represent books and quotes
* style
  * wider reference column
  * how to handle when text spills over?
  * put HR before first row as well
  * streamline the left side references
* how to layout for friendly copy-paste?
* consider how to bring in topics / tagz??

* more breadcrumbs (resource top, book, chapter links)
* properly load library resources -- best place for that logic?
* create stylesheets for each page
* add a header: Tags | Resources | History | Search [ ... ]
  * search: tag search, references, words in bible book?
  * auto detect or have multiple search boxes?
* should a large portion of scripture show tags contained
  within it?
* add next verse/chapter links
* with and without verse number
* verses on own line or not
* search within book of the bible
* modification views
  * rename and delete tag
  * remove a ref from a tag
  ---
  * remove a tag from a ref
  * add a tag to a ref (allows creation of a new tag)


0.2
---
* pybooks support with endpoints for resource and reference within
  - [DONE] navigate through 'references'
    * 2 dimensional indexes
  - [DONE] search through book in bible
* [DONE] search for reference first then query

0.1
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
* [DONE] style views with CSS
* [DONE] add bootstrap styling
* [DONE] heroku: database migrated
* [DONE] heroku: pybible: as git+https from a read only account on bitbucket installed as package data


Future Features
---------------
* generalize to (bible, books, quotes, persons, webpages (page, video), gdocs)
  * inefficiency of searching bible refs with aliases
    * maybe one general ref endpoint takes guids but another specific one
      (refs/bible/xxx) does alias lookups
* plan/reorg around more apps (refs -> new app?)
* come up with an initial design for the pages -- sketch it out
  * plan create/modify views
  * research: delicious
---
* UI
  * auto-complete style box for searching on tags/refs
  * general search box that searches both tags and references, or one or the other
* Bible-specific
  * create a Bible sort order
  * show full book names not the abbreviations
  * add book type filters: OT/NT / Pauline, etc -- SimpleListFilter
* admin
  * [template??] so admin columns not so wide
* models
  * timestamps of modifications and history view
* system
  * authentication to require login
  * multi-user: data stored separately for each user
* misc technical debt
  * upgrade to django 1.5

Future Tech Stories
-------------------
* install sublime text2 and django plugins
  * CurrentScope, Djaneiro, SublimeCodeIntel, and SublimeLinter 
  * http://sontek.net/blog/detail/turning-vim-into-a-modern-python-ide#django

Way Future
----------
* show related tags (lexically, semantically)
* move bible-specific functionality into plugins



