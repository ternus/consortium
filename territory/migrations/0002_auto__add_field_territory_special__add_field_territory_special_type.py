# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Territory.special'
        db.add_column('territory_territory', 'special',
                      self.gf('django.db.models.fields.CharField')(max_length=256, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Territory.special_type'
        db.add_column('territory_territory', 'special_type',
                      self.gf('django.db.models.fields.CharField')(max_length=256, null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Territory.special'
        db.delete_column('territory_territory', 'special')

        # Deleting field 'Territory.special_type'
        db.delete_column('territory_territory', 'special_type')


    models = {
        'territory.action': {
            'Meta': {'object_name': 'Action'},
            'faction': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['territory.Faction']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'special': ('django.db.models.fields.CharField', [], {'max_length': '256', 'blank': 'True'}),
            'support_to': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'t_supp_to'", 'null': 'True', 'to': "orm['territory.Territory']"}),
            'support_type': ('django.db.models.fields.CharField', [], {'max_length': '256', 'blank': 'True'}),
            'target': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'t_move_to'", 'null': 'True', 'to': "orm['territory.Territory']"}),
            'territory': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'t_territory'", 'to': "orm['territory.Territory']"}),
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