from django.template import Context, loader
from django.http import HttpResponse
from tagz.models import Tag, Reference


def tags(request):
  """ All tags. For each show all refs. """
  all_tags = Tag.objects.all()
  t = loader.get_template('tagz/tag_index.html')
  c = Context({
    'all_tags': all_tags,
  })
  return HttpResponse(t.render(c))


def tag(request, tag_name):
  """ Single tag. For each show other tags on that ref."""
  return HttpResponse("Hello, world. You're at the tags index., tagname="+ tag_name)


def refs(request):
  """ All refs. """
  refs = Reference.objects.all()
  return HttpResponse("Number of references found: %s" % refs.count())
