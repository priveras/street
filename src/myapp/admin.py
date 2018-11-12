# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import Project, Team, Comment, Assumption, Primary, Empathy
from .models import Metric, File, Past, Future, Summary, Secondary, Tutorial
from .models import Profile, Link, Dvf, Progress, Zone, Invite, Resource, Elevator, Tool, Wallet, Billing
from .models import Objective
from import_export.admin import ImportExportModelAdmin

#class ProjectAdmin(admin.ModelAdmin):
    #prepopulated_fields = {'slug': ('title',)}

class TutorialAdmin(SummernoteModelAdmin):
    summernote_fields = ('content',)


admin.site.register(Tutorial, TutorialAdmin)
@admin.register(Project)
class ProjectAdmin(ImportExportModelAdmin):
    pass
admin.site.register(Team)
admin.site.register(Elevator)
admin.site.register(Profile)
admin.site.register(Comment)
@admin.register(Assumption)
class AssumptionAdmin(ImportExportModelAdmin):
    pass
admin.site.register(Primary)
admin.site.register(Empathy)
admin.site.register(Billing)
admin.site.register(Secondary)
admin.site.register(Zone)
admin.site.register(Metric)
admin.site.register(File)
admin.site.register(Past)
admin.site.register(Future)
admin.site.register(Summary)
admin.site.register(Link)
admin.site.register(Wallet)
admin.site.register(Dvf)
admin.site.register(Progress)
admin.site.register(Invite)
@admin.register(Resource)
class ResourceAdmin(ImportExportModelAdmin):
    pass
admin.site.register(Objective)
admin.site.register(Tool)
