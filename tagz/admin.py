from tagz.models import Tag
from tagz.models import Reference
from django.contrib import admin
#from django.db import models
#from django.forms import TextInput

class RegisterAdmin(admin.ModelAdmin):
  readonly_fields = ("created_at","updated_at",)
  list_display = ("book", "chapter", "firstLine", "lastLine", "tag",)
  list_filter = ('book',)
  search_fields = ['book', 'tag__tag']
  #formfield_overrides = {
  #  models.CharField: {'widget': TextInput(attrs={'size':'50'})},
  #  #models.TextField: {'widget': Textarea(attrs={'rows':4, 'cols':40})},
  #}

class TagAdmin(admin.ModelAdmin):
  search_fields = ['tag',]
  list_display = ("tag",)

admin.site.register(Tag, TagAdmin)
admin.site.register(Reference, RegisterAdmin)

