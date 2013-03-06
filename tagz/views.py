#from django.template import Context, loader
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse
#from django.http import Http404

from tagz.models import Tag
from tagz.models import Reference
from tagz.models import get_refs_with_tag
from tagz.models import get_tags_for_ref

from pybible import api


def tags(request):
  """ All tags: for each show all refs. """
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
