# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'JobSpec'
        db.delete_table('core_jobspec')

        # Deleting field 'Spec.latest_python_versions'
        db.delete_column('core_spec', 'latest_python_versions')

        # Renaming field 'Spec.modified'
        db.rename_column('core_spec', 'modified', 'updated_at')

        # Deleting field 'Spec.latest_release_date'
        db.delete_column('core_spec', 'latest_release_date')

        # Deleting field 'Spec.latest_version'
        db.delete_column('core_spec', 'latest_version')

        # Renaming field 'Spec.created'
        db.rename_column('core_spec', 'created', 'created_at')

        # Adding field 'Spec.started_at'
        db.add_column('core_spec', 'started_at',
                      self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Spec.finished_at'
        db.add_column('core_spec', 'finished_at',
                      self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True),
                      keep_default=False)

        # Renaming field 'Job.modified'
        db.rename_column('core_job', 'modified', 'updated_at')

        # Renaming field 'Job.start'
        db.rename_column('core_job', 'start', 'started_at')

        # Renaming field 'Job.finish'
        db.rename_column('core_job', 'finish', 'finished_at')

        # Renaming field 'Job.created'
        db.rename_column('core_job', 'created', 'created_at')

        # Adding M2M table for field specs on 'Job'
        m2m_table_name = db.shorten_name('core_job_specs')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('job', models.ForeignKey(orm['core.job'], null=False)),
            ('spec', models.ForeignKey(orm['core.spec'], null=False))
        ))
        db.create_unique(m2m_table_name, ['job_id', 'spec_id'])

        # Renaming field 'Package.created'
        db.rename_column('core_package', 'created', 'created_at')

        # Renaming field 'Package.modified'
        db.rename_column('core_package', 'modified', 'updated_at')

        # Changing field 'Package.slug'
        db.alter_column('core_package', 'slug', self.gf('autoslug.fields.AutoSlugField')(populate_from='name', unique=True, unique_with=(), max_length=50))

    def backwards(self, orm):
        # Adding model 'JobSpec'
        db.create_table('core_jobspec', (
            ('modified', self.gf('model_utils.fields.AutoLastModifiedField')(default=datetime.datetime.now)),
            ('start', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('finish', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('job', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Job'])),
            ('created', self.gf('model_utils.fields.AutoCreatedField')(default=datetime.datetime.now)),
            ('status', self.gf('model_utils.fields.StatusField')(default='pending', no_check_for_status=True, max_length=100)),
            ('spec', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Spec'], related_name='job_specs')),
        ))
        db.send_create_signal('core', ['JobSpec'])

        # Adding field 'Spec.latest_python_versions'
        db.add_column('core_spec', 'latest_python_versions',
                      self.gf('jsonfield.fields.JSONField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Spec.modified'
        db.add_column('core_spec', 'modified',
                      self.gf('model_utils.fields.AutoLastModifiedField')(default=datetime.datetime.now),
                      keep_default=False)

        # Adding field 'Spec.latest_release_date'
        db.add_column('core_spec', 'latest_release_date',
                      self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Spec.latest_version'
        db.add_column('core_spec', 'latest_version',
                      self.gf('django.db.models.fields.CharField')(blank=True, default='', max_length=20),
                      keep_default=False)

        # Adding field 'Spec.created'
        db.add_column('core_spec', 'created',
                      self.gf('model_utils.fields.AutoCreatedField')(default=datetime.datetime.now),
                      keep_default=False)

        # Deleting field 'Spec.created_at'
        db.delete_column('core_spec', 'created_at')

        # Deleting field 'Spec.updated_at'
        db.delete_column('core_spec', 'updated_at')

        # Deleting field 'Spec.started_at'
        db.delete_column('core_spec', 'started_at')

        # Deleting field 'Spec.finished_at'
        db.delete_column('core_spec', 'finished_at')

        # Adding field 'Job.modified'
        db.add_column('core_job', 'modified',
                      self.gf('model_utils.fields.AutoLastModifiedField')(default=datetime.datetime.now),
                      keep_default=False)

        # Adding field 'Job.start'
        db.add_column('core_job', 'start',
                      self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Job.finish'
        db.add_column('core_job', 'finish',
                      self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Job.created'
        db.add_column('core_job', 'created',
                      self.gf('model_utils.fields.AutoCreatedField')(default=datetime.datetime.now),
                      keep_default=False)

        # Deleting field 'Job.created_at'
        db.delete_column('core_job', 'created_at')

        # Deleting field 'Job.updated_at'
        db.delete_column('core_job', 'updated_at')

        # Deleting field 'Job.started_at'
        db.delete_column('core_job', 'started_at')

        # Deleting field 'Job.finished_at'
        db.delete_column('core_job', 'finished_at')

        # Removing M2M table for field specs on 'Job'
        db.delete_table(db.shorten_name('core_job_specs'))

        # Adding field 'Package.created'
        db.add_column('core_package', 'created',
                      self.gf('model_utils.fields.AutoCreatedField')(default=datetime.datetime.now),
                      keep_default=False)

        # Adding field 'Package.modified'
        db.add_column('core_package', 'modified',
                      self.gf('model_utils.fields.AutoLastModifiedField')(default=datetime.datetime.now),
                      keep_default=False)

        # Deleting field 'Package.created_at'
        db.delete_column('core_package', 'created_at')

        # Deleting field 'Package.updated_at'
        db.delete_column('core_package', 'updated_at')


        # Changing field 'Package.slug'
        db.alter_column('core_package', 'slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=50))

    models = {
        'core.job': {
            'Meta': {'object_name': 'Job'},
            'created_at': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            'finished_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'requirements': ('django.db.models.fields.TextField', [], {}),
            'specs': ('django.db.models.fields.related.ManyToManyField', [], {'null': 'True', 'to': "orm['core.Spec']", 'blank': 'True', 'symmetrical': 'False'}),
            'started_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'status': ('model_utils.fields.StatusField', [], {'default': "'pending'", 'no_check_for_status': 'True', 'max_length': '100'}),
            'updated_at': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'})
        },
        'core.package': {
            'Meta': {'object_name': 'Package'},
            'ci_status': ('django.db.models.fields.CharField', [], {'default': "'unknown'", 'max_length': '20'}),
            'ci_url': ('django.db.models.fields.URLField', [], {'blank': 'True', 'max_length': '200'}),
            'comment_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'comment_most_voted': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'created_at': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            'fork_url': ('django.db.models.fields.URLField', [], {'blank': 'True', 'max_length': '200'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'issue_status': ('django.db.models.fields.CharField', [], {'default': "'unknown'", 'max_length': '20'}),
            'issue_url': ('django.db.models.fields.URLField', [], {'blank': 'True', 'max_length': '200'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'pr_status': ('django.db.models.fields.CharField', [], {'default': "'unknown'", 'max_length': '20'}),
            'pr_url': ('django.db.models.fields.URLField', [], {'blank': 'True', 'max_length': '200'}),
            'repo_last_commit_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'repo_url': ('django.db.models.fields.URLField', [], {'blank': 'True', 'max_length': '200'}),
            'slug': ('autoslug.fields.AutoSlugField', [], {'populate_from': "'name'", 'unique': 'True', 'unique_with': '()', 'max_length': '50'}),
            'updated_at': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'})
        },
        'core.spec': {
            'Meta': {'index_together': "(('package', 'version'),)", 'unique_together': "(('package', 'version'),)", 'object_name': 'Spec'},
            'code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'created_at': ('model_utils.fields.AutoCreatedField', [], {'default': 'datetime.datetime.now'}),
            'finished_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'package': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.Package']"}),
            'python_versions': ('jsonfield.fields.JSONField', [], {'null': 'True', 'blank': 'True'}),
            'release_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'started_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'status': ('model_utils.fields.StatusField', [], {'default': "'pending'", 'no_check_for_status': 'True', 'max_length': '100'}),
            'updated_at': ('model_utils.fields.AutoLastModifiedField', [], {'default': 'datetime.datetime.now'}),
            'version': ('django.db.models.fields.CharField', [], {'blank': 'True', 'max_length': '20'})
        }
    }

    complete_apps = ['core']
