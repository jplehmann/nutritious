Inbox
-----

Modify
------
TODO:
  o change database in the fields it stores
    - put unique constraint on "tag name"
    - tag, resource, ref, index.start, index.end
{{{
    ** changing this to a string causes some problems... right now I know
      when references overlap, and so when I show some text, I can show
      all the associated tags.  
      Or when I show a tag, and I show all tagrefs for that tag, for
      each tagref, I can get the other tags.. In other words, I need to
      be able to associate/normalize the refs. 
        If I have a ref, say John 3:16, then I need to be able to find out
        what tags mark this.  Or say John 3:1-3, which tags cover this span?

      you can say for a tag, give me refs

      you can't say for a ref give me tags -- unless you have this
      functionaliy: the db has no way of knowing what overlaps, 
      and since i am not enforcing any standard on what refs look like,
      IE lines, then I can't analyze it within the db.

      Maybe the interface can provide a notion of start and end... computed
      however it wants. for example line + chapter*1000 + book#*1,000,000
      so I can then check if start and end positions are overlapping.
      It doesn't have to be reversable although it could be... in which case
      i wouldn't need to store a text ref possibly.

      How to create the algo which converts book/chap/line into a well ordered
      number? have to ensure that enough of a smaller can't roll over into
      the next digit.   dot notiationw ould work, except the DB can't compae that.
      though, it could maybe compare alphabetically.
      
      ** actually it just needs to be the lin number in the resource. So if
      lines have global IDS.
}}}
  o update endpoint to rename a tag
{{{
  def update():
    tagNew = Tag.objects(tag=newName)
    if not tagNew:
      tagOld.name = newName
    else:
      for r in tagOld.references():
        r.tag = tagNew
      tagOld.delete()
      
}}}
  o import TSV
  o export TSV

DONE: 
{{{
  x create form for an existing tag OR a new one
  x create GET detail for tagref
    * problem of specifying an ID is that it may not be consistnet with path,
      and is redundant, I guess I can just enforce consistency.
    - should tag detail be same as edit?
    - should after creating go to detail/get page?
  x fix initial value of existing tag: how to pass to angular? need to
    set default value on model/controller

TAGS
x read:
    GET /tags/<tag>
x create: (should just be implicit when a tagref is created)
    POST /tags/createform
o update: rename the tag (could collapse?) *FORM*
    PUT /tags/<tag>
x delete: remove all references
    DEL /tags/<tag>

TAGREFS
x read:
    GET /tags/<tag>/refs/<id>
x create: associates a tag with a ref *FORM*
    POST /tags/<tag>/refs/createform
x update: -- dont allow this  --
    (none)
x delete: remove a reference
    DEL /tags/<tag>/refs/<id>

  Currently:
    Reference has book/chp/first/last, tag
    Change to: resource, reference

  FORM for creation of a tagref:
    tag name -- select OR new input field
      - validte: confirm creation of new
    resource: pick
    reference: freeform text input (could look it up through/valdiate)
      - validate: check if ref exists
}}}

Bugs
----
- AttributeError: BibleResource instance has no __call__ method
- search bar when at library or tags is broken/unsupported
- anger tag has 0 John ref

Todo
----
- first pass documentation: both get a readme describing what they're for, what technology they use, where they're hosted? and features and todos?
- rename packages "Nutricious" and "Textbites"
- rename library to resources "res"
- open source resources -- pride and prejudice, NKJV, quotes, some web text where tagging makes sense
- move to github

0.4
---
* create and edit tags (rename?)
* authentication to protect writes
- browser test would be really good at this point, lots of functionality
- export tags database to xml/json
* more bible versions (easy) (and figure out copyright issue)
- should search be case insensitive by default? (how could regex override?) -- might expect other normalization too, stemming

0.5
---
* remove absolute paths (esp in view, try reverse())
* integrate tagz into references
- click search should select all to replace
- shortcut key to do search
* autocomplete for tag search (medium) (AJAX query for tags) angular UI select2 or "chosen" (has nice multi-select)
* friendly copy-paste: maybe button to copy? better layout/selecable (maybe linerange returns a single block, and let user select linerange)
* add URLs as a resource type (export my delicious)

1.0
---
* context should work for a linerange too
* select search highlights all (can bootstrap do this?)
* navigation: more breadcrumbs (book, chapter links)
* Tag search: scope tags to certain resources/refs
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

2.0
---
* Mutability for resources like Quotes
* Responsiveness: rendering in nice size fonts for mobile.  Also add features like dropdown beneath search with book names.
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


Tech Questions
---------
- rename does a PUT and then is redirected with what should be a GET. The browser says its doing a GET but the server says it got a second PUT. Which is true? what is wrong?
- how to have delete let server do the redirect? I think the AJAX eats it.  after deleting let controller say where to go.
- How to go straight to a view method but change the path? Is a redirect required?  
  - For example how to in /lib?q=#tags go to /tagz/tags/... -- preferrably not with a redirect because I already have the list of things I want to show, I've done the serach at this point.  
  - so this problem occurs when an intermediate URL needs to do some of the work, and we dont want to redo that work.
  - Figute out the best way to write my search method which redirects back to a resource if one was provided. Or if we wanted to do a scoped search with a tag, how would that work? My goal was that search should centralize the searching... Maybe it also needs to handle searches over resources.
* how to have div (non-table) view but have dynamic column width, according to the longest items?
  - seems impossible to do a row-based approach like this because the rows are independent.  Could do a column layout with fixed height instead perhaps, but this sounds even worse.


Questions
---------
- divergences of ref simple ref and view ref, what to do? tests reflect actual
  api while reference api has moved on
- how to assign colors to tags?
- if making a mutable resource (quotes), is that a django project, and where to
  put code? If not in pybooks, does this make testing hard?


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

0.2
---
* [DONE] break into pages for different levels rather than 1 view for ALL
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
* [DONE] search for tag reference first then query
* [DONE] multiple tag results

