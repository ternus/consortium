# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Node'
        db.create_table('hexgrid_node', (
            ('name', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('short_name', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('hex', self.gf('django.db.models.fields.IntegerField')(unique=True, primary_key=True)),
            ('quick_desc', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('long_desc', self.gf('django.db.models.fields.TextField')()),
            ('dead_until_day', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('rumors_at_once', self.gf('django.db.models.fields.IntegerField')(default=2)),
            ('rumors_per_day', self.gf('django.db.models.fields.IntegerField')(default=2)),
            ('special', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('expired', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('hexgrid', ['Node'])

        # Adding model 'Secret'
        db.create_table('hexgrid_secret', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('node', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['hexgrid.Node'])),
            ('password', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('moneycost', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('othercost', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('text', self.gf('django.db.models.fields.TextField')()),
            ('valid', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('only_once', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('hexgrid', ['Secret'])

        # Adding model 'Rumor'
        db.create_table('hexgrid_rumor', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('subject', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('text', self.gf('django.db.models.fields.TextField')()),
            ('true', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('valid', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal('hexgrid', ['Rumor'])

        # Adding model 'ItemBid'
        db.create_table('hexgrid_itembid', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('character', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['hexgrid.Character'])),
            ('item', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['hexgrid.Item'])),
            ('node', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['hexgrid.Node'])),
            ('amount', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('day', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('disguised', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('resolved', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('won', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('hexgrid', ['ItemBid'])

        # Adding model 'NodeEvent'
        db.create_table('hexgrid_nodeevent', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('where', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['hexgrid.Node'])),
            ('when', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('who', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['hexgrid.Character'])),
            ('who_disguised', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('day', self.gf('django.db.models.fields.IntegerField')()),
            ('item', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['hexgrid.Item'], null=True, blank=True)),
        ))
        db.send_create_signal('hexgrid', ['NodeEvent'])

        # Adding model 'Item'
        db.create_table('hexgrid_item', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('base_price', self.gf('django.db.models.fields.IntegerField')(default=None, null=True, blank=True)),
            ('base_name', self.gf('django.db.models.fields.CharField')(max_length=256, blank=True)),
            ('post_buy', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('rarity_class', self.gf('django.db.models.fields.CharField')(default='Common', max_length=10)),
            ('rarity_prob', self.gf('django.db.models.fields.FloatField')(default=0.0)),
            ('item_card', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['gametex.GameTeXObject'], null=True, blank=True)),
            ('valid', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal('hexgrid', ['Item'])

        # Adding M2M table for field sold_by on 'Item'
        db.create_table('hexgrid_item_sold_by', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('item', models.ForeignKey(orm['hexgrid.item'], null=False)),
            ('node', models.ForeignKey(orm['hexgrid.node'], null=False))
        ))
        db.create_unique('hexgrid_item_sold_by', ['item_id', 'node_id'])

        # Adding model 'CharNode'
        db.create_table('hexgrid_charnode', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('character', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['hexgrid.Character'])),
            ('node', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['hexgrid.Node'])),
            ('unlocked_on', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal('hexgrid', ['CharNode'])

        # Adding model 'CharNodeWatch'
        db.create_table('hexgrid_charnodewatch', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('char', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['hexgrid.Character'])),
            ('node', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['hexgrid.Node'])),
            ('watched_on', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('hexgrid', ['CharNodeWatch'])

        # Adding model 'Character'
        db.create_table('hexgrid_character', (
            ('gametexuser_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['gametex.GameTeXUser'], unique=True, primary_key=True)),
            ('phone', self.gf('django.db.models.fields.CharField')(default='', max_length=15, blank=True)),
            ('urgent_sms', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('routine_sms', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('points', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('is_disguised', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('has_disguise', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('alive', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal('hexgrid', ['Character'])

        # Adding model 'GameDay'
        db.create_table('hexgrid_gameday', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('day', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('tick_time', self.gf('django.db.models.fields.TimeField')()),
        ))
        db.send_create_signal('hexgrid', ['GameDay'])


    def backwards(self, orm):
        # Deleting model 'Node'
        db.delete_table('hexgrid_node')

        # Deleting model 'Secret'
        db.delete_table('hexgrid_secret')

        # Deleting model 'Rumor'
        db.delete_table('hexgrid_rumor')

        # Deleting model 'ItemBid'
        db.delete_table('hexgrid_itembid')

        # Deleting model 'NodeEvent'
        db.delete_table('hexgrid_nodeevent')

        # Deleting model 'Item'
        db.delete_table('hexgrid_item')

        # Removing M2M table for field sold_by on 'Item'
        db.delete_table('hexgrid_item_sold_by')

        # Deleting model 'CharNode'
        db.delete_table('hexgrid_charnode')

        # Deleting model 'CharNodeWatch'
        db.delete_table('hexgrid_charnodewatch')

        # Deleting model 'Character'
        db.delete_table('hexgrid_character')

        # Deleting model 'GameDay'
        db.delete_table('hexgrid_gameday')


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
            'phone': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '15', 'blank': 'True'}),
            'points': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'routine_sms': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'urgent_sms': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
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
            'rarity_class': ('django.db.models.fields.CharField', [], {'default': "'Common'", 'max_length': '10'}),
            'rarity_prob': ('django.db.models.fields.FloatField', [], {'default': '0.0'}),
            'sold_by': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['hexgrid.Node']", 'null': 'True', 'blank': 'True'}),
            'valid': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        },
        'hexgrid.itembid': {
            'Meta': {'object_name': 'ItemBid'},
            'amount': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'character': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['hexgrid.Character']"}),
            'day': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'disguised': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['hexgrid.Item']"}),
            'node': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['hexgrid.Node']"}),
            'resolved': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'won': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'hexgrid.node': {
            'Meta': {'ordering': "['hex']", 'object_name': 'Node'},
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
            'item': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['hexgrid.Item']", 'null': 'True', 'blank': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'when': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'where': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['hexgrid.Node']"}),
            'who': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['hexgrid.Character']"}),
            'who_disguised': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'hexgrid.rumor': {
            'Meta': {'object_name': 'Rumor'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'subject': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'text': ('django.db.models.fields.TextField', [], {}),
            'true': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
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