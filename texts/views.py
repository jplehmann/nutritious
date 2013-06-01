import traceback

from django.shortcuts import render_to_response
from django.shortcuts import redirect
from django.core.urlresolvers  import reverse
from django.http import HttpResponseRedirect
from django.http import Http404
from django.template import RequestContext
from django.utils.http import urlquote

from pybooks import library

from tags.views import tag_search


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


def safe_int(val):
  return int(val) if val != None else val

