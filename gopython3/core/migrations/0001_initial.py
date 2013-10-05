# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Job'
        db.create_table('core_job', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('model_utils.fields.AutoCreatedField')(default=datetime.datetime.now)),
            ('modified', self.gf('model_utils.fields.AutoLastModifiedField')(default=datetime.datetime.now)),
            ('start', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('finish', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('requirements', self.gf('django.db.models.fields.TextField')()),
            ('status', self.gf('model_utils.fields.StatusField')(max_length=100, default='pending', no_check_for_status=True)),
        ))
        db.send_create_signal('core', ['Job'])

        # Adding model 'Package'
        db.create_table('core_package', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('model_utils.fields.AutoCreatedField')(default=datetime.datetime.now)),
            ('modified', self.gf('model_utils.fields.AutoLastModifiedField')(default=datetime.datetime.now)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100, unique=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50, unique=True)),
            ('repo_url', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
            ('repo_last_commit_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('issue_url', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
            ('issue_status', self.gf('django.db.models.fields.CharField')(max_length=20, default='unknown')),
            ('pr_url', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
            ('pr_status', self.gf('django.db.models.fields.CharField')(max_length=20, default='unknown')),
            ('fork_url', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
            ('ci_url', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
            ('ci_status', self.gf('django.db.models.fields.CharField')(max_length=20, default='unknown')),
            ('comment_count', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('comment_most_voted', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal('core', ['Package'])

        # Adding model 'Spec'
        db.create_table('core_spec', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('model_utils.fields.AutoCreatedField')(default=datetime.datetime.now)),
            ('modified', self.gf('model_utils.fields.AutoLastModifiedField')(default=datetime.datetime.now)),
            ('code', self.gf('django.db.models.fields.CharField')(max_length=100, unique=True)),
            ('status', self.gf('model_utils.fields.StatusField')(max_length=100, default='pending', no_check_for_status=True)),
            ('package', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Package'])),
            ('version', self.gf('django.db.models.fields.CharField')(max_length=20, blank=True)),
            ('release_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('python_versions', self.gf('jsonfield.fields.JSONField')(null=True, blank=True)),
            ('latest_version', self.gf('django.db.models.fields.CharField')(max_length=20, blank=True)),
            ('latest_release_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('latest_python_versions', self.gf('jsonfield.fields.JSONField')(null=True, blank=True)),
        ))
        db.send_create_signal('core', ['Spec'])

        # Adding unique constraint on 'Spec', fields ['package', 'version']
        db.create_unique('core_spec', ['package_id', 'version'])

        # Adding index on 'Spec', fields ['package', 'version']
        db.create_index('core_spec', ['package_id', 'version'])

        # Adding model 'JobSpec'
        db.create_table('core_jobspec', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('model_utils.fields.AutoCreatedField')(default=datetime.datetime.now)),
            ('modified', self.gf('model_utils.fields.AutoLastModifiedField')(default=datetime.datetime.now)),
            ('start', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('finish', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('job', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Job'])),
            ('spec', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Spec'], related_name='job_specs')),
            ('status', self.gf('model_utils.fields.StatusField')(max_length=100, default='pending', no_check_for_status=True)),
        ))
        db.send_create_signal('core', ['JobSpec'])


    def backwards(self, orm):
        # Removing index on 'Spec', fields ['package', 'version']
        db.delete_index('core_spec', ['package_id', 'version'])

        # Removing unique constraint on 'Spec', fields ['package', 'version']
        db.delete_unique('core_spec', ['package_id', 'version'])

        # Deleting model 'Job'
        db.delete_table('core_job')

        # Deleting model 'Package'
        db.delete_table('core_package')

        # Deleting model 'Spec'
        db.delete_table('core_spec')

        # Deleting model 'JobSpec'
        db.delete_table('core_jobspec')


    models = {
        'core.job': {
            'Meta': {'object_name': 'Job'},
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            'finish': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'job_specs': ('django.db.models.fields.related.ManyToManyField', [], {'through': "orm['core.JobSpec']", 'null': 'True', 'blank': 'True', 'symmetrical': 'False', 'to': "orm['core.Spec']"}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'requirements': ('django.db.models.fields.TextField', [], {}),
            'start': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'status': ('model_utils.fields.StatusField', [], {'max_length': '100', 'default': "'pending'", 'no_check_for_status': 'True'})
        },
        'core.jobspec': {
            'Meta': {'object_name': 'JobSpec'},
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            'finish': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'job': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Job']"}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'spec': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Spec']", 'related_name': "'job_specs'"}),
            'start': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'status': ('model_utils.fields.StatusField', [], {'max_length': '100', 'default': "'pending'", 'no_check_for_status': 'True'})
        },
        'core.package': {
            'Meta': {'object_name': 'Package'},
            'ci_status': ('django.db.models.fields.CharField', [], {'max_length': '20', 'default': "'unknown'"}),
            'ci_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'comment_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'comment_most_voted': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            'fork_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'issue_status': ('django.db.models.fields.CharField', [], {'max_length': '20', 'default': "'unknown'"}),
            'issue_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'unique': 'True'}),
            'pr_status': ('django.db.models.fields.CharField', [], {'max_length': '20', 'default': "'unknown'"}),
            'pr_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'repo_last_commit_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'repo_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'unique': 'True'})
        },
        'core.spec': {
            'Meta': {'index_together': "(('package', 'version'),)", 'object_name': 'Spec', 'unique_together': "(('package', 'version'),)"},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '100', 'unique': 'True'}),
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'latest_python_versions': ('jsonfield.fields.JSONField', [], {'null': 'True', 'blank': 'True'}),
            'latest_release_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'latest_version': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'package': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Package']"}),
            'python_versions': ('jsonfield.fields.JSONField', [], {'null': 'True', 'blank': 'True'}),
            'release_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'status': ('model_utils.fields.StatusField', [], {'max_length': '100', 'default': "'pending'", 'no_check_for_status': 'True'}),
            'version': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'})
        }
    }

    complete_apps = ['core']