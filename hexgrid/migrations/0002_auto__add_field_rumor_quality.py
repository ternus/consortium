# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Rumor.quality'
        db.add_column('hexgrid_rumor', 'quality',
                      self.gf('django.db.models.fields.IntegerField')(default=1),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Rumor.quality'
        db.delete_column('hexgrid_rumor', 'quality')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'gametex.gametexclass': {
            'Meta': {'object_name': 'GameTeXClass'},
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '256', 'primary_key': 'True'})
        },
        'gametex.gametexfield': {
            'Meta': {'object_name': 'GameTeXField'},
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '256', 'primary_key': 'True'})
        },
        'gametex.gametexfieldvalue': {
            'Meta': {'object_name': 'GameTeXFieldValue'},
            'field': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['gametex.GameTeXField']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['gametex.GameTeXObject']"}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '256', 'blank': 'True'})
        },
        'gametex.gametexobject': {
            'Meta': {'object_name': 'GameTeXObject'},
            'classes': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['gametex.GameTeXClass']", 'symmetrical': 'False'}),
            'custom_fields': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['gametex.GameTeXField']", 'through': "orm['gametex.GameTeXFieldValue']", 'symmetrical': 'False'}),
            'macro': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '256', 'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        },
        'gametex.gametexuser': {
            'Meta': {'object_name': 'GameTeXUser'},
            'gto': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['gametex.GameTeXObject']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'hexgrid.character': {
            'Meta': {'object_name': 'Character', '_ormbases': ['gametex.GameTeXUser']},
            'alive': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'gametexuser_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['gametex.GameTeXUser']", 'unique': 'True', 'primary_key': 'True'}),
            'has_disguise': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_disguised': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'nodes': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['hexgrid.Node']", 'through': "orm['hexgrid.CharNode']", 'symmetrical': 'False'}),
            'points': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'hexgrid.charnode': {
            'Meta': {'object_name': 'CharNode'},
            'character': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['hexgrid.Character']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'node': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['hexgrid.Node']"}),
            'unlocked_on': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'hexgrid.charnodewatch': {
            'Meta': {'object_name': 'CharNodeWatch'},
            'char': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['hexgrid.Character']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'node': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['hexgrid.Node']"}),
            'watched_on': ('django.db.models.fields.IntegerField', [], {})
        },
        'hexgrid.gameday': {
            'Meta': {'object_name': 'GameDay'},
            'day': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'tick_time': ('django.db.models.fields.TimeField', [], {})
        },
        'hexgrid.item': {
            'Meta': {'object_name': 'Item'},
            'base_name': ('django.db.models.fields.CharField', [], {'max_length': '256', 'blank': 'True'}),
            'base_price': ('django.db.models.fields.IntegerField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item_card': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['gametex.GameTeXObject']", 'null': 'True', 'blank': 'True'}),
            'post_buy': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'sold_by': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['hexgrid.Node']", 'null': 'True', 'blank': 'True'})
        },
        'hexgrid.itembid': {
            'Meta': {'object_name': 'ItemBid'},
            'character': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['hexgrid.Character']"}),
            'day': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['hexgrid.Item']"}),
            'resolved': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'won': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'hexgrid.node': {
            'Meta': {'object_name': 'Node'},
            'dead_until_day': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'expired': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'hex': ('django.db.models.fields.IntegerField', [], {'unique': 'True', 'primary_key': 'True'}),
            'long_desc': ('django.db.models.fields.TextField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'quick_desc': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'rumors_at_once': ('django.db.models.fields.IntegerField', [], {'default': '2'}),
            'rumors_per_day': ('django.db.models.fields.IntegerField', [], {'default': '2'}),
            'short_name': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'special': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'hexgrid.nodeevent': {
            'Meta': {'object_name': 'NodeEvent'},
            'day': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'what': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'when': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'where': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['hexgrid.Node']"}),
            'who': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['hexgrid.Character']"}),
            'who_disguised': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'hexgrid.rumor': {
            'Meta': {'object_name': 'Rumor'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'probability': ('django.db.models.fields.FloatField', [], {'default': '1.0'}),
            'quality': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'subject': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'text': ('django.db.models.fields.TextField', [], {}),
            'valid': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        },
        'hexgrid.secret': {
            'Meta': {'object_name': 'Secret'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'moneycost': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'node': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['hexgrid.Node']"}),
            'only_once': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'othercost': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'text': ('django.db.models.fields.TextField', [], {}),
            'valid': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        }
    }

    complete_apps = ['hexgrid']