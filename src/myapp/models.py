from django.db import models
from django.contrib.auth.models import User

class Tutorial(models.Model):
    content = models.TextField(blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(db_index=True, auto_now_add=True)

class Profile(models.Model):
    user = models.ForeignKey(User, unique=True)
    job_title = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    profile_image = models.FileField(upload_to='images/%Y%m%d', null=True)

    def __str__(self):
        return str(self.user)

class Project(models.Model):

	STATUS_ACTIVE = 'Active'
	STATUS_ARCHIVED = 'Archived'
	STATUS_KILLED = 'Killed'
	STATUS_DRAFT = 'Draft'

	STATUS_ALL = (
		(STATUS_ACTIVE, 'Active'),
		(STATUS_ARCHIVED, 'Archived'),
		(STATUS_KILLED, 'Killed'),
		(STATUS_DRAFT, 'Draft'),
	)

	title = models.CharField(max_length=200)
	slug = models.SlugField(max_length=200, unique=True)
	description = models.TextField(blank=True)
	status = models.CharField(choices=STATUS_ALL, max_length=200)
	updated_at = models.DateTimeField(auto_now=True)
	created_at = models.DateTimeField(db_index=True, auto_now_add=True)

	def __str__(self):
		return str(self.title)

class Team(models.Model):
	user = models.ForeignKey(User)
	project = models.ForeignKey(Project)
	updated_at = models.DateTimeField(auto_now=True)
	created_at = models.DateTimeField(db_index=True, auto_now_add=True)

	def __str__(self):
		return str(self.project)

class Comment(models.Model):
    project = models.ForeignKey(Project)
    user = models.ForeignKey(User)
    text = models.TextField(blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(db_index=True, auto_now_add=True)

    def __str__(self):
        return str(self.project)

class Assumption(models.Model):
    user = models.ForeignKey(User)
    project = models.ForeignKey(Project)
    stage_choices = (
            ('seed', 'Seed'),
            ('seedlaunch', 'Seed Launch'),
            ('launch', 'Launch'),
            )
    stage = models.CharField(choices=stage_choices, max_length=200, blank=True)
    dvf_choices = (
            ('desirability', 'Desirability'),
            ('viability', 'Viability'),
            ('feasibility', 'Feasibility'),
            )
    dvf = models.CharField(choices=dvf_choices, max_length=200, blank=True)
    assumption = models.TextField(blank=True)
    metric = models.TextField(blank=True)
    learnings = models.TextField(blank=True)
    status_choices = (
            ('Validated', 'Validated'),
            ('In Progress', 'In Progress'),
            ('Invalidated', 'Invalidated'),
            )
    status = models.CharField(choices=status_choices, max_length=200, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(db_index=True, auto_now_add=True)

    def __str__(self):
        return str(self.project)

class Metric(models.Model):
    user = models.ForeignKey(User)
    project = models.ForeignKey(Project)
    stage_choices = (
            ('seed', 'Seed'),
            ('seedlaunch', 'Seed Launch'),
            ('launch', 'Launch'),
            )
    stage = models.CharField(choices=stage_choices, max_length=200, blank=True)
    dvf_choices = (
            ('desirability', 'Desirability'),
            ('viability', 'Viability'),
            ('feasibility', 'Feasibility'),
            )
    dvf = models.CharField(choices=dvf_choices, max_length=200, blank=True)
    metric = models.TextField(blank=True)
    value = models.TextField(blank=True)
    status_choices = (
            ('On Track', 'On Track'),
            ('Delayed', 'Delayed'),
            ('At Risk', 'At Risk'),
            )
    status = models.CharField(choices=status_choices, max_length=200, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(db_index=True, auto_now_add=True)

    def __str__(self):
        return str(self.project)

class Problem(models.Model):
    user = models.ForeignKey(User)
    project = models.ForeignKey(Project)
    stage_choices = (
            ('seed', 'Seed'),
            ('seedlaunch', 'Seed Launch'),
            ('launch', 'Launch'),
            )
    stage = models.CharField(choices=stage_choices, max_length=200, blank=True)
    text = models.TextField(blank=True)
    status_choices = (
            ('Validated', 'Validated'),
            ('In Progress', 'In Progress'),
            ('Invalidated', 'Invalidated'),
            )
    status = models.CharField(choices=status_choices, max_length=200, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(db_index=True, auto_now_add=True)

    def __str__(self):
        return str(self.project)

class Elevator(models.Model):
    user = models.ForeignKey(User)
    project = models.ForeignKey(Project)
    stage_choices = (
            ('seed', 'Seed'),
            ('seedlaunch', 'Seed Launch'),
            ('launch', 'Launch'),
            )
    stage = models.CharField(choices=stage_choices, max_length=200, blank=True)
    text = models.TextField(blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(db_index=True, auto_now_add=True)

    def __str__(self):
        return str(self.project)

class Summary(models.Model):
    user = models.ForeignKey(User)
    project = models.ForeignKey(Project)
    stage_choices = (
            ('seed', 'Seed'),
            ('seedlaunch', 'Seed Launch'),
            ('launch', 'Launch'),
            )
    stage = models.CharField(choices=stage_choices, max_length=200, blank=True)
    text = models.TextField(blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(db_index=True, auto_now_add=True)

    def __str__(self):
        return str(self.project)

class Past(models.Model):
    user = models.ForeignKey(User)
    project = models.ForeignKey(Project)
    stage_choices = (
            ('seed', 'Seed'),
            ('seedlaunch', 'Seed Launch'),
            ('launch', 'Launch'),
            )
    stage = models.CharField(choices=stage_choices, max_length=200, blank=True)
    text = models.TextField(blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(db_index=True, auto_now_add=True)

    def __str__(self):
        return str(self.project)

class Future(models.Model):
    user = models.ForeignKey(User)
    project = models.ForeignKey(Project)
    stage_choices = (
            ('seed', 'Seed'),
            ('seedlaunch', 'Seed Launch'),
            ('launch', 'Launch'),
            )
    stage = models.CharField(choices=stage_choices, max_length=200, blank=True)
    text = models.TextField(blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(db_index=True, auto_now_add=True)

    def __str__(self):
        return str(self.project)

class Solution(models.Model):
    user = models.ForeignKey(User)
    project = models.ForeignKey(Project)
    stage_choices = (
            ('seed', 'Seed'),
            ('seedlaunch', 'Seed Launch'),
            ('launch', 'Launch'),
            )
    stage = models.CharField(choices=stage_choices, max_length=200, blank=True)
    text = models.TextField(blank=True)
    status_choices = (
            ('Validated', 'Validated'),
            ('In Progress', 'In Progress'),
            ('Invalidated', 'Invalidated'),
            )
    status = models.CharField(choices=status_choices, max_length=200, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(db_index=True, auto_now_add=True)

    def __str__(self):
        return str(self.project)

class BusinessModel(models.Model):
    user = models.ForeignKey(User)
    project = models.ForeignKey(Project)
    stage_choices = (
            ('seed', 'Seed'),
            ('seedlaunch', 'Seed Launch'),
            ('launch', 'Launch'),
            )
    stage = models.CharField(choices=stage_choices, max_length=200, blank=True)
    text = models.TextField(blank=True)
    status_choices = (
            ('Validated', 'Validated'),
            ('In Progress', 'In Progress'),
            ('Invalidated', 'Invalidated'),
            )
    status = models.CharField(choices=status_choices, max_length=200, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(db_index=True, auto_now_add=True)

    def __str__(self):
        return str(self.project)

class File(models.Model):
    user = models.ForeignKey(User)
    project = models.ForeignKey(Project)
    title = models.CharField(max_length=200)
    file = models.FileField(upload_to='files/%Y%m%d')
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(db_index=True, auto_now_add=True)

    def __str__(self):
        return str(self.project)