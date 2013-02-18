from django.db import models

class Tag(models.Model):
  tag = models.CharField(max_length=100)
  def __unicode__(self):
      return self.tag

class Reference(models.Model):
  tag = models.ForeignKey(Tag)
  book = models.CharField(max_length=100)
  chapter = models.IntegerField()
  firstLine = models.IntegerField()
  lastLine = models.IntegerField()
  def __unicode__(self):
    return "%s @ %s %d:%d:%d" % (
      self.tag, self.book, self.chapter, self.firstLine, self.lastLine)

