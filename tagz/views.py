#from django.template import Context, loader
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.http import Http404

from tagz.models import Tag, Reference


def tags(request):
  """ All tags. For each show all refs. """
  all_tags = Tag.objects.all()
  return render_to_response('tagz/tag_index.html', {'all_tags': all_tags})


def tag(request, tag_name):
  """ Single tag. For each show other tags on that ref."""
  try:
    t = Tag.objects.get(tag=tag_name)
  except Tag.DoesNotExist:
    raise Http404
  return render_to_response('tagz/tag_detail.html', {'tag': t})


def refs(request):
  """ All refs. """
  refs = Reference.objects.all()
  return HttpResponse("Number of references found: %s" % refs.count())
