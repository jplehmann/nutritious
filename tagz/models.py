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
  #created_at = models.DateTimeField(auto_now_add=True, editable=False)
  #updated_at = models.DateTimeField(auto_now=True, editable=False)

  def __unicode__(self):
    return "%s @ %s %d:%d:%d" % (
      self.tag, self.book, self.chapter, self.firstLine, self.lastLine)
    
  class Meta:
      ordering = ["book", "chapter", "firstLine", "tag", "lastLine"]


