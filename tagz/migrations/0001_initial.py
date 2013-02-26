# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Tag'
        db.create_table('tagz_tag', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('tag', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal('tagz', ['Tag'])

        # Adding model 'Reference'
        db.create_table('tagz_reference', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('tag', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tagz.Tag'])),
            ('book', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('chapter', self.gf('django.db.models.fields.IntegerField')()),
            ('firstLine', self.gf('django.db.models.fields.IntegerField')()),
            ('lastLine', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('tagz', ['Reference'])


    def backwards(self, orm):
        # Deleting model 'Tag'
        db.delete_table('tagz_tag')

        # Deleting model 'Reference'
        db.delete_table('tagz_reference')


    models = {
        'tagz.reference': {
            'Meta': {'ordering': "['book', 'chapter', 'firstLine', 'tag', 'lastLine']", 'object_name': 'Reference'},
            'book': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'chapter': ('django.db.models.fields.IntegerField', [], {}),
            'firstLine': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lastLine': ('django.db.models.fields.IntegerField', [], {}),
            'tag': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tagz.Tag']"})
        },
        'tagz.tag': {
            'Meta': {'ordering': "['tag']", 'object_name': 'Tag'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'tag': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['tagz']