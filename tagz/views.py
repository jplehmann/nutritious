#from django.template import Context, loader
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse
#from django.http import Http404

from tagz.models import Tag, Reference, get_refs_with_tag


def tags(request):
  """ All tags. For each show all refs. """
  all_tags = Tag.objects.all()
  counts = []
  for t in all_tags:
    refs = get_refs_with_tag(t)
    counts.append(refs.count())
  counted_tags = zip(all_tags, counts)
  return render_to_response('tagz/tag_index.html', 
      {'counted_tags': counted_tags, 'count': len(counted_tags) })


def tag(request, tag_name):
  """ Single tag. For each show other tags on that ref."""
  t = get_object_or_404(Tag, tag=tag_name)
  related_refs = get_refs_with_tag(t)
  return render_to_response('tagz/tag_detail.html', 
      {'tag': t, 'related_refs': related_refs})


def refs(request):
  """ All refs. """
  refs = Reference.objects.all()
  return HttpResponse("Number of references found: %s" % refs.count())
