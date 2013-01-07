# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'ConsortiumApp.saved_on'
        db.alter_column('app_consortiumapp', 'saved_on', self.gf('django.db.models.fields.DateTimeField')(null=True))

        # Changing field 'ConsortiumApp.apped_on'
        db.alter_column('app_consortiumapp', 'apped_on', self.gf('django.db.models.fields.DateTimeField')(null=True))

    def backwards(self, orm):

        # User chose to not deal with backwards NULL issues for 'ConsortiumApp.saved_on'
        raise RuntimeError("Cannot reverse this migration. 'ConsortiumApp.saved_on' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for 'ConsortiumApp.apped_on'
        raise RuntimeError("Cannot reverse this migration. 'ConsortiumApp.apped_on' and its values cannot be restored.")

    models = {
        'app.consortiumapp': {
            'Meta': {'object_name': 'ConsortiumApp'},
            'app_id': ('django.db.models.fields.CharField', [], {'max_length': '256', 'blank': 'True'}),
            'apped_on': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'campus': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'changing_minds': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'die_for': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'do_not_call': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '256'}),
            'genders': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'how_cast': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'motivations': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'new_player': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '256', 'blank': 'True'}),
            'public_secret': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'punts': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'saved_on': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'sms_ok': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'spy_plots': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'submitted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'teammate': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'time_constraints': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'typecast': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'wargame_ok': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'what_else': ('django.db.models.fields.TextField', [], {'blank': 'True'})
        }
    }

    complete_apps = ['app']