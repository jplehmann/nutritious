import logging
import traceback

from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.core.urlresolvers  import reverse
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.http import Http404
from django.template import RequestContext
from django import forms
from django.contrib.auth.decorators import login_required

from textbites import library

from tags.models import Tag
from tags.models import Reference
from tags.models import get_all_tags
from tags.models import get_tags_for_ref
from tags.models import get_exact_tag
from tags.models import get_matching_tags
from tags.models import get_refs_with_tag
from tags.models import get_export_tsv
from tags.models import import_tsv_file


log = logging.getLogger("nutritious." + __name__)


def tag_search(request, query):
  """ Searches for a tag with exact and fuzzy matching.

  Currently only supports a single tag, and must begin with #.
  """
  query = query.strip()
  if query.startswith("#"):
    # search the tags
    query = query[1:]
    try:
      # exact match
      match = get_exact_tag(request.user, query)
      return redirect(reverse('tags') + match.tag)
    except:
      # starts-with match
      matches = get_matching_tags(request.user, query)
      # render even if no tags found
      return render_tags(request, matches)
  # root search must contain only an #tag
  raise Http404 


def tags(request, tags=None):
  """ Show tags. If no tags are provided, shows all tags.
  """
  if request:
    query = request.GET.get('q', None)
    if query:
      return tag_search(request, query)
  all_tags = get_all_tags(request.user) if tags == None else tags
  return render_tags(request, all_tags)


def render_tags(request, tags):
  """ Render the given tags. 
  """
  counts = []
  for t in tags:
    refs = get_refs_with_tag(request.user, t)
    counts.append(refs.count())
  counted_tags = zip(tags, counts)
  return render_to_response('tags/tag_index.html',
      {'counted_tags': counted_tags},
      context_instance=RequestContext(request))


def tag(request, tag_name):
  """ Show all references for single tag and related tags.
  """
  if request.method == 'DELETE':
    return tag_delete(request, tag_name)
  elif request.method == 'PUT':
    return tag_update(request, tag_name)
  t = get_object_or_404(Tag, tag=tag_name, user=request.user)
  related_refs = get_refs_with_tag(request.user, t)
  clean_refs = []
  related_tags = []
  texts = []
  ref_paths = []
  ids = []
  for ref in related_refs: 
    related_tags.append(get_tags_for_ref(request.user, ref))
    ids.append(ref.id)
    resource = ref.resource
    try:
      pybook_ref = library.get(resource).reference(ref.pretty_ref())
      text = pybook_ref.text()
      clean_ref = pybook_ref.pretty()
    except Exception:
      log.warning("Exception for " + ref.pretty_ref() + " = " + traceback.format_exc())
      text, clean_ref = ('unknown', ref.pretty_ref())
    clean_refs.append(clean_ref)
    texts.append(text)
    ref_paths.append(reverse('resource', args=(resource, ref.pretty_ref())))
  related_refs_n_tags = zip(ids, clean_refs, ref_paths, related_tags, texts)
  return render_to_response('tags/tag_detail.html',
      {'tag': t, 'related_refs_n_tags': related_refs_n_tags},
      context_instance=RequestContext(request))


@login_required
def tag_delete(request, tag_name):
  """ Delete a tag and all associated tagrefs.
  """
  t = get_object_or_404(Tag, tag=tag_name, user=request.user)
  # clean up all associated references, since references only have 1 tag in them
  # but this seems to not be necessary, maybe Django is cleaning up for me?
  for ref in get_refs_with_tag(request.user, t):
    ref.delete()
  t.delete()
  # FIXME: not doing anything when called from AJAX request b/c response eats it
  return HttpResponseRedirect(reverse('tags'));


@login_required
def tag_update(request, tag_name):
  """ Rename a tag; if the tag name exists already, merge them.
  """
  t_old = get_object_or_404(Tag, tag=tag_name, user=request.user)
  try:
    new_name = request.GET.get('name', None)
  except:
    log.debug("Problem renaming tag\n%s", traceback.format_exc())
  log.debug("renamed tag: old name, new: %s, %s", tag_name, new_name)
  try:
    t_new = get_exact_tag(request.user, new_name)
    for r in get_refs_with_tag(request.user, t_old):
      r.tag = t_new
      log.debug("updating ref: " + str(r))
      r.save()
    t_old.delete()
  except:
    log.error("Error renaming tag: %s", traceback.format_exc())
    t_old.tag = new_name
    t_old.save()
  return HttpResponseRedirect(reverse('tag', args=new_name));


def tagref_detail(request, tag_name, id):
  """ Show detail for a tagref.
  """
  tagref = get_object_or_404(Reference, id=id, user=request.user)
  # make sure the tag with this id belongs under this path
  if (tag_name != tagref.tag.tag):
    log.info("Mismatched tag name path with id '%s' '%s'", tag_name, tagref.tag.tag)
    raise Http404
  if request.method == 'DELETE':
    tagref.delete()
    # TODO: if this is the last ref for this tag, delete the tag?
    # not doing anything when called from AJAX request b/c response eats it
    return HttpResponseRedirect(reverse('tags'));
  return render_to_response('tags/tagref_detail.html',
      {'tag_name': tag_name, 'tagref': tagref },
      context_instance=RequestContext(request))


@login_required
def tagref_createform(request, tag_name=None):
  """ Form to create a single tag reference.
  """
  return render_to_response('tags/tagref_create.html',
      {'tag_name': tag_name, 
       'resources': library.list(),
       'res_default': 'NASB'
       }, context_instance=RequestContext(request))


@login_required
def tagref_create(request, tag_name):
  """ Create a single tag reference. 
  
  The resource must exist and the reference must be valid, but if the tag
  doesn't exist, then then it is created. 
  """
  try:
    # resource MUST exist
    res_str = request.POST['resource'].strip()
    resource = library.get(res_str)
    # reference must be valid
    ref_str = request.POST['reference']
    ref = resource.reference(ref_str)
  except:
    log.info("User provided bad resource or reference.")
    raise Http404
  # if tag name doesn't exist, create it
  try:
    t = get_exact_tag(request.user, tag_name)
  except:
    # TODO: move to models
    t = Tag(tag=tag_name, user=request.user)
    t.save()
  log.debug("Saving new tag %s %s %s %s", ref_str, tag_name, t, ref.pretty())
  # TODO: move to models
  new_ref = Reference(tag=t, resource=res_str, reference=ref.pretty(), 
      offset_start=ref.indices().start, offset_end=ref.indices().end, 
      user=request.user)
  new_ref.save()
  return HttpResponseRedirect(reverse('tagref_detail', args=(tag_name, str(new_ref.id))));


def tags_export(request):
  """ Export tags to a TSV.
  """
  response = HttpResponse(get_export_tsv(request.user), content_type="application/tsv")
  response['Content-Disposition'] = 'attachment; filename=export.tsv'
  return response


class ImportFileForm(forms.Form):
  """ Form for importint tags.
  """
  docfile = forms.FileField(label="Select a file to upload.")


@login_required
def tags_import(request):
  """ Import tags from an uploaded TSV.
  """
  if request.method == 'POST':
    form = ImportFileForm(request.POST, request.FILES)
    if form.is_valid():
      errors, successes = import_tsv_file(request.user, request.FILES['docfile'])
      # TODO: msg user # of errors and successes
      return HttpResponseRedirect(reverse('tags'))
  else:
    form = ImportFileForm()
  return render_to_response('tags/tags_import.html', {'form': form},
      context_instance=RequestContext(request))



