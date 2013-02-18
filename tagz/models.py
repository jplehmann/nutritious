from django.db import models

class Tag(models.Model):
  tag = models.CharField(max_length=100)
  def __unicode__(self):
      return self.tag

class Reference(models.Model):
  book = models.CharField(max_length=100)
  chapter = models.IntegerField()
  def __unicode__(self):
    return self.book + " " + str(self.chapter)

class Annotation(models.Model):
  tag = models.ForeignKey(Tag)
  reference = models.ForeignKey(Reference)
  firstLine = models.IntegerField()
  lastLine = models.IntegerField()
  def __unicode__(self):
    return "%s @ %s:%d:%d" % (
      self.tag, self.reference, self.firstLine, self.lastLine)

