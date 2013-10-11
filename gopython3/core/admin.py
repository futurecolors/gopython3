from django.contrib import admin
from . import models


class SpeckInline(admin.TabularInline):
    model = models.JobSpec
    readonly_fields = ['spec', 'start', 'finish', 'status']
    extra = 0


class JobAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'created', 'modified', 'status']
    readonly_fields = ['start', 'finish', 'status']
    list_filter = ['status']
    inlines = [SpeckInline]


class SpeckAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'release_date', 'python_versions',
                    'created', 'modified', 'status']
    list_filter = ['status']


class PackageAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'repo_url', 'issue_url', 'created', 'modified']


admin.site.register(models.Job, JobAdmin)
admin.site.register(models.Spec, SpeckAdmin)
admin.site.register(models.Package, PackageAdmin)
