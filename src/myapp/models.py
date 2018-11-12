from django.db import models
from django.contrib.auth.models import User
from pinax.eventlog.models import log
from datetime import datetime, timezone


class Billing(models.Model):
    _SILVER = 'silver'
    _GOLD = 'gold'
    _PLATINUM = 'platinum'

    CHOICES = (
        (_SILVER, _SILVER),
        (_GOLD, _GOLD),
        (_PLATINUM, _PLATINUM),
    )

    user = models.ForeignKey(User)
    plan = models.CharField(choices=CHOICES, max_length=20)
    priority = models.IntegerField(default=1)
    token = models.CharField(max_length=100)
    customer = models.CharField(max_length=100)
    status = models.IntegerField(default=1)
    valid_until = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(db_index=True, auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)


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

    user = models.ForeignKey(User, blank=True, null=True)
    title = models.CharField(max_length=200, blank=False, null=False)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField(blank=True)
    status = models.CharField(choices=STATUS_ALL, max_length=200)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(db_index=True, auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.id:
            log(
                user=self.user,
                action='CREATE_PROJECT',
                obj=self,
                extra={
                    "project_slug": self.slug,
                    "project": self.title,
                    "description": self.description,
                    "status": self.status,
                    "event": "created project"
                    }
                )
        else:
            log(
                user=self.user,
                action='EDIT_PROJECT',
                obj=self,
                extra={
                    "project_id": self.id,
                    "project": self.title,
                    "description": self.description,
                    "status": self.status,
                    "event": "edited project"
                    }
                )

        super(Project, self).save(args, kwargs)

    def __str__(self):
        return str(self.title)

class Elevator(models.Model):
    user = models.ForeignKey(User)
    project = models.ForeignKey(Project)
    text = models.TextField()
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(db_index=True, auto_now_add=True)

    def save(self, *args, **kwargs):

        if not self.id:
            log(
                user=self.user,
                action='ADD_ELEVATOR',
                obj=self,
                extra={
                    "project_id": self.project.id,
                    "project": self.project.title,
                    "text": self.text,
                    "event": "added elevator pitch"
                    }
                )
        else:
            log(
                user=self.user,
                action='EDIT_ELEVATOR',
                obj=self,
                extra={
                    "project_id": self.project.id,
                    "project": self.project.title,
                    "text": self.text,
                    "event": "edited elevator pitch"
                    }
                )

        super(Elevator, self).save(args, kwargs)

    def delete(self, *args, **kwargs):

        log(
            user=self.user,
            action='DELETE_ELEVATOR',
            obj=self,
            extra={
                "project_id": self.project.id,
                "project": self.project.title,
                "text": self.text,
                "event": "deleted elevator pitch"
                }
            )

        super(Elevator, self).delete(args, kwargs)

    def __str__(self):
        return str(self.project)

    def __str__(self):
        return str(self.title)

class Resource(models.Model):
    user = models.ForeignKey(User)
    title = models.CharField(max_length=300, blank=True)
    excerpt = models.TextField(blank=True)
    link = models.CharField(max_length=300, blank=True)
    file = models.FileField(upload_to='files/%Y%m%d', blank=True)
    featured = models.BooleanField(default=False, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(db_index=True, auto_now_add=True)

    def __str__(self):
        return str(self.title)

class Tool(models.Model):
    user = models.ForeignKey(User)
    title = models.CharField(max_length=300)
    excerpt = models.TextField(blank=True)
    image = models.FileField(upload_to='images/tools/%Y%m%d', null=True)
    link = models.CharField(max_length=300)
    category = models.CharField(max_length=500)
    featured = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(db_index=True, auto_now_add=True)

    def __str__(self):
        return str(self.title)

class Progress(models.Model):
    user = models.ForeignKey(User, unique=True)
    intro = models.BooleanField(default=False, blank=True)
    elevator_pitch = models.BooleanField(default=False, blank=True)
    customer_persona = models.BooleanField(default=False, blank=True)
    empathy_map = models.BooleanField(default=False, blank=True)
    obj = models.BooleanField(default=False, blank=True)
    seo = models.BooleanField(default=False, blank=True)
    google = models.BooleanField(default=False, blank=True)
    content = models.BooleanField(default=False, blank=True)
    tech = models.BooleanField(default=False, blank=True)
    next_steps = models.BooleanField(default=False, blank=True)

    def __str__(self):
        return str(self.user)


class Tutorial(models.Model):
    title = models.CharField(max_length=300)
    content = models.TextField(blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(db_index=True, auto_now_add=True)

class Profile(models.Model):
    user = models.ForeignKey(User, unique=True)
    job_title = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    company = models.CharField(max_length=200)
    profile_image = models.FileField(upload_to='images/%Y%m%d', null=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(db_index=True, auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.id:
            log(
                user=self.user,
                action='CREATE_PROFILE',
                obj=self,
                extra={
                    "job_title": self.job_title,
                    "location": self.location,
                    "company": self.company,
                    "event": "joined UA Framework"
                    }
                )
        else:
            log(
                user=self.user,
                action='EDIT_PROFILE',
                obj=self,
                extra={
                    "job_title": self.job_title,
                    "location": self.location,
                    "company": self.company,
                    "event": "edited profile"
                    }
                )

        super(Profile, self).save(args, kwargs)

    def __str__(self):
        return str(self.user)


class Team(models.Model):
    user = models.ForeignKey(User)
    project = models.ForeignKey(Project)
    permission_choices = (
            ('edit', 'Edit'),
            ('view', 'View'),
            )
    permission = models.CharField(choices=permission_choices, max_length=200)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(db_index=True, auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.id:
            log(
                user=self.user,
                action='ADD_TEAM',
                obj=self,
                extra={
                    "project_id": self.project.id,
                    "project": self.project.title,
                    "permission": self.permission,
                    "event": "joined project"
                    }
                )
        else:
            log(
                user=self.user,
                action='EDIT_TEAM',
                obj=self,
                extra={
                    "project_id": self.project.id,
                    "project": self.project.title,
                    "permission": self.permission,
                    "event": "permission updated"
                    }
                )

        super(Team, self).save(args, kwargs)

    def __str__(self):
        return str(self.user)

class Comment(models.Model):
    project = models.ForeignKey(Project)
    user = models.ForeignKey(User)
    text = models.TextField()
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(db_index=True, auto_now_add=True)

    def save(self, *args, **kwargs):

        if not self.id:
            log(
                user=self.user,
                action='ADD_COMMENT',
                obj=self,
                extra={
                    "project_id": self.project.id,
                    "project": self.project.title,
                    "text": self.text,
                    "event": "added a comment"
                    }
                )

        super(Comment, self).save(args, kwargs)

    def __str__(self):
        return str(self.user)

class Link(models.Model):
    project = models.ForeignKey(Project)
    user = models.ForeignKey(User)
    title = models.CharField(max_length=500, null=False)
    link = models.URLField(null=False)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(db_index=True, auto_now_add=True)

    def __str__(self):
        return str(self.project)

    def save(self, *args, **kwargs):

        if not self.id:
            log(
                user=self.user,
                action='ADD_LINK',
                obj=self,
                extra={
                    "project_id": self.project.id,
                    "project": self.project.title,
                    "title": self.title,
                    "link": self.link,
                    "event": "added link"
                    }
                )

        super(Link, self).save(args, kwargs)

    def delete(self, *args, **kwargs):

        log(
            user=self.user,
            action='DELETE_LINK',
            obj=self,
            extra={
                "project_id": self.project.id,
                "project": self.project.title,
                "title": self.title,
                "link": self.link,
                "event": "deleted link"
                }
            )

        super(Link, self).delete(args, kwargs)

    def __str__(self):
        return str(self.user)

class Dvf(models.Model):
    user = models.ForeignKey(User)
    project = models.ForeignKey(Project)
    stage_choices = (
            ('seed', 'Seed'),
            ('seedlaunch', 'Seed Launch'),
            ('launch', 'Launch'),
            )
    stage = models.CharField(choices=stage_choices, max_length=200)
    status_choices = (
            ('On Track', 'On Track'),
            ('Delayed', 'Delayed'),
            ('At Risk', 'At Risk'),
            )
    desirability = models.CharField(choices=status_choices, max_length=200)
    viability = models.CharField(choices=status_choices, max_length=200)
    feasibility = models.CharField(choices=status_choices, max_length=200)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(db_index=True, auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.id:
            log(
                user=self.user,
                action='ADD_DVF',
                obj=self,
                extra={
                    "project_id": self.project.id,
                    "project": self.project.title,
                    "stage": self.stage,
                    "desirability": self.desirability,
                    "viability": self.viability,
                    "feasibility": self.feasibility,
                    "event": "added DVF"
                    }
                )
        else:

            log(
                user=self.user,
                action='EDIT_DVF',
                obj=self,
                extra={
                    "project_id": self.project.id,
                    "project": self.project.title,
                    "stage": self.stage,
                    "desirability": self.desirability,
                    "viability": self.viability,
                    "feasibility": self.feasibility,
                    "event": "edited dvf"
                    }
                )

        super(Dvf, self).save(args, kwargs)

    def get_active_user_count(User):
        now = datetime.now(timezone.utc)
        count_active = 0
        active_user_list = User.objects.all()

        for u in active_user_list:
            if (now - u.last_login).days > 14:
                count_active += 1

        return count_active


    def time_in_stage(self):
        now = datetime.now(timezone.utc)
        return (now - self.created_at).days

    def getTimeSeed(self):
        dvf_list_seed = Dvf.objects.filter(stage="seed")
        dvfTotal = 0
        now = datetime.now(timezone.utc)
        dvf_seed_count = 0
        dvf_seed_count_biz = 0

        for d in dvf_list_seed:
            if d.project.stage in ('Seed 1', 'Seed 2', 'Seed 3'):
                dvf_seed_count += 1
                dvf_seed_count_biz += 1
                dvfTotal += ((now-d.created_at).days)

        if (dvf_seed_count == 0):
            dvf_seed_count = 0

        else:
            dvf_seed_count = dvfTotal/dvf_seed_count

        return dvf_seed_count

    def getTimeSeedLaunch(self):
        dvf_list_seedlaunch = Dvf.objects.filter(stage="seedlaunch")
        seedlaunch_total = 0
        time_diff = datetime.now(timezone.utc)
        dvf_sl_count = 0
        sl_biz = 0

        for d in dvf_list_seedlaunch:
            if d.project.stage in ('Seed Launch'):
                seedlaunch_total += 1
                dvf_sl_count += 1
                sl_biz += ((time_diff-d.created_at).days)

        if (sl_biz == 0):
            sl_biz = 0

        else:
            sl_biz = seedlaunch_total/(sl_biz)

        return sl_biz

    def getTimeLaunch(self):
        dvf_list_launch = Dvf.objects.filter(stage="launch")
        launch_total = 0
        time_diffs = datetime.now(timezone.utc)
        dvf_l_count = 0
        l_biz = 0

        for d in dvf_list_launch:
            if d.project.stage in ('Launch'):
                launch_total += 1
                dvf_l_count += 1
                l_biz += ((time_diffs-d.created_at).days)

        if (dvf_l_count == 0):
            dvf_l_count = 0

        else:
            l_biz = dvf_l_count/l_biz

        return l_biz




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
    stage = models.CharField(choices=stage_choices, max_length=200)
    dvf_choices = (
            ('desirability', 'Desirability'),
            ('viability', 'Viability'),
            ('feasibility', 'Feasibility'),
            )
    dvf = models.CharField(choices=dvf_choices, max_length=200)
    objective_id = models.TextField(blank=True)
    assumption = models.TextField()
    metric = models.TextField(blank=True)
    learnings = models.TextField(blank=True)
    status_choices = (
            ('Validated', 'Validated'),
            ('In Progress', 'In Progress'),
            ('Invalidated', 'Invalidated'),
            ('Inconclusive', 'Inconclusive'),
            )
    status = models.CharField(choices=status_choices, max_length=200)
    scale_choices = (
            ('high', 'High'),
            ('medium', 'Medium'),
            ('low', 'Low'),
            )
    uncertainty = models.CharField(choices=scale_choices, max_length=200, blank=True)
    critical = models.CharField(choices=scale_choices, max_length=200, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(db_index=True, auto_now_add=True)

    def save(self, *args, **kwargs):

        if not self.id:
            log(
                user=self.user,
                action='ADD_ASSUMPTION',
                obj=self,
                extra={
                    "project_id": self.project.id,
                    "project": self.project.title,
                    "stage": self.stage,
                    "dvf": self.dvf,
                    "text": self.assumption,
                    "metric": self.metric,
                    "learnings": self.learnings,
                    "status": self.status,
                    "uncertainty": self.uncertainty,
                    "critical": self.critical,
                    "event": "added assumption"
                    }
                )
        else:
            log(
                user=self.user,
                action='EDIT_ASSUMPTION',
                obj=self,
                extra={
                    "project_id": self.project.id,
                    "project": self.project.title,
                    "stage": self.stage,
                    "dvf": self.dvf,
                    "text": self.assumption,
                    "metric": self.metric,
                    "learnings": self.learnings,
                    "status": self.status,
                    "event": "edited assumption"
                    }
                )

        super(Assumption, self).save(args, kwargs)

    def delete(self, *args, **kwargs):

        log(
            user=self.user,
            action='DELETE_ASSUMPTION',
            obj=self,
            extra={
                "project_id": self.project.id,
                "project": self.project.title,
                "stage": self.stage,
                "dvf": self.dvf,
                "text": self.assumption,
                "metric": self.metric,
                "learnings": self.learnings,
                "status": self.status,
                "event": "deleted assumption"
                }
            )

        super(Assumption, self).delete(args, kwargs)

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
    stage = models.CharField(choices=stage_choices, max_length=200)
    dvf_choices = (
            ('desirability', 'Desirability'),
            ('viability', 'Viability'),
            ('feasibility', 'Feasibility'),
            )
    dvf = models.CharField(choices=dvf_choices, max_length=200)
    metric = models.TextField()
    value = models.TextField(blank=True)
    status_choices = (
            ('On Track', 'On Track'),
            ('Delayed', 'Delayed'),
            ('At Risk', 'At Risk'),
            )
    status = models.CharField(choices=status_choices, max_length=200)
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
    stage = models.CharField(choices=stage_choices, max_length=200)
    id = models.AutoField(primary_key=True)
    dvf_choices = (
            ('problem', 'Problem'),
            ('solution', 'Solution'),
            ('business model', 'Business Model'),
            )
    dvf = models.CharField(choices=dvf_choices, max_length=200)
    value = models.TextField(blank=True)
    metric = models.TextField(blank=True)
    status_choices = (
            ('Complete', 'Complete'),
            ('On Track', 'On Track'),
            ('Delayed', 'Delayed'),
            ('At Risk', 'At Risk'),
            )
    status = models.CharField(choices=status_choices, max_length=200)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(db_index=True, auto_now_add=True)

    def save(self, *args, **kwargs):

        if not self.id:
            log(
                user=self.user,
                action='ADD_OBJECTIVE',
                obj=self,
                extra={
                    "project_id": self.project.id,
                    "project": self.project.title,
                    "stage": self.stage,
                    "dvf": self.dvf,
                    "value": self.value,
                    "metric": self.metric,
                    "status": self.status,
                    "event": "added objective"
                    }
                )
        else:
            log(
                user=self.user,
                action='EDIT_OBJECTIVE',
                obj=self,
                extra={
                    "project_id": self.project.id,
                    "project": self.project.title,
                    "stage": self.stage,
                    "dvf": self.dvf,
                    "value": self.value,
                    "metric": self.metric,
                    "status": self.status,
                    "event": "edited objective"
                    }
                )

        super(Objective, self).save(args, kwargs)

    def delete(self, *args, **kwargs):

        log(
            user=self.user,
            action='DELETE_OBJECTIVE',
            obj=self,
            extra={
                "project_id": self.project.id,
                "project": self.project.title,
                "stage": self.stage,
                "dvf": self.dvf,
                "value": self.value,
                "metric": self.metric,
                "status": self.status,
                "event": "removed objective"
                }
            )

        super(Objective, self).delete(args, kwargs)

    def __str__(self):
        return str(self.project)

class Primary(models.Model):
    user = models.ForeignKey(User)
    project = models.ForeignKey(Project)
    text = models.TextField()
    status_choices = (
            ('Validated', 'Validated'),
            ('Testing', 'Testing'),
            ('Invalidated', 'Invalidated'),
            )
    status = models.CharField(choices=status_choices, max_length=200)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(db_index=True, auto_now_add=True)

    def save(self, *args, **kwargs):

        if not self.id:
            log(
                user=self.user,
                action='ADD_PRIMARY',
                obj=self,
                extra={
                    "project_id": self.project.id,
                    "project": self.project.title,
                    "text": self.text,
                    "status": self.status,
                    "event": "added a primary persona"
                    }
                )
        else:
            log(
                user=self.user,
                action='EDIT_PROBLEM',
                obj=self,
                extra={
                    "project_id": self.project.id,
                    "project": self.project.title,
                    "text": self.text,
                    "status": self.status,
                    "event": "edited primary persona"
                    }
                )

        super(Primary, self).save(args, kwargs)

    def delete(self, *args, **kwargs):

        log(
            user=self.user,
            action='DELETE_PRIMARY',
            obj=self,
            extra={
                "project_id": self.project.id,
                "project": self.project.title,
                "text": self.text,
                "status": self.status,
                "event": "deleted primary persona"
                }
            )

        super(Primary, self).delete(args, kwargs)

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
    stage = models.CharField(choices=stage_choices, max_length=200)
    text = models.TextField()
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(db_index=True, auto_now_add=True)

    def save(self, *args, **kwargs):

        if not self.id:
            log(
                user=self.user,
                action='ADD_SUMMARY',
                obj=self,
                extra={
                    "project_id": self.project.id,
                    "project": self.project.title,
                    "text": self.text,
                    "stage": self.stage,
                    "event": "added summary"
                    }
                )
        else:
            log(
                user=self.user,
                action='EDIT_SUMMARY',
                obj=self,
                extra={
                    "project_id": self.project.id,
                    "project": self.project.title,
                    "text": self.text,
                    "stage": self.stage,
                    "event": "edited summary"
                    }
                )

        super(Summary, self).save(args, kwargs)

    def delete(self, *args, **kwargs):

        log(
            user=self.user,
            action='DELETE_SUMMARY',
            obj=self,
            extra={
                "project_id": self.project.id,
                "project": self.project.title,
                "text": self.text,
                "stage": self.stage,
                "event": "deleted summary"
                }
            )

        super(Summary, self).delete(args, kwargs)


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
    stage = models.CharField(choices=stage_choices, max_length=200)
    text = models.TextField()
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(db_index=True, auto_now_add=True)

    def save(self, *args, **kwargs):

        if not self.id:
            log(
                user=self.user,
                action='ADD_PRIORITY',
                obj=self,
                extra={
                    "project_id": self.project.id,
                    "project": self.project.title,
                    "text": self.text,
                    "stage": self.stage,
                    "event": "added current priorities"
                    }
                )
        else:
            log(
                user=self.user,
                action='EDIT_PRIORITY',
                obj=self,
                extra={
                    "project_id": self.project.id,
                    "project": self.project.title,
                    "text": self.text,
                    "stage": self.stage,
                    "event": "edited current priorities"
                    }
                )

        super(Future, self).save(args, kwargs)

    def delete(self, *args, **kwargs):

        log(
            user=self.user,
            action='DELETE_PRIORITY',
            obj=self,
            extra={
                "project_id": self.project.id,
                "project": self.project.title,
                "text": self.text,
                "stage": self.stage,
                "event": "deleted current priorities"
                }
            )

        super(Future, self).delete(args, kwargs)

    def __str__(self):
        return str(self.project)

class Secondary(models.Model):
    user = models.ForeignKey(User)
    project = models.ForeignKey(Project)
    text = models.TextField()
    status_choices = (
            ('Validated', 'Validated'),
            ('Testing', 'Testing'),
            ('Invalidated', 'Invalidated'),
            )
    status = models.CharField(choices=status_choices, max_length=200)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(db_index=True, auto_now_add=True)

    def save(self, *args, **kwargs):

        if not self.id:
            log(
                user=self.user,
                action='ADD_SECONDARY',
                obj=self,
                extra={
                    "project_id": self.project.id,
                    "project": self.project.title,
                    "text": self.text,
                    "status": self.status,
                    "event": "added a secondary persona"
                    }
                )
        else:
            log(
                user=self.user,
                action='EDIT_SECONDARY',
                obj=self,
                extra={
                    "project_id": self.project.id,
                    "project": self.project.title,
                    "text": self.text,
                    "status": self.status,
                    "event": "edited secondary persona"
                    }
                )

        super(Secondary, self).save(args, kwargs)

    def delete(self, *args, **kwargs):

        log(
            user=self.user,
            action='DELETE_SECONDARY',
            obj=self,
            extra={
                "project_id": self.project.id,
                "project": self.project.title,
                "text": self.text,
                "status": self.status,
                "event": "deleted secondary persona"
                }
            )

        super(Secondary, self).delete(args, kwargs)

    def __str__(self):
        return str(self.project)

class Empathy(models.Model):
    user = models.ForeignKey(User)
    project = models.ForeignKey(Project)
    description = models.TextField()
    think = models.TextField()
    see = models.TextField()
    say = models.TextField()
    hear = models.TextField()
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(db_index=True, auto_now_add=True)

    def save(self, *args, **kwargs):

        if not self.id:
            log(
                user=self.user,
                action='ADD_EMPATHY_MAP',
                obj=self,
                extra={
                    "project_id": self.project.id,
                    "project": self.project.title,
                    "text": self.description,
                    "text": self.think,
                    "text": self.see,
                    "text": self.say,
                    "text": self.hear,
                    "event": "added empathy map"
                    }
                )
        else:
            log(
                user=self.user,
                action='EDIT_EMPATHY_MAP',
                obj=self,
                extra={
                    "project_id": self.project.id,
                    "project": self.project.title,
                    "text": self.description,
                    "text": self.think,
                    "text": self.see,
                    "text": self.say,
                    "text": self.hear,
                    "event": "edited empathy map"
                    }
                )

        super(Empathy, self).save(args, kwargs)

    def delete(self, *args, **kwargs):

        log(
            user=self.user,
            action='DELETE_EMPATHY_MAP',
            obj=self,
            extra={
                "project_id": self.project.id,
                "project": self.project.title,
                "text": self.description,
                "text": self.think,
                "text": self.see,
                "text": self.say,
                "text": self.hear,
                "event": "deleted empathy map"
                }
            )

        super(Empathy, self).delete(args, kwargs)

    def __str__(self):
        return str(self.project)

class File(models.Model):
    user = models.ForeignKey(User)
    project = models.ForeignKey(Project)
    title = models.CharField(max_length=200)
    file = models.FileField(upload_to='files/%Y%m%d', blank=False, null=False)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(db_index=True, auto_now_add=True)

    def save(self, *args, **kwargs):

        if not self.id:
            log(
                user=self.user,
                action='ADD_FILE',
                obj=self,
                extra={
                    "project_id": self.project.id,
                    "project": self.project.title,
                    "title": self.title,
                    "file": self.file.url,
                    "event": "added a file"
                    }
                )

        super(File, self).save(args, kwargs)

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

class Wallet(models.Model):
    user = models.ForeignKey(User, blank=True, null=True)
    project = models.ForeignKey(Project)
    period_choices = (
            ('1', '1Q18'),
            ('2', '2Q18'),
            ('3', '3Q18'),
            ('4', '4Q18'),
            ('5', '1Q19'),
            ('6', '2Q19'),
            ('7', '3Q19'),
            ('8', '4Q19'),
            )
    period = models.CharField(choices=period_choices, max_length=200)
    amount_budget = models.FloatField(default=0)
    amount_actual = models.FloatField(default=0)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(db_index=True, auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.id:
            log(
                user=self.user,
                action='ADD_COMMENT',
                obj=self,
                extra={
                    "project_id": self.project.id,
                    "project": self.project.title,
                    "amount_budget": self.amount_budget,
                    "amount_actual": self.amount_actual,
                    "period": self.period,
                    "event": "added wallet"
                    }
                )
        else:
            log(
                user=self.user,
                action='EDIT_WALLET',
                obj=self,
                extra={
                    "project_id": self.project.id,
                    "project": self.project.title,
                    "amount_budget": self.amount_budget,
                    "amount_actual": self.amount_actual,
                    "period": self.period,
                    "event": "added wallet"
                    }
                )

        super(Wallet, self).save(args, kwargs)