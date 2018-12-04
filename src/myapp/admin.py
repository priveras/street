# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import Profile, Resource, Post, Comment, Job, Event
from import_export.admin import ImportExportModelAdmin

admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Job)
admin.site.register(Event)

class TutorialAdmin(SummernoteModelAdmin):
    summernote_fields = ('content',)

admin.site.register(Profile)
class AssumptionAdmin(ImportExportModelAdmin):
    pass
@admin.register(Resource)
class ResourceAdmin(ImportExportModelAdmin):
    pass

