# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Package.slug'
        db.alter_column('core_package', 'slug', self.gf('autoslug.fields.AutoSlugField')(populate_from='name', unique_with=(), max_length=50, unique=True))
        # Deleting field 'Spec.latest_release_date'
        db.delete_column('core_spec', 'latest_release_date')

        # Deleting field 'Spec.latest_python_versions'
        db.delete_column('core_spec', 'latest_python_versions')

        # Deleting field 'Spec.latest_version'
        db.delete_column('core_spec', 'latest_version')

        # Adding field 'Spec.start'
        db.add_column('core_spec', 'start',
                      self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Spec.finish'
        db.add_column('core_spec', 'finish',
                      self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True),
                      keep_default=False)

        # Deleting field 'JobSpec.status'
        db.delete_column('core_jobspec', 'status')

        # Deleting field 'JobSpec.start'
        db.delete_column('core_jobspec', 'start')

        # Deleting field 'JobSpec.finish'
        db.delete_column('core_jobspec', 'finish')


    def backwards(self, orm):

        # Changing field 'Package.slug'
        db.alter_column('core_package', 'slug', self.gf('django.db.models.fields.SlugField')(max_length=50, unique=True))
        # Adding field 'Spec.latest_release_date'
        db.add_column('core_spec', 'latest_release_date',
                      self.gf('django.db.models.fields.DateTimeField')(blank=True, null=True),
                      keep_default=False)

        # Adding field 'Spec.latest_python_versions'
        db.add_column('core_spec', 'latest_python_versions',
                      self.gf('jsonfield.fields.JSONField')(blank=True, null=True),
                      keep_default=False)

        # Adding field 'Spec.latest_version'
        db.add_column('core_spec', 'latest_version',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=20, blank=True),
                      keep_default=False)

        # Deleting field 'Spec.start'
        db.delete_column('core_spec', 'start')

        # Deleting field 'Spec.finish'
        db.delete_column('core_spec', 'finish')

        # Adding field 'JobSpec.status'
        db.add_column('core_jobspec', 'status',
                      self.gf('model_utils.fields.StatusField')(default='pending', no_check_for_status=True, max_length=100),
                      keep_default=False)

        # Adding field 'JobSpec.start'
        db.add_column('core_jobspec', 'start',
                      self.gf('django.db.models.fields.DateTimeField')(blank=True, null=True),
                      keep_default=False)

        # Adding field 'JobSpec.finish'
        db.add_column('core_jobspec', 'finish',
                      self.gf('django.db.models.fields.DateTimeField')(blank=True, null=True),
                      keep_default=False)


    models = {
        'core.job': {
            'Meta': {'object_name': 'Job'},
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            'finish': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'requirements': ('django.db.models.fields.TextField', [], {}),
            'specs': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'null': 'True', 'through': "orm['core.JobSpec']", 'to': "orm['core.Spec']", 'blank': 'True'}),
            'start': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'status': ('model_utils.fields.StatusField', [], {'default': "'pending'", 'no_check_for_status': 'True', 'max_length': '100'})
        },
        'core.jobspec': {
            'Meta': {'object_name': 'JobSpec'},
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'job': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Job']"}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'spec': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'job_specs'", 'to': "orm['core.Spec']"})
        },
        'core.package': {
            'Meta': {'object_name': 'Package'},
            'ci_status': ('django.db.models.fields.CharField', [], {'default': "'unknown'", 'max_length': '20'}),
            'ci_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'comment_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'comment_most_voted': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            'fork_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'issue_status': ('django.db.models.fields.CharField', [], {'default': "'unknown'", 'max_length': '20'}),
            'issue_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'unique': 'True'}),
            'pr_status': ('django.db.models.fields.CharField', [], {'default': "'unknown'", 'max_length': '20'}),
            'pr_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'repo_last_commit_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'repo_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'slug': ('autoslug.fields.AutoSlugField', [], {'populate_from': "'name'", 'unique_with': '()', 'max_length': '50', 'unique': 'True'})
        },
        'core.spec': {
            'Meta': {'unique_together': "(('package', 'version'),)", 'object_name': 'Spec', 'index_together': "(('package', 'version'),)"},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '100', 'unique': 'True'}),
            'created': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            'finish': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'package': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Package']"}),
            'python_versions': ('jsonfield.fields.JSONField', [], {'null': 'True', 'blank': 'True'}),
            'release_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'start': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'status': ('model_utils.fields.StatusField', [], {'default': "'pending'", 'no_check_for_status': 'True', 'max_length': '100'}),
            'version': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'})
        }
    }

    complete_apps = ['core']