
Backlog
=======
- search term lost after search
- search should link straight to context
- tag on context page gets wrong resource; get from url?
- put nav at bottom of verses too

Todo
----


* move to github
  - travis CI -- once I'm on github
  - first pass documentation: readme, features, todos

* more browser tests
  * delete all
    - delete all needs to take user to login screen
    - even get or 404 thinsg are broken in logged out mode?

- need to secure any writes (e.g. length of write) so I can make integration test pw insecure

- how to store other resources in a protected way and load when deploying
  (dependency, or EWS with password but cache)

- delete all
  - move 404 to view?
  - why getting error on purl sometimes?, also createform
  - need double check: are you sure?

Testing
-------
- add to tests: login with testing account, delete all, and import testing fixture
- tests running too slowly on heroku, how to fix? set greater timeout on heroku
  or use angular XHR?
{{{
x search
{{{
  x reference
      x book
      x chapter
      x line
  x keyword query
      x 'Adam'
  o tags
      x tag exact
      - tag prefix -> single
      - tag prefix -> list
      - tag match none
}}}
o clicking links
{{{
  o resource 
      -> book
      -> chapter
  o book 
      -> chapter
      -> line

  o line -> context
}}}
o navigational links
{{{
    resource - no nav links
    book -> top, up, next, prev (next and prev disabled if last, first)
    chapter ->  (same)
    line -> (same)
    context -> top, up, prev/next disabled
}}}
o authentication
{{{
  that you can do all the above as a guest
    but not create tag
  test login
    verify that you can create a tag
    delete it
  logout
    verify that you are logged out
}}}
o power user
{{{
  o select lines and copy to buffer and paste?
  o select lines and ctrl-t tag
  o ctrl-S to search
}}}
o import and export -- do roundtrip test
o tags
{{{
  - all tags
    - listing of all tags (check count)
    - create tagref
      - new tag
      - pre-existing tag
    - delete tag
  - tag detail (lists all verses)
    - create (another tagref for this tag)
    - delete tag
    - rename tag
      - if other doesn't exsit
      - if other does exist
    - per tagref
      - test link to refernece
      - view tagref
      - delete tagref
}}}
o test other kinds of resources
{{{
  - PIP TEST1
    - navigation
    - create a tag on another resource as well

  - quotes
}}}

}}}


Bugs
----
- ajax tag creation/deletion
  - delete tag on tag detail gives 404 though it works
  - tagref detail
    - rename doesnt redirect: rename does a PUT and then is redirected with what should be a GET. The browser says its doing a GET but the server says it got a second PUT. Which is true? what is wrong?
    - delete tagref on tag detail is also broken, doesnt work at all
  - in general figure out right way to handle responses in AJAX which require
    redirects, etc. I think the AJAX eats it.  after deleting let controller
    say where to go.
- cannot use Ctrl-T on Linux (why some Ctrl-S override, but not others?)
* because of missing lines (e.g NIV) line lookups can be off by 1, this is a but in pybooks for reference search -- fix by inserting blank lines
* search bar when at library or tags is broken/unsupported
- plus import/export endpoints are ambiguous with tag names
- anger tag has 0 John ref
- getting index offsets, about 20 errors when exporting
- getting index offsets, about 20 errors couldn't find references

Smaller
-------
* select, tag and copy from Search page and Tag Detail page
  * create a directive for displaying verses to use in all 3+ places
* search
  * parallel search
  {{{
    * with a meta flag like @all, OR maybe aliases like @bible
    which maps to a set of resources (stored in library), then search each. 
    * search across all, but then render using current resource knowing that double
    click can expand out to the other versions. (depends on parallel lookup)
  }}}
  * tag search: scope tags to certain resources/refs with @x
  * tag search with multiple tags and operators (+ = must have, - = can't have), default is disjunction.
  * highlight search terms (textbites to return offsets)
  * make search case insensitive
* parallel lookup
{{{
  * double click on a line to trigger a lookpu on all 
  resources in the library with that reference, then display them below
  in a collapse-like fold. Double click on the first again to close. Need
  to display resource name somewhere on the line or beside it?
  * figure out how to make this work with copy/paste range
}}}
* custom 404 page
* random tags view
* add URLs as a resource type (export my delicious) (wait until mutable sources?)
* figure out copyright issues 
* open source resources -- pride and prejudice??
* tag list / search result set should allow multi-select of results, then ability to "add tag" to that set, or remove
* context should work for a linerange too
* navigation: more breadcrumbs (book, chapter links)
* paragraph markers
* design for less views
  * could put library / resources in a navbar dropdown
* related tags and texts popover on text view
* Manually test quotes for new features, and need auto tests for this too... Put tests into simple and make sure quotes and bible use those.
  * quotes / any simple resource: needs a path test, indices test
* validation for input
  * such as friendly message when refernce for tagref is bad
    * quotes wont show text for a person, yet we can create a reference to it.
      how could we validate this earlier on?
* D3 visualizations about tags
* autocomplete for tag search (AJAX query for tags) angular UI select2 or "chosen" (has nice multi-select)
* book groups with @xxx
* historical view of tagref changes

Larger
------
* Mutability for resources like Quotes, Links (database-backed textbites)
* generalize to other resource types with attributes (bible, books, quotes, persons, webpages (page, video), gdocs)
* metatags/tagsets: sets of other tags (and metas?), and can have color
  * each account can have sets of tags, one for general, one for a
    particular memory set. each tag can be in any number of sets. (many to
    many). I think this should be pretty easy to add as columns in the
    database. Seems really cool because just as my sets are meaningful to me
    they can extend them and be a place for life to look to.
  * memorization logic like flash cards or even text reminders
* Comments: (noted elsewhere) the ability to attach comments. These are just
  like tags, except don't have a topic but do have a longer text portion.
* Index Notes (say google docs), tagging references there and creating
  an index, so that you have footnotes into your own documents and studies.
* show related tags (lexically, semantically)
* Responsiveness: rendering in nice size fonts for mobile.  Also add features like dropdown beneath search with book names.

Tech Stories
------------
- Upgrade to Django 1.5
- Use a RESTful framework like django-rest-framework
- Explore Generic class-based views


Discussion
==========

Tech Questions
---------
- Look into how to using Angular $http instead of form post
- Find out in general how to handle redirecting after ajax
- can relative template paths be named like urls?
- rename does a PUT and then is redirected with what should be a GET. The browser says its doing a GET but the server says it got a second PUT. Which is true? what is wrong?
- how to have delete let server do the redirect? I think the AJAX eats it.  after deleting let controller say where to go.
* How to go straight to a view method but change the path? Is a redirect required?
  * For example how to in /lib?q=#tags go to /tagz/tags/... -- preferrably not with a redirect because I already have the list of things I want to show, I've done the serach at this point.
  * so this problem occurs when an intermediate URL needs to do some of the work, and we dont want to redo that work.
  * Figute out the best way to write my search method which redirects back to a resource if one was provided. Or if we wanted to do a scoped search with a tag, how would that work? My goal was that search should centralize the searching... Maybe it also needs to handle searches over resources.
* how to have div (non-table) view but have dynamic column width, according to the longest items?
  - seems impossible to do a row-based approach like this because the rows are independent.  Could do a column layout with fixed height instead perhaps, but this sounds even worse.
- divergences of ref simple ref and view ref, what to do? tests reflect actual
  api while reference api has moved on
- if making a mutable resource (quotes), is that a django project, and where to
  put code? If not in pybooks, does this make testing hard?


Design
------
* more important to stay general to do other kinds of books, or to 
  be able to do more with this vertical?
  * decision:  Seems fairly easy to generalize a bit, and then get books and
    quotes in here.  If it's hard I won't do it.
{{{
    * books: same a top level, just doesn't have any chapters
      * need to allow tags of top level resources
    * quotation:
      * a 'bible' (volume?) would have a bunch of quote references
      * like a book: author, date?, text
}}}
* do we really need "resource" separate from the top level ref?
{{{
  * decision: this would simplify the implementation, but the benefits
    won't outweight the drawbacks when I do need something stored there,
    such as name and type.
  * why not make it a ref as well?
  * then add reference as a method of the root reference class
  * except for the Views implementation, we put a lot of logic at the top,
    so would have to see if I can put that in the root reference..
    (Maybe break them apart at this point)
}}}
* Study my view and see how many attributes it has... 
  * Each reference:
    - has a displayable / pretty form
    - is searchable
    - might have children
    - might have text
* add name, type to resource
  - why name?  what's wrong with the top reference's name?
  - well resources have a type
  - in any case top ref can also be a resoruce
* Rest Endpoints
  {{{
  * TAGS
    * read:
        GET /tags/<tag>
    * create: (should just be implicit when a tagref is created)
        POST /tags/createform
    * update: rename the tag (could collapse?) *FORM*
        PUT /tags/<tag>
    * delete: remove all references
        DEL /tags/<tag>

  * TAGREFS
    * read:
        GET /tags/<tag>/refs/<id>
    * create: associates a tag with a ref *FORM*
        POST /tags/<tag>/refs/createform
    * update: -- dont allow this  --
        (none)
    * delete: remove a reference
        DEL /tags/<tag>/refs/<id>

  * Currently:
    * Reference has book/chp/first/last, tag
    * Change to: resource, reference

  * FORM for creation of a tagref:
    * tag name -- select OR new input field
      * validte: confirm creation of new
    * resource: pick
    * reference: freeform text input (could look it up through/valdiate)
      * validate: check if ref exists
  }}}


History
=======

0.1
---
* hosting with bitbucket
* rename the dirs
* load fixture data into database
* setup virtualenv: source ~/.venv/tagz/bin/activate
* switch to postgres (for heroku)
* setup DATABASE_URL correctly on Heroku 
* setup DATABASE_URL locally
* load data into heroku
* get it deployed to heroku and working
* timestamps for ref creation
* customize the admin
* View: tags alphabetically
* View: references by ref
* View: index 
* View: All Tags: for each show list of refs
* View: Single Tag: for each show other tags on that ref
* turn bible sources into a package as a support lib
* create API for my support libs
* show scripture on the tag page
* detail view for references
* style views with CSS
* add bootstrap styling
* heroku: database migrated
* heroku: pybible: as git+https from a read only account on bitbucket installed as package data

0.2
---
* break into pages for different levels rather than 1 view for ALL
* going up from a book is broken beccause links are inconsistent
* let references generate their own full paths
* add a header: Tags | Resources | History | Search [ ... ]
* tags pages go to references
* re-done chapter view with refs "inline"
* nav bar
* use smoke background
* next/previous (child) links
* [1] widen context +-3 (say of single verse, or chapter and highlight)
* pybooks support with endpoints for resource and reference within
  * navigate through 'references'
    * 2 dimensional indexes
  * search through book in bible
* search for tag reference first then query
* multiple tag results

0.3
---
* new restful operations on tag: create, delete, rename
* new restful operations on tag refs: create, delete
* forms for create and modify tag/tagrefs
* import TSV
* export TSV
* resources contain index/offsets
* new database schema, migrated and code updated
* more bible versions
* authentication to protect writes
* multi-user: data stored separately for each user
* guest account for not logged in users
* select verses and copy -- Cmd/Ctrl-C with ZClip
* search
  * Ctrl-S shortcut key to do search
  * click search should select all to replace
* select verses and tag -- Cmd/Ctrl-T (ideally a pop-up or modal)
* setup LESS: http://stackoverflow.com/a/8726853/317110
* rename projects to nutritious and textbites
* split out texts app
* rename tagz app to tags and rebuild databases
* angular scenario test runner test
