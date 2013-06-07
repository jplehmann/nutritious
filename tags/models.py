import logging
import traceback
from cStringIO import StringIO

from django.db import models
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

from textbites import library


log = logging.getLogger("nutritious." + __name__)


class Tag(models.Model):
  user = models.ForeignKey(User)
  tag = models.CharField(max_length=100, db_index=True)

  def __unicode__(self):
      return self.tag

  class Meta:
      ordering = ["tag"]
      unique_together = ('user', 'tag')


class Reference(models.Model):
  user = models.ForeignKey(User)
  tag = models.ForeignKey(Tag)
  resource = models.CharField(max_length=100)
  reference = models.CharField(max_length=100, db_index=True)
  created_at = models.DateTimeField(auto_now_add=True, editable=False, null=True)
  updated_at = models.DateTimeField(auto_now=True, editable=False, null=True)
  # TODO revisit this null part
  offset_start = models.IntegerField(null=True)
  offset_end = models.IntegerField(null=True)

  def __unicode__(self):
    return "%s @ %s" % (self.tag, self.pretty_ref())

  def pretty_ref(self):
    """
    A nice looking version of the reference.
    """
    return str(self.reference)
    #s = "%s %d:%d" % (self.book.title().replace('_', ' '), self.chapter, self.firstLine)
    #if (self.firstLine == self.lastLine):
    #  return s
    #else:
    #  return s + "-" + str(self.lastLine)

  class Meta:
      ordering = ["offset_start", "offset_end", "resource", "reference", "tag"]


def user_pk(user):
  """ Return this user's pk or the one for guest if anonymous.
  """
  if user.is_authenticated():
    return user.pk
  # return "guest" for anonymous users
  return User.objects.get(username="guest").pk


def get_all_tags(user):
  return Tag.objects.filter(user=user_pk(user))


def get_exact_tag(user, query):
  """ Raises DoesNotExist exception 
  """
  return Tag.objects.filter(user=user_pk(user)).get(tag=query)


def get_matching_tags(user, query):
  """ If tag starts with the query.
  """
  return Tag.objects.filter(user=user_pk(user), tag__istartswith=query)


def get_refs_with_tag(user, tag):
  """
  Return QuerySet with all references which have this tag. 
  """
  return Reference.objects.filter(user=user_pk(user), tag=tag)
    

def get_tags_for_ref(user, ref):
  """
  Get all tags which are linked to references which are covered
  by this ref.
  """
  tags = []
  for rel_ref in get_overlapping_refs(user, ref):
    tags.append(rel_ref.tag)
  return tags


def get_overlapping_refs(user, ref):
  """
  Return QuerySet with all references which are completely covered
  by this ref, so we know all their tags are on this ref.
  - find overlapping refs
    - filter on same resource, overlapping offsets
    - get each of their tags
    - get all the other refs which are a superset or subset?
  """
  return Reference.objects.filter(
      user=user_pk(user),
      resource=ref.resource, 
      offset_start__gte=ref.offset_start, offset_end__lte=ref.offset_end)


def get_export_tsv(user):
  out = StringIO()
  for ref in Reference.objects.filter(user=user_pk(user)):
    offset_start = ref.offset_start
    offset_end = ref.offset_end
    resource = str(ref.resource)
    ref_str = str(ref.reference)
    # if offsets aren't known, look them up
    if not offset_start or not offset_end:
      try:
        pybook_ref = library.get(resource).reference(ref_str)
      except:
        log.info("Couldn't find refernce: %s", ref_str)
        continue
      try:
        offset_start, offset_end = pybook_ref.indices()
      except:
        log.warning("Problem with index: %s  %s", ref_str, traceback.format_exc())
    print >>out, '\t'.join(
        [ref.tag.tag, resource, ref_str, str(offset_start), str(offset_end)])
  return out.getvalue()


def import_tsv_file(user, f):
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
      # with or without offsets
      if (len(vals) != 3 and len(vals) != 5):
        errors += 1
        log.info("Wrong number of values on line #%d = %d", line_num, len(vals))
        continue
      try:
        tag_name = extract(vals[0])
        res = extract(vals[1])
        ref_str = extract(vals[2])
        offset_start = int(extract(vals[3])) if len(vals) == 5 else None
        offset_end = int(extract(vals[4])) if len(vals) == 5 else None
      except:
        log.info("Bad value on line #%d", line_num)
        errors += 1
        continue
      # see if tag exists
      try:
        tag = get_exact_tag(user, tag_name)
      except:
        log.debug("Creating new tag: %s", tag_name)
        tag = Tag(tag=tag_name, user=user)
        tag.save()
      # check for duplicates
      dups = Reference.objects.filter(tag=tag, resource=res, 
          reference=ref_str, user=user_pk(user));
      if (dups):
        log.debug("Skipping duplicate. with %s", str(dups))
        continue
      if offset_start == None:
        ref = Reference(tag=tag, resource=res, reference=ref_str, user=user)
      else:
        ref = Reference(tag=tag, resource=res, reference=ref_str, 
            offset_start=offset_start, offset_end=offset_end, user=user)
      ref.save()
      log.debug("Created new tagref: %s %s %s", tag, res, ref_str)
      successes += 1
  return (errors, successes)
      

def delete_tags(user, tag_names):
  for t in tag_names:
    delete_tag(user, t)


def delete_tag(user, tag_name):
  # NOTE: do we want to 404 here? this would be a 500 if we are the 
  # one who got this list of tags.  TODO: use try catch then 404 in 
  # the view instead
  t = get_object_or_404(Tag, tag=tag_name, user=user_pk(user))
  # clean up all associated references, since references only have 1 tag in them
  # but this seems to not be necessary, maybe Django is cleaning up
  # for me?
  for ref in get_refs_with_tag(user, t):
    ref.delete()
  log.debug("Deleting tag and all refs for: %s", t.tag)
  t.delete()
