from django.db import models


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


def get_refs_with_tag(tag):
  """
  Return QuerySet with all references which have this tag. 
  """
  return Reference.objects.filter(tag=tag);
    

def get_tags_for_ref(ref):
  tags = []
  for rel_ref in get_overlapping_refs(ref):
    tags.append(rel_ref.tag)
  return tags


def get_overlapping_refs(ref):
  """
  Return QuerySet with all tags that are on refs that are completely
  covered by this ref, so we know all their tags are on this ref.
  - find overlapping refs
    - filter on same book, same chapter, overlapping lines?
    - get each of their tags

    - get all the other refs which are a superset or subset?
  """
  return Reference.objects.filter(
      chapter=ref.chapter, book=ref.book, 
      firstLine__gte=ref.firstLine, lastLine__lte=ref.lastLine)
