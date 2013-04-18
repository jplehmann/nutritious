Tagz
====
Tagging app for all kinds of things (books, quotes, persons).

Can search a reference scope with q=
* Even regex support (encode + as %2b)
  * http://127.0.0.1:8000/tagz/lib/NASB/Luke?q=hi\w%2bt

Inbox
-----
- should search be case insensitive by default? (how could regex override?) -- might expect other normalization too, stemming

Bugs
----
- search bar when at library or tags is broken/unsupported

Tech Questions
---------
* how to have div (non-table) view but have dynamic column width, according to the longest items?
  - seems impossible to do a row-based approach like this because the rows are independent.  Could do a column layout with fixed height instead perhaps, but this sounds even worse.

Questions
---------
- do OSS analysis and decide if I should break -- what open source do I have
  here to show?
- divergences of ref simple ref and view ref, what to do? tests reflect actual
  api while reference api has moved on
- what to name this thing?
- how to assign colors to tags?
- if making a mutable resource (quotes), is that a django project, and where to
  put code? If not in pybooks, does this make testing hard?

Todo
----
* [0] merge resource and top level reference for uniformity
* [0] remove absolute paths (esp in view, try reverse())
* [1] integrate tagz into references (both ways)
  - show tags on references
* [1] Modification views
  * add a tag to a ref (allows creation of a new tag)
  * rename and delete tag
  * remove a ref from a tag
  * remove a tag from a ref
  * should a large portion of scripture show tags contained within it?
* [2] search for a tag (over all resources?)
  - [3] search with autocompletion, like delicious plugin
* UI features
  * [2] friendly copy-paste: maybe button to copy? better layout/selecable
    * [1] option for linerange to return single block instead
    * [1] then user could select multiple lines in chapter view to get a
          detail view with that range?
  * [2] context should work for a linerange too
  * [3] select search highlights all (can bootstrap do this?)
  * [3] navigation: more breadcrumbs (book, chapter links)
  * Tag search: along with references, words in bible book?
    * auto detect or have multiple search boxes?
* Style
  * wider reference column
  * how to handle when text spills over?
  * put HR before first row as well
  * streamline the left side references
* Tech stories
  * setup angular
  * setup LESS
* Design
  * properly load library resources -- best place for that logic?
  * return None rather than throwing, for easier inspection (text and children)
* tests for view/controllers: input mock resources and intercept template call
* paragraph markers
* could put library / resources in a navbar dropdown
* resource could provide some relative links for a navbar dropdown (OT/NT)
* Manually test quotes for new features, and need auto tests for this too... Put tests into simple and make sure quotes and bible use those.

Future Features
---------------
* Make it responsive, and rendering in nice size fonts for mobile.  Also add features like dropdown beneath search with book names.
* generalize to (bible, books, quotes, persons, webpages (page, video), gdocs)
  * inefficiency of searching bible refs with aliases
    * maybe one general ref endpoint takes guids but another specific one
      (refs/bible/xxx) does alias lookups
* plan/reorg around more apps (refs -> new app?)
- Tag Sets: each account can have sets of tags, one for general, one for a
  particular memory set. each tag can be in any number of sets. (many to
  many). I think this should be pretty easy to add as columns in the
  database. Seems really cool because just as my sets are meaningful to me
  they can extend them and be a place for life to look to.
- Comments: (noted elsewhere) the ability to attach comments. These are just
  like tags, except don't have a topic but do have a longer text portion.
- Index Notes (say google docs), tagging references there and creating
  an index, so that you have footnotes into your own documents and studies.
- break into pages for different levels rather than 1 view for ALL
    - index view (the "grid" look)
      - put the numbers on badges/buttons so they are bigger to click
      - jump to detail or jump to within chapter view (internal anchor)?
    - search view (2 columns: refs and text)
    - chapter view (1 column of text)
    - detail view (larger text, no inline refs)
* UI
  * auto-complete style box for searching on tags/refs
  * general search box that searches both tags and references, or one or the other
* Bible-specific
  * add book type filters: OT/NT / Pauline, etc -- SimpleListFilter
  * memorization logic like flash cards or even text reminders.
* admin
  * [template??] so admin columns not so wide
* models
  * timestamps of modifications and history view
* users
  * authentication to require login
  * multi-user: data stored separately for each user
* misc technical debt
  * upgrade to django 1.5
* show related tags (lexically, semantically)
* move bible-specific functionality into plugins


Design Discussion
-----------------
* more important to stay general to do other kinds of books, or to 
  be able to do more with this vertical?
  - decision:  Seems fairly easy to generalize a bit, and then get books and
    quotes in here.  If it's hard I won't do it.
{{{
    books: same a top level, just doesn't have any chapters
      - need to allow tags of top level resources
    quotation:
      - a 'bible' (volume?) would have a bunch of quote references
      - like a book: author, date?, text
}}}
* do we really need "resource" separate from the top level ref?
{{{
  - decision: this would simplify the implementation, but the benefits
    won't outweight the drawbacks when I do need something stored there,
    such as name and type.
  - why not make it a ref as well?
  - then add reference as a method of the root reference class
  * except for the Views implementation, we put a lot of logic at the top,
    so would have to see if I can put that in the root reference..
    (Maybe break them apart at this point)
}}}
Study my view and see how many attributes it has... 
  Each reference:
    - has a displayable / pretty form
    - is searchable
    - might have children
    - might have text
- would like ability to get parents() including root reference()
* add name, type to resource
  - why name?  what's wrong with the top reference's name?
  - well resources have a type
  - in any case top ref can also be a resoruce

Future Tech Stories
-------------------
* install sublime text2 and django plugins
  * CurrentScope, Djaneiro, SublimeCodeIntel, and SublimeLinter 
  * http://sontek.net/blog/detail/turning-vim-into-a-modern-python-ide#django


0.2
---
* [DONE] going up from a book is broken beccause links are inconsistent
* [DONE] let references generate their own full paths
* [DONE] add a header: Tags | Resources | History | Search [ ... ]
* [DONE] tags pages go to references
* [DONE] re-done chapter view with refs "inline"
* [DONE] nav bar
* [DONE] use smoke background
* [DONE] next/previous (child) links
* [DONE] [1] widen context +-3 (say of single verse, or chapter and highlight)
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



