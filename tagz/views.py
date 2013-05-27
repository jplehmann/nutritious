#from django.template import Context, loader
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.core.urlresolvers  import reverse
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.http import Http404
from django.utils.http import urlquote
#from django.core.exceptions import DoesNotExist
from django.template import RequestContext
from django import forms
from django.contrib.auth.decorators import login_required

from tagz.models import Tag
from tagz.models import Reference
from tagz.models import get_all_tags
from tagz.models import get_tags_for_ref
from tagz.models import get_exact_tag
from tagz.models import get_matching_tags
from tagz.models import get_refs_with_tag
from tagz.models import get_export_tsv
from tagz.models import import_tsv_file

from pybooks import library
import traceback


from django.contrib.auth import logout

def logout_view(request):
    logout(request)
    # Redirect to a success page.

library.load_resources()

def lib(request):
  """ Library root.
      Also receives searches performed when no resource is selected.
  """
  query = request.GET.get('q', None)
  # generic library response
  if not query:
    return render_to_response('tagz/library.html', 
        {'resources': library.list()}, 
        context_instance=RequestContext(request))
  else:
    return tag_search(request, query)


def lib_resource_search(request, resource, res_name, ref_obj, query, ref_str):
  """ Search a resource given a query.
  """
  # temporarily redirect tag search to root
  query = query.strip()
  if query.startswith("#"):
    return redirect(reverse('tags') + '?q=' + urlquote(query))
    #return tag_search(request, query)
  # first see if this is a reference in this resource
  try:
    new_ref = resource.reference(query)
    # we don't pass the request back because we don't want
    # it to find the search parameters
    return render_resource(request, res_name, new_ref.pretty())
  except Exception as e:
    print traceback.format_exc()
    print e
    pass
  hits = ref_obj.search(query)
  title = ("Search of '%s' for '%s' (%d hits)" % 
      (ref_obj.pretty(), query, len(hits)))
  # TODO keep this up to date with parameters in lib_resource
  # Let a test confirm this.
  res_path = reverse('resource', args=(res_name, None))
  return render_to_response('tagz/ref_search_results.html', 
      {'resource_name': res_name, 'title': title,
       'resource_path': res_path,
       'parent_ref': ref_obj.path(), 
       'children': hits,
       'text': None, 'sub_ref': ref_str if ref_str else "" },
      context_instance=RequestContext(request))


def nasb(request):
  """ Must redirect instead of simply serving the resource, otherwise
      relative links built up will be wrong.
  """
  return HttpResponseRedirect(reverse('resource', kwargs={'res_name':'NASB'}))
  

def get_resource(request, res_name, ref_str=None, highlights=None):
  """ Display a resource. If a reference is given within
  that resource, then it shows that particular scope.
  This handler is also used to front-end searches, which
  are redirected to another handler.
  @param Request may be None in the case where search is calling back
  to here, in order to display a reference.
  @param ref_str from the path, if given. The reference within the resource
  to be retrieved like 'John 5:1'
  @param highlights are reference strings which should be highlighted,
  which should be 'sub-references' to make sense.
  """
  try:
    resource = library.get(res_name)
    if ref_str:
      ref_obj = resource.reference(ref_str)
    else:
      ref_obj = resource.top_reference()
    # see if they want a search
    if request:
      query = request.GET.get('q', None)
      if query:
        return lib_resource_search(request, resource, res_name, ref_obj, query, ref_str)
    return render_resource(request, res_name, ref_str, highlights)
  except Exception as e:
    print "Exception: " + str(e)
    print traceback.format_exc()
    raise Http404


def render_resource(request, res_name, ref_str=None, highlights=None):
  """ Doesn't check for query parameters.
  """
  try:
    resource = library.get(res_name)
    if ref_str:
      ref_obj = resource.reference(ref_str)
    else:
      ref_obj = resource.top_reference()
    # inspect if the referene has children
    # should return None if it doesn't have them. 
    children = ref_obj.children()
    # inspect if the children have text
    # show child text IF the children don't have children
    show_child_text = (not children[0].children() if children else False)
    # get text if possible
    try:
      text = ref_obj.text()
    except:
      text = None
    # requesting context is legal if there are no children, AND, it
    # is a text-bearing reference
    if text and not children:
      context_size = safe_int(request.GET.get('ctx', 0)) if request else None
      # get the amount of context needed
      if context_size and context_size > 0:
        # get reference 
        try:
          context = ref_obj.context(context_size)
          # set the highlight on our center line
          return render_resource(
              request, res_name, context.pretty(), [ref_obj.pretty()])
        except Exception as e:
          print e
    # navigation references
    parent_ref, previous_ref, next_ref = None, None, None
    res_path = (reverse('resource', kwargs={'res_name':res_name}))
    if ref_obj:
      def rel_url(rel_fct):
        # TODO: could make this into a reverse() 
        return res_path + rel_fct().path() if rel_fct() else None
      parent_ref = rel_url(ref_obj.parent)
      previous_ref = rel_url(ref_obj.previous)
      next_ref = rel_url(ref_obj.next)
    context = {
         'resource_name': res_name, 'title': ref_obj.pretty(), 
         'resource_path': res_path,
         'parent_ref': parent_ref, 
         'previous_ref': previous_ref, 'next_ref': next_ref,
         'children': children,
         'highlights': highlights,
         'text': text, 'sub_ref': ref_str if ref_str else ""
    }
    # determine which view to use
    if children:
      if show_child_text:
        return render_to_response('tagz/ref_text_list.html', context,
            context_instance=RequestContext(request))
      else:
        return render_to_response('tagz/ref_index.html', context,
            context_instance=RequestContext(request))
    else:
      return render_to_response('tagz/ref_detail.html', context,
          context_instance=RequestContext(request))
  except Exception as e:
    print "Exception: " + str(e)
    print traceback.format_exc()
    raise Http404


def tag_search(request, query):
  # tag search: currently only supports a single tag, and must begin with #
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
  raise Http404 # ("Root search must contain only an #tag.")


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
  return render_to_response('tagz/tag_index.html', 
      {'counted_tags': counted_tags},
      context_instance=RequestContext(request))


def tag(request, tag_name):
  """ Single tag: show all references, and other tags on those refs."""
  if request.method == 'DELETE':
    return tag_delete(request, tag_name)
  elif request.method == 'PUT':
    return tag_update(request, tag_name)
  t = get_object_or_404(Tag, tag=tag_name)
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
      print "Exception for " + ref.pretty_ref() + " = " + traceback.format_exc()
      text, clean_ref = ('unknown', ref.pretty_ref())
    clean_refs.append(clean_ref)
    texts.append(text)
    ref_paths.append(reverse('resource', args=(resource, ref.pretty_ref())))
  related_refs_n_tags = zip(ids, clean_refs, ref_paths, related_tags, texts)
  return render_to_response('tagz/tag_detail.html', 
      {'tag': t, 'related_refs_n_tags': related_refs_n_tags},
      context_instance=RequestContext(request))


@login_required
def tag_delete(request, tag_name):
  """ Delete a tag and all associated tagrefs.
  """
  t = get_object_or_404(Tag, tag=tag_name)
  # clean up all associated references, since references only have 1 tag in them
  # but this seems to not be necessary, maybe Django is cleaning up
  # for me?
  for ref in get_refs_with_tag(request.user, t):
    ref.delete()
  t.delete()
  # FIXME: not doing anything when called from AJAX request b/c response eats it
  return HttpResponseRedirect(reverse('tags'));


@login_required
def tag_update(request, tag_name):
  """ Rename a tag. If the tag name is exists already, it will merge them.
  """
  t_old = get_object_or_404(Tag, tag=tag_name)
  try:
    new_name = request.GET.get('name', None)
  except:
    print traceback.format_exc()
    print "problem getting new name"
  print "old name, new: " + tag_name + " " + new_name
  try:
    t_new = get_exact_tag(request.user, new_name)
    print t_new
    for r in get_refs_with_tag(request.user, t_old):
      r.tag = t_new
      print "updating ref: " + str(r)
      r.save()
    t_old.delete()
  except:
    print traceback.format_exc()
    print "renaming tag"
    t_old.tag = new_name
    t_old.save()
  return HttpResponseRedirect(reverse('tag', args=new_name));


def tagref_detail(request, tag_name, id):
  tagref = get_object_or_404(Reference, id=id)
  # make sure the tag with this id belongs under this path
  if (tag_name != tagref.tag.tag):
    print "Mismatched tag name path with id '%s' '%s'" %( tag_name, tagref.tag.tag)
    raise Http404
  if request.method == 'DELETE':
    tagref.delete()
    # TODO: if this is the last ref for this tag, delete the tag?
    # not doing anything when called from AJAX request b/c response eats it
    return HttpResponseRedirect(reverse('tags'));
  return render_to_response('tagz/tagref_detail.html',
      {'tag_name': tag_name, 'tagref': tagref },
      context_instance=RequestContext(request))

@login_required
def tagref_createform(request, tag_name=None):
  """ Form to create a single tag reference """
  return render_to_response('tagz/tagref_create.html',   
      {'tag_name': tag_name, 
       'resources': library.list(),
       'res_default': 'NASB'
       }, context_instance=RequestContext(request))

@login_required
def tagref_create(request, tag_name):
  """ Create a single tag reference. The resource must exist and 
      the reference must be valid, but if the tag doesn't exist, 
      then then it is created. 
  """
  print "Tagref create"
  try:
    # resource MUST exist
    res_str = request.POST['resource'].strip()
    resource = library.get(res_str)
    # reference must be valid
    ref_str = request.POST['reference']
    ref = resource.reference(ref_str)
  except:
    print "User provided bad resource or reference."
    print traceback.format_exc()
    raise Http404
  # if tag name doesn't exist, create it
  try:
    t = get_exact_tag(request.user, tag_name)
  except:
    # TODO: move to models
    t = Tag(tag=tag_name, user=request.user)
    t.save()
  print "Saving be saving", ref_str, tag_name, t, ref.pretty()
  # TODO: move to models
  new_ref = Reference(tag=t, resource=res_str, reference=ref.pretty(), 
      offset_start=ref.indices().start, offset_end=ref.indices().end, 
      user=request.user)
  new_ref.save()
  return HttpResponseRedirect(reverse('tagref_detail', args=(tag_name, str(new_ref.id))));


def tags_export(request):
  response = HttpResponse(get_export_tsv(request.user), content_type="application/tsv")
  response['Content-Disposition'] = 'attachment; filename=export.tsv'
  return response


class ImportFileForm(forms.Form):
    docfile = forms.FileField(label="Select a file to upload.")


@login_required
def tags_import(request):
  if request.method == 'POST':
    form = ImportFileForm(request.POST, request.FILES)
    if form.is_valid():
      errors, successes = import_tsv_file(request.user, request.FILES['docfile'])
      # TODO: msg user # of errors and successes
      return HttpResponseRedirect(reverse('tags'))
  else:
    form = ImportFileForm()
  return render_to_response('tagz/tags_import.html', {'form': form},
      context_instance=RequestContext(request))


def safe_int(val):
  return int(val) if val != None else val


