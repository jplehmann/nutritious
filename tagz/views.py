from django.http import HttpResponse
import tagz.Tag
import tagz.Reference


def tags(request):
  """ All tags. For each show all refs. """
  return HttpResponse("Hello, world. You're at the tags index.")


def tag(request, tag_name):
  """ Single tag. For each show other tags on that ref."""
  return HttpResponse("Hello, world. You're at the tags index., tagname="+ tag_name)


def refs(request):
  """ All refs. """
  return HttpResponse("Hello, world. You're at the tags index.")
