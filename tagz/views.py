#from django.template import Context, loader
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse
from django.http import Http404

from tagz.models import Tag
from tagz.models import Reference
from tagz.models import get_refs_with_tag
from tagz.models import get_tags_for_ref

from pybible import api
from pybooks import library


import pybooks.library
library.load_resources()
def lib(request):
  """ Library root.
  """
  return render_to_response('tagz/tag_library.html', 
      {'resources': library.list()})


import traceback


def lib_resource_search(resource, res_name, ref_obj, query, ref_str):
  """ Search a resource given a query.
  """
  # first see if this is a reference in this resource
  try:
    new_ref = resource.reference(query)
    return lib_resource(None, res_name, new_ref.pretty())
  except Exception as e:
    print e
  hits = ref_obj.search(query)
  title = ("Search of '%s' for '%s' (%d hits)" % 
      (ref_obj.pretty(), query, len(hits)))
  # TODO keep this up to date with parameters in lib_resource
  # Let a test confirm this.
  res_path = "/tagz/lib/" + res_name
  return render_to_response('tagz/tag_library_resource.html', 
      {'resource_name': res_name, 'title': title,
       'resource_path': res_path,
       'parent_ref': ref_obj.pretty(), 
       'show_child_text': True, 'children': hits,
       'text': None, 'sub_ref': ref_str if ref_str else ""})


def lib_resource(request, res_name, ref_str=None, highlights=None):
  """ Display a resource. If a reference is given within
  that resource, then it shows that particular scope.
  This handler is also used to front-end searches, which
  are redirected to another handler.
  @param Request may be None in the case where search is calling back
  to here, in order to display a reference.
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
        return lib_resource_search(resource, res_name, ref_obj, query, ref_str)
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
      context_size = safe_int(request.GET.get('ctx', 0))
      # get the amount of context needed
      if context_size and context_size > 0:
        # get reference 
        try:
          context = ref_obj.context(context_size)
          # TODO set the highlight on our center line
          return lib_resource(None, res_name, context.pretty(), [ref_obj.pretty()])
        except Exception as e:
          print e
    # navigation references
    parent_ref, previous_ref, next_ref = None, None, None
    res_path = "/tagz/lib/" + res_name
    if ref_obj:
      def rel_url(rel_fct):
        return res_path + '/' + rel_fct().pretty() if rel_fct() else None
      parent_ref = rel_url(ref_obj.parent)
      previous_ref = rel_url(ref_obj.previous)
      next_ref = rel_url(ref_obj.next)
    return render_to_response('tagz/tag_library_resource.html', 
        {'resource_name': res_name, 'title': ref_obj.pretty(), 
         'resource_path': res_path,
         'parent_ref': parent_ref, 
         'previous_ref': previous_ref, 'next_ref': next_ref,
         'show_child_text': show_child_text, 'children': children,
         'highlights': highlights,
         'text': text, 'sub_ref': ref_str if ref_str else ""})
  except Exception as e:
    print "Exception: " + str(e)
    print traceback.format_exc()
    raise Http404


def tags(request):
  """ All tags: for each show all refs. 
  """
  all_tags = Tag.objects.all()
  counts = []
  for t in all_tags:
    refs = get_refs_with_tag(t)
    counts.append(refs.count())
  counted_tags = zip(all_tags, counts)
  return render_to_response('tagz/tag_index.html', 
      {'counted_tags': counted_tags})


def tag(request, tag_name):
  """ Single tag: for each show other tags on that ref."""
  t = get_object_or_404(Tag, tag=tag_name)
  related_refs = get_refs_with_tag(t)
  related_tags = []
  texts = []
  for ref in related_refs: 
    related_tags.append(get_tags_for_ref(ref))
    text, cleanRef = api.getTextAndCleanReference(ref.pretty_ref())
    texts.append(text)
  related_refs_n_tags = zip(related_refs, related_tags, texts)
  return render_to_response('tagz/tag_detail.html', 
      {'tag': t, 'related_refs_n_tags': related_refs_n_tags})


def ref(request, ref_name):
  """ Single ref: show scripture and tags."""
  #ref = get_object_or_404(Reference, ref=ref_name)
  # 1. parse this ref 
  text, clean_ref = api.getTextAndCleanReference(ref_name)
  # 2. create a new reference object
  # 3. look up all tags that overlap
  #get_tags_for_ref(ref)
  tags = []
  return render_to_response('tagz/ref_detail.html', 
      {'ref_name': clean_ref, 'text': text, 'tags': tags})


def refs(request):
  """ All refs: simply show count."""
  refs = Reference.objects.all()
  return HttpResponse("Number of references found: %s" % refs.count())


def safe_int(val):
  return int(val) if val != None else val


