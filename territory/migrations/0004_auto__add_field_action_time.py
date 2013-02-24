# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Action.time'
        db.add_column('territory_action', 'time',
                      self.gf('django.db.models.fields.DateTimeField')(default=None, null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Action.time'
        db.delete_column('territory_action', 'time')


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
        'hexgrid.charnode': {
            'Meta': {'object_name': 'CharNode'},
            'character': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['hexgrid.Character']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'node': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['hexgrid.Node']"}),
            'unlocked_on': ('django.db.models.fields.IntegerField', [], {})
        },
        'hexgrid.hgcharacter': {
            'Meta': {'object_name': 'Character', '_ormbases': ['gametex.GameTeXUser']},
            'gametexuser_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['gametex.GameTeXUser']", 'unique': 'True', 'primary_key': 'True'}),
            'has_disguise': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_disguised': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'nodes': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['hexgrid.Node']", 'through': "orm['hexgrid.CharNode']", 'symmetrical': 'False'}),
            'points': ('django.db.models.fields.IntegerField', [], {'default': '0'})
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
        'territory.action': {
            'Meta': {'object_name': 'Action'},
            'faction': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['territory.Faction']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'issuer': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': "orm['hexgrid.Character']", 'null': 'True', 'blank': 'True'}),
            'special': ('django.db.models.fields.CharField', [], {'max_length': '256', 'blank': 'True'}),
            'support_to': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'t_supp_to'", 'null': 'True', 'to': "orm['territory.Territory']"}),
            'support_type': ('django.db.models.fields.CharField', [], {'max_length': '256', 'blank': 'True'}),
            'target': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'t_move_to'", 'null': 'True', 'to': "orm['territory.Territory']"}),
            'territory': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'t_territory'", 'to': "orm['territory.Territory']"}),
            'time': ('django.db.models.fields.DateTimeField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'turn': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'validation_level': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'territory.faction': {
            'Meta': {'object_name': 'Faction'},
            'code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '256', 'primary_key': 'True'}),
            'color': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '256'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        },
        'territory.gameboard': {
            'Meta': {'object_name': 'GameBoard'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'turn': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'territory.territory': {
            'Meta': {'object_name': 'Territory'},
            'center_s': ('django.db.models.fields.CharField', [], {'max_length': '256', 'blank': 'True'}),
            'code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '256', 'primary_key': 'True'}),
            'connects': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'connects_rel_+'", 'to': "orm['territory.Territory']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['territory.Faction']", 'null': 'True', 'blank': 'True'}),
            'pts_s': ('django.db.models.fields.CharField', [], {'max_length': '512', 'blank': 'True'}),
            'special': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'special_type': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'})
        },
        'territory.unit': {
            'Meta': {'object_name': 'Unit'},
            'alive': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'faction': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['territory.Faction']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'special': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '256', 'blank': 'True'}),
            'territory': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['territory.Territory']"})
        }
    }

    complete_apps = ['territory']