from tagz.models import Tag
from tagz.models import Reference
from django.contrib import admin
#from django.db import models
#from django.forms import TextInput

class RegisterAdmin(admin.ModelAdmin):
  readonly_fields = ("created_at","updated_at",)
  list_display = ("reference", "resource", "offset_start", "offset_end", "tag",)
  list_filter = ('reference',)
  search_fields = ['reference', 'tag__tag']
  #formfield_overrides = {
  #  models.CharField: {'widget': TextInput(attrs={'size':'50'})},
  #  #models.TextField: {'widget': Textarea(attrs={'rows':4, 'cols':40})},
  #}

class TagAdmin(admin.ModelAdmin):
  search_fields = ['tag',]
  list_display = ("tag",)

admin.site.register(Tag, TagAdmin)
admin.site.register(Reference, RegisterAdmin)

