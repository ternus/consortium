# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'ConsortiumApp'
        db.create_table('app_consortiumapp', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=256)),
            ('phone', self.gf('django.db.models.fields.CharField')(max_length=256, blank=True)),
            ('do_not_call', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('time_constraints', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('new_player', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('genders', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('sms_ok', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('wargame_ok', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('typecast', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('punts', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('how_cast', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('spy_plots', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('public_secret', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('motivations', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('die_for', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('teammate', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('campus', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('changing_minds', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('what_else', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('saved_on', self.gf('django.db.models.fields.DateTimeField')(blank=True)),
            ('apped_on', self.gf('django.db.models.fields.DateTimeField')(blank=True)),
            ('submitted', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('app_id', self.gf('django.db.models.fields.CharField')(max_length=256, blank=True)),
        ))
        db.send_create_signal('app', ['ConsortiumApp'])


    def backwards(self, orm):
        # Deleting model 'ConsortiumApp'
        db.delete_table('app_consortiumapp')


    models = {
        'app.consortiumapp': {
            'Meta': {'object_name': 'ConsortiumApp'},
            'app_id': ('django.db.models.fields.CharField', [], {'max_length': '256', 'blank': 'True'}),
            'apped_on': ('django.db.models.fields.DateTimeField', [], {'blank': 'True'}),
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
            'saved_on': ('django.db.models.fields.DateTimeField', [], {'blank': 'True'}),
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