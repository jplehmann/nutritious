# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding index on 'Tag', fields ['tag']
        db.create_index('tagz_tag', ['tag'])

        # Adding unique constraint on 'Tag', fields ['tag']
        db.create_unique('tagz_tag', ['tag'])

        # Deleting field 'Reference.chapter'
        db.delete_column('tagz_reference', 'chapter')

        # Deleting field 'Reference.firstLine'
        db.delete_column('tagz_reference', 'firstLine')

        # Deleting field 'Reference.lastLine'
        db.delete_column('tagz_reference', 'lastLine')

        # Deleting field 'Reference.book'
        db.delete_column('tagz_reference', 'book')

        # Adding field 'Reference.resource'
        db.add_column('tagz_reference', 'resource',
                      self.gf('django.db.models.fields.CharField')(default=0, max_length=100),
                      keep_default=False)

        # Adding field 'Reference.reference'
        db.add_column('tagz_reference', 'reference',
                      self.gf('django.db.models.fields.CharField')(default=0, unique=True, max_length=100, db_index=True),
                      keep_default=False)

        # Adding field 'Reference.offset_start'
        db.add_column('tagz_reference', 'offset_start',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)

        # Adding field 'Reference.offset_end'
        db.add_column('tagz_reference', 'offset_end',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)


    def backwards(self, orm):
        # Removing unique constraint on 'Tag', fields ['tag']
        db.delete_unique('tagz_tag', ['tag'])

        # Removing index on 'Tag', fields ['tag']
        db.delete_index('tagz_tag', ['tag'])

        # Adding field 'Reference.chapter'
        db.add_column('tagz_reference', 'chapter',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)

        # Adding field 'Reference.firstLine'
        db.add_column('tagz_reference', 'firstLine',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)

        # Adding field 'Reference.lastLine'
        db.add_column('tagz_reference', 'lastLine',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)

        # Adding field 'Reference.book'
        db.add_column('tagz_reference', 'book',
                      self.gf('django.db.models.fields.CharField')(default=0, max_length=100),
                      keep_default=False)

        # Deleting field 'Reference.resource'
        db.delete_column('tagz_reference', 'resource')

        # Deleting field 'Reference.reference'
        db.delete_column('tagz_reference', 'reference')

        # Deleting field 'Reference.offset_start'
        db.delete_column('tagz_reference', 'offset_start')

        # Deleting field 'Reference.offset_end'
        db.delete_column('tagz_reference', 'offset_end')


    models = {
        'tagz.reference': {
            'Meta': {'ordering': "['offset_start', 'offset_end', 'resource', 'reference', 'tag']", 'object_name': 'Reference'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'offset_end': ('django.db.models.fields.IntegerField', [], {}),
            'offset_start': ('django.db.models.fields.IntegerField', [], {}),
            'reference': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100', 'db_index': 'True'}),
            'resource': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'tag': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tagz.Tag']"}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'})
        },
        'tagz.tag': {
            'Meta': {'ordering': "['tag']", 'object_name': 'Tag'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'tag': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100', 'db_index': 'True'})
        }
    }

    complete_apps = ['tagz']