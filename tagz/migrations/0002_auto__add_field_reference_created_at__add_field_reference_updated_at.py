# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Reference.created_at'
        db.add_column('tagz_reference', 'created_at',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Reference.updated_at'
        db.add_column('tagz_reference', 'updated_at',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Reference.created_at'
        db.delete_column('tagz_reference', 'created_at')

        # Deleting field 'Reference.updated_at'
        db.delete_column('tagz_reference', 'updated_at')


    models = {
        'tagz.reference': {
            'Meta': {'ordering': "['book', 'chapter', 'firstLine', 'tag', 'lastLine']", 'object_name': 'Reference'},
            'book': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'chapter': ('django.db.models.fields.IntegerField', [], {}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'firstLine': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lastLine': ('django.db.models.fields.IntegerField', [], {}),
            'tag': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tagz.Tag']"}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'})
        },
        'tagz.tag': {
            'Meta': {'ordering': "['tag']", 'object_name': 'Tag'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'tag': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['tagz']