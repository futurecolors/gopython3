from django.contrib import admin
from . import models


class LineInline(admin.TabularInline):
    model = models.Job.specs.through
    extra = 0


class JobAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'created_at', 'updated_at']
    readonly_fields = ['started_at', 'finished_at']
    inlines = [LineInline]


class SpeckAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'release_date', 'python_versions',
                    'created_at', 'updated_at', 'status']
    list_filter = ['status']


class PackageAdmin(admin.ModelAdmin):
    list_display = ['name', 'repo_url', 'issue_url', 'created_at', 'updated_at']


admin.site.register(models.Job, JobAdmin)
admin.site.register(models.Spec, SpeckAdmin)
admin.site.register(models.Package, PackageAdmin)
