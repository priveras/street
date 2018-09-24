# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import Project, Team, Comment, Assumption, Problem, BusinessModel, Metric, File, Past, Future, Summary, Solution, Tutorial, Profile, Link

class ProjectAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}

class TutorialAdmin(SummernoteModelAdmin):
    summernote_fields = ('content',)

admin.site.register(Tutorial, TutorialAdmin)

admin.site.register(Project, ProjectAdmin)
admin.site.register(Team)
admin.site.register(Profile)
admin.site.register(Comment)
admin.site.register(Assumption)
admin.site.register(Problem)
admin.site.register(BusinessModel)
admin.site.register(Solution)
admin.site.register(Metric)
admin.site.register(File)
admin.site.register(Past)
admin.site.register(Future)
admin.site.register(Summary)
admin.site.register(Link)
