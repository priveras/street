from django.db import models
from django.contrib.auth.models import User

class Progress(models.Model):
    user = models.ForeignKey(User, unique=True)
    zx_dashboard = models.BooleanField(default=False, blank=True)
    os_model = models.BooleanField(default=False, blank=True)
    assumptions = models.BooleanField(default=False, blank=True)
    elevator_pitch = models.BooleanField(default=False, blank=True)
    problem = models.BooleanField(default=False, blank=True)
    solution = models.BooleanField(default=False, blank=True)
    business_model = models.BooleanField(default=False, blank=True)
    checkpoint = models.BooleanField(default=False, blank=True)
    assumption_list = models.BooleanField(default=False, blank=True)
    traction = models.BooleanField(default=False, blank=True)
    dashboard = models.BooleanField(default=False, blank=True)
    next_steps = models.BooleanField(default=False, blank=True)

    def __str__(self):
        return str(self.user)


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

    STAGE_CONCEPT = 'Concept'
    STAGE_SEED_1 = 'Seed 1'
    STAGE_SEED_2 = 'Seed 2'
    STAGE_SEED_3 = 'Seed 3'
    STAGE_LAUNCH_1 = 'Seed Launch'
    STAGE_LAUNCH_2 = 'Launch'
    STAGE_SCALE = 'Scale'

    STATUS_ALL = (
        (STATUS_ACTIVE, 'Active'),
        (STATUS_ARCHIVED, 'Archived'),
        (STATUS_KILLED, 'Killed'),
        (STATUS_DRAFT, 'Draft'),
        )

    STAGES = (
        (STAGE_CONCEPT, 'Concept'),
        (STAGE_SEED_1, 'Seed 1'),
        (STAGE_SEED_2, 'Seed 2'),
        (STAGE_SEED_3, 'Seed 3'),
        (STAGE_LAUNCH_1, 'Seed Launch'),
        (STAGE_LAUNCH_2, 'Launch'),
        (STAGE_SCALE, 'Scale'),
        )

    title = models.CharField(max_length=200, blank=False, null=False)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField(blank=True)
    stage = models.CharField(choices=STAGES, max_length=200, blank=True)
    status = models.CharField(choices=STATUS_ALL, max_length=200)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(db_index=True, auto_now_add=True)

    def __str__(self):
        return str(self.title)

class Team(models.Model):
    user = models.ForeignKey(User)
    project = models.ForeignKey(Project)
    permission_choices = (
            ('edit', 'Edit'),
            ('view', 'View'),
            )
    permission = models.CharField(choices=permission_choices, max_length=200, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(db_index=True, auto_now_add=True)

    def __str__(self):
        return str(self.user)

class Comment(models.Model):
    project = models.ForeignKey(Project)
    user = models.ForeignKey(User)
    text = models.TextField(blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(db_index=True, auto_now_add=True)

    def __str__(self):
        return str(self.user)

class Link(models.Model):
    project = models.ForeignKey(Project)
    user = models.ForeignKey(User)
    title = models.CharField(max_length=500, null=False, blank=False)
    link = models.URLField(null=False, blank=False)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(db_index=True, auto_now_add=True)

    def __str__(self):
        return str(self.project)

class Dvf(models.Model):
    user = models.ForeignKey(User)
    project = models.ForeignKey(Project)
    stage_choices = (
            ('seed', 'Seed'),
            ('seedlaunch', 'Seed Launch'),
            ('launch', 'Launch'),
            )
    stage = models.CharField(choices=stage_choices, max_length=200, blank=True)
    status_choices = (
            ('On Track', 'On Track'),
            ('Delayed', 'Delayed'),
            ('At Risk', 'At Risk'),
            )
    desirability = models.CharField(choices=status_choices, max_length=200, blank=True)
    viability = models.CharField(choices=status_choices, max_length=200, blank=True)
    feasibility = models.CharField(choices=status_choices, max_length=200, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(db_index=True, auto_now_add=True)

    def __str__(self):
        return str(self.project)

class Zone(models.Model):
    project = models.ForeignKey(Project)

    ZONE_APACS = 'APAC S'
    ZONE_APACN = 'APAC N'
    ZONE_EU = 'EU'
    ZONE_NAZ = 'NAZ'
    ZONE_MAZ = 'MAZ'
    ZONE_LAS = 'LAN LAS'

    ZONES = (
        (ZONE_APACS, 'APAC S'),
        (ZONE_APACN, 'APAC N'),
        (ZONE_EU, 'EU'),
        (ZONE_NAZ, 'NAZ'),
        (ZONE_MAZ, 'MAZ'),
        (ZONE_LAS, 'LAN LAS'),
        )

    zone = models.CharField(choices=ZONES, max_length=200, blank=True)

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
            ('Inconclusive', 'Inconclusive'),
            )
    status = models.CharField(choices=status_choices, max_length=200, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(db_index=True, auto_now_add=True)

    def __str__(self):
        return str(self.project)

class Metric(models.Model):
    user = models.ForeignKey(User)
    project = models.ForeignKey(Project, null=True)
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

class Objective(models.Model):
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
    file = models.FileField(upload_to='files/%Y%m%d', blank=False, null=False)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(db_index=True, auto_now_add=True)

    def __str__(self):
        return str(self.project)


class Invite(models.Model):
    PERMISSION_EDIT = 'edit'
    PERMISSION_VIEW = 'view'

    PERMISSIONS = (
        (PERMISSION_EDIT, 'Edit'),
        (PERMISSION_VIEW, 'View'),
    )

    permission = models.CharField(choices=PERMISSIONS, max_length=10)
    user = models.ForeignKey(User)
    project = models.ForeignKey(Project)
    email = models.EmailField()
    key = models.CharField(max_length=32)
    used = models.BooleanField(default=False)

    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(db_index=True, auto_now_add=True)
