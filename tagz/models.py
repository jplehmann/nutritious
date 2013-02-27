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


def get_refs_with_tag(the_tag):
  """
  Return QuerySet with all references which have this tag. 
  """
  return Reference.objects.filter(tag=the_tag);
    

