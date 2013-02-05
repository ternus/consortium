# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Territory'
        db.create_table('territory_territory', (
            ('code', self.gf('django.db.models.fields.CharField')(unique=True, max_length=256, primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('pts_s', self.gf('django.db.models.fields.CharField')(max_length=512, blank=True)),
            ('center_s', self.gf('django.db.models.fields.CharField')(max_length=256, blank=True)),
            ('owner', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['territory.Faction'], null=True, blank=True)),
        ))
        db.send_create_signal('territory', ['Territory'])

        # Adding M2M table for field connects on 'Territory'
        db.create_table('territory_territory_connects', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('from_territory', models.ForeignKey(orm['territory.territory'], null=False)),
            ('to_territory', models.ForeignKey(orm['territory.territory'], null=False))
        ))
        db.create_unique('territory_territory_connects', ['from_territory_id', 'to_territory_id'])

        # Adding model 'Faction'
        db.create_table('territory_faction', (
            ('code', self.gf('django.db.models.fields.CharField')(unique=True, max_length=256, primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('color', self.gf('django.db.models.fields.CharField')(default='', max_length=256)),
        ))
        db.send_create_signal('territory', ['Faction'])

        # Adding model 'Unit'
        db.create_table('territory_unit', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('faction', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['territory.Faction'])),
            ('territory', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['territory.Territory'])),
            ('alive', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('special', self.gf('django.db.models.fields.CharField')(default='', max_length=256, blank=True)),
        ))
        db.send_create_signal('territory', ['Unit'])

        # Adding model 'Action'
        db.create_table('territory_action', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('faction', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['territory.Faction'])),
            ('turn', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('territory', self.gf('django.db.models.fields.related.ForeignKey')(related_name='t_territory', to=orm['territory.Territory'])),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('target', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='t_move_to', null=True, to=orm['territory.Territory'])),
            ('special', self.gf('django.db.models.fields.CharField')(max_length=256, blank=True)),
            ('support_type', self.gf('django.db.models.fields.CharField')(max_length=256, blank=True)),
            ('support_to', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='t_supp_to', null=True, to=orm['territory.Territory'])),
            ('validation_level', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal('territory', ['Action'])

        # Adding model 'GameBoard'
        db.create_table('territory_gameboard', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('turn', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal('territory', ['GameBoard'])


    def backwards(self, orm):
        # Deleting model 'Territory'
        db.delete_table('territory_territory')

        # Removing M2M table for field connects on 'Territory'
        db.delete_table('territory_territory_connects')

        # Deleting model 'Faction'
        db.delete_table('territory_faction')

        # Deleting model 'Unit'
        db.delete_table('territory_unit')

        # Deleting model 'Action'
        db.delete_table('territory_action')

        # Deleting model 'GameBoard'
        db.delete_table('territory_gameboard')


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
            'pts_s': ('django.db.models.fields.CharField', [], {'max_length': '512', 'blank': 'True'})
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