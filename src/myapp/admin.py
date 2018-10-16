# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import Project, Team, Comment, Assumption, Problem, BusinessModel
from .models import Metric, File, Past, Future, Summary, Solution, Tutorial
from .models import Profile, Link, Dvf, Progress, Zone, Invite, Resource, Elevator
from .models import Objective

class ProjectAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}

class TutorialAdmin(SummernoteModelAdmin):
    summernote_fields = ('content',)


admin.site.register(Tutorial, TutorialAdmin)
admin.site.register(Project, ProjectAdmin)
admin.site.register(Team)
admin.site.register(Elevator)
admin.site.register(Profile)
admin.site.register(Comment)
admin.site.register(Assumption)
admin.site.register(Problem)
admin.site.register(BusinessModel)
admin.site.register(Solution)
admin.site.register(Zone)
admin.site.register(Metric)
admin.site.register(File)
admin.site.register(Past)
admin.site.register(Future)
admin.site.register(Summary)
admin.site.register(Link)
admin.site.register(Dvf)
admin.site.register(Progress)
admin.site.register(Invite)
admin.site.register(Resource)
admin.site.register(Objective)
