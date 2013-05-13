from django.db import models
from cStringIO import StringIO


class Tag(models.Model):
  tag = models.CharField(max_length=100)

  def __unicode__(self):
      return self.tag

  class Meta:
      ordering = ["tag"]


class Reference(models.Model):
  tag = models.ForeignKey(Tag)
  book = models.CharField(max_length=100)
  chapter = models.IntegerField()
  firstLine = models.IntegerField()
  lastLine = models.IntegerField()
  created_at = models.DateTimeField(auto_now_add=True, editable=False, null=True)
  updated_at = models.DateTimeField(auto_now=True, editable=False, null=True)

  def __unicode__(self):
    return "%s @ %s" % (self.tag, self.pretty_ref())

  def pretty_ref(self):
    """
    A nice looking version of the reference.
    """
    s = "%s %d:%d" % (self.book.title().replace('_', ' '), self.chapter, self.firstLine)
    if (self.firstLine == self.lastLine):
      return s
    else:
      return s + "-" + str(self.lastLine)

  class Meta:
      ordering = ["book", "chapter", "firstLine", "tag", "lastLine"]


def get_exact_tag(query):
  """ Raises DoesNotExist exception 
  """
  return Tag.objects.get(tag=query)


def get_matching_tags(query):
  """ If tag starts with the query.
  """
  return Tag.objects.filter(tag__istartswith=query)



def get_refs_with_tag(tag):
  """
  Return QuerySet with all references which have this tag. 
  """
  return Reference.objects.filter(tag=tag);
    

def get_tags_for_ref(ref):
  """
  Get all tags which are linked to references which are covered
  by this ref.
  """
  tags = []
  for rel_ref in get_overlapping_refs(ref):
    tags.append(rel_ref.tag)
  return tags


def get_overlapping_refs(ref):
  """
  Return QuerySet with all references which are completely covered
  by this ref, so we know all their tags are on this ref.
  - find overlapping refs
    - filter on same book, same chapter, overlapping lines?
    - get each of their tags

    - get all the other refs which are a superset or subset?
  """
  return Reference.objects.filter(
      chapter=ref.chapter, book=ref.book, 
      firstLine__gte=ref.firstLine, lastLine__lte=ref.lastLine)


def get_export_tsv():
  out = StringIO()
  for ref in Reference.objects.all():
    print >>out, '\t'.join([ref.tag.tag, "NASB", ref.pretty_ref()])
  return out.getvalue()


def import_tsv_file(f):
  """ Parse the file input and create models.
  """
  line_num = 0
  successes = 0
  errors = 0
  def extract(v):
    v = v.strip()
    if len(v) == 0:
      raise Exception("Empty value")
    return v
  for chunk in f.chunks():
    for line in chunk.split('\n'):
      line = line.strip()
      line_num += 1
      vals = line.split('\t')
      if (len(vals) != 3):
        errors += 1
        print "Wrong number of values on line #%d = %d" % (line_num, len(vals))
        continue
      try:
        tag_name = extract(vals[0])
        book = extract(vals[1])
        chapter = int(extract(vals[2]))
      except:
        print "Bad value on line #%d" % line_num
        errors += 1
        continue
      # see if tag exists
      try:
        tag = get_exact_tag(tag_name)
      except:
        print "Creating new tag: " + tag_name
        tag = Tag(tag=tag_name)
        tag.save()
      # check for duplicates
      dups = Reference.objects.filter(tag=tag, book=book, chapter=chapter);
      print "found " + str(len(dups))
      if (dups):
        print "Skipping duplicate. with " + str(dups)
        continue
      ref = Reference(tag=tag, book=book, chapter=chapter, 
          firstLine="1", lastLine="2")
      ref.save()
      print "Creating new tagref"
      successes += 1
  return (errors, successes)
      

