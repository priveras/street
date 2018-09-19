# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Project, Team, Comment, Assumption, Problem, BusinessModel, Metric, File

class ProjectAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}

admin.site.register(Project, ProjectAdmin)
admin.site.register(Team)
admin.site.register(Comment)
admin.site.register(Assumption)
admin.site.register(Problem)
admin.site.register(BusinessModel)
admin.site.register(Metric)
admin.site.register(File)
