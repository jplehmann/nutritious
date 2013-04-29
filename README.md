Nutritious
==========
Nutritious is a Django-based web application for browsing and tagging textual content, inspired by Delicious.  It generalizes tagging beyond webpages to within-document bookmark-like tags, and can apply to arbitrary collections of text, such as a quotation library.  In addition it provides navigation within these resources as well as regex-based search.

A live demo can be seen at [nutritious.herokuapps.com][1].

Details
-------
Nutritious enables the browsing and tagging of [Textbites][2] resources. Textbites provides a Python API for a textual resource. 

* Tags are persisted in a Postgres DB.
* Currently all Textbite are static, though this is a future feature.
* Nutritious does not currently support multiple users.


[1]: http://nutritious.herokuapps.com
[2]: http://github.com/jplehmann/textbites


Features
--------
* RESTful paths to resources and tags
* Browsing of textual resources
  * Highlighted context expansion
* Scoped search (with q=)
  * Even regex support (encode + as %2b)
    * http://127.0.0.1:8000/tagz/lib/NASB/Luke?q=hi\w%2bt
* Tags library
  * Tags search
* Several different kinds of Textbite implementations (books, bible, quotes)


Technical 
---------
* Django 1.4.4


