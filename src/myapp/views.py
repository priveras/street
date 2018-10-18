from django.views import generic
from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import render, redirect, Http404
from django.views.decorators.csrf import csrf_exempt
from datetime import date
from django.http import JsonResponse
from django.utils.text import slugify
from django.utils.crypto import get_random_string
from django.core.mail import send_mail
from django.template.loader import get_template
from django.template import Context

from .forms import ProfileForm, SummaryForm, PastForm, FutureForm, ProjectForm
from .forms import ElevatorForm, ProblemForm, SolutionForm, BusinessModelForm
from .forms import AssumptionForm, CommentForm, FileForm, DvfForm, LinkForm
from .forms import InviteForm, ObjectiveForm

from .models import Project, Team, Comment, Assumption, Problem, BusinessModel
from .models import Solution, Metric, File, Profile, Summary, Past, Future
from .models import Elevator, Tutorial, Progress, Dvf, Link, Zone, Invite, Resource
from .models import Objective
from django.http import HttpResponseRedirect
from pinax.eventlog.models import Log

class LibraryView(generic.ListView):
    template_name = 'library.html'
    context_object_name = 'resources_list'
    model = Resource

    def get_context_data(self, **kwargs):
        context = super(LibraryView, self).get_context_data(**kwargs)
        context['resources_list'] = Resource.objects.all()

        return context

class DashboardProjectsView(generic.ListView):
    template_name = 'dashboard/projects.html'
    context_object_name = 'projects_list'
    model = Project

    def get_context_data(self, **kwargs):
        context = super(DashboardProjectsView, self).get_context_data(**kwargs)
        context['projects_list'] = Project.objects.order_by("-created_at")
        context['assumptions'] = Assumption.objects.all()
        context['objectives'] = Objective.objects.all()
        context['elevators'] = Elevator.objects.all()
        context['problems'] = Problem.objects.all()
        context['solutions'] = Solution.objects.all()
        context['models'] = BusinessModel.objects.all()
        context['dvf'] = Dvf.objects.all()
        context['futures'] = Future.objects.all()
        context['summaries'] = Summary.objects.all()
        context['links'] = Link.objects.all()
        context['files'] = File.objects.all()

        return context

def index(request):
    return HttpResponseRedirect('/projects/')

# Error Pages
def server_error(request):
    return render(request, 'errors/500.html')

def not_found(request):
    return render(request, 'errors/404.html')

def permission_denied(request):
    return render(request, 'errors/403.html')

def bad_request(request):
    return render(request, 'errors/400.html')

def learn(request):
    tutorial = Tutorial.objects.order_by('created_at')
    progress = Progress.objects.filter(user=request.user).first()
    doc = progress
    if doc is None:
        doc = Progress()

    saved = [
        doc.zx_dashboard,
        doc.os_model,
        doc.assumptions,
        doc.elevator_pitch,
        doc.problem,
        doc.solution,
        doc.business_model,
        doc.checkpoint,
        doc.assumption_list,
        doc.traction,
        doc.dashboard,
        doc.next_steps,
    ]

    return render(request, 'learn.html', {
        'tutorial': tutorial,
        'progress': progress,
        'saved': saved,
    })

class DashboardView(generic.ListView):
    template_name = 'dashboard/reports.html'
    # context_object_name = 'users_list'
    model = Project

    def get_context_data(self, **kwargs):
        context = super(DashboardView, self).get_context_data(**kwargs)

        context['projects'] = Project.objects.order_by('title')
        context['users'] = User.objects.order_by('first_name')
        context['actives'] = Project.objects.filter(status="Active")
        context['killed'] = Project.objects.filter(status="Killed")
        context['assumptions_list'] = Assumption.objects.all()
        context['comments_list'] = Comment.objects.all()
        context['dvfs'] = Dvf.objects.all()

        context['concept_list'] = Project.objects.filter(stage = "Concept").filter(status = "Active")
        context['scale_list'] = Project.objects.filter(stage = "Scale").filter(status = "Active")
        context['seed_list'] = Project.objects.filter(stage = "Seed 3") | Project.objects.filter(stage = "Seed 2") | Project.objects.filter(stage = "Seed 1").filter(status = "Active")
        context['seedlaunch_list'] = Project.objects.filter(stage = "Seed Launch")
        context['launch_list'] = Project.objects.filter(stage = "Launch")

        context['zones_apacs_seed'] = (Zone.objects.filter(project__stage="Seed 1") | Zone.objects.filter(project__stage="Seed 2") | Zone.objects.filter(project__stage="Seed 3")).filter(zone="APAC S")
        context['zones_apacs_seedlaunch'] = Zone.objects.filter(project__stage="Seed Launch").filter(zone="APAC S")
        context['zones_apacs_launch'] = Zone.objects.filter(project__stage="Launch").filter(zone="APAC S")

        context['zones_apacn_seed'] = (Zone.objects.filter(project__stage="Seed 1") | Zone.objects.filter(project__stage="Seed 2") | Zone.objects.filter(project__stage="Seed 3")).filter(zone="APAC N")
        context['zones_apacn_seedlaunch'] = Zone.objects.filter(project__stage="Seed Launch").filter(zone="APAC N")
        context['zones_apacn_launch'] = Zone.objects.filter(project__stage="Launch").filter(zone="APAC N")

        context['zones_eu_seed'] = (Zone.objects.filter(project__stage="Seed 1") | Zone.objects.filter(project__stage="Seed 2") | Zone.objects.filter(project__stage="Seed 3")).filter(zone="EU")
        context['zones_eu_seedlaunch'] = Zone.objects.filter(project__stage="Seed Launch").filter(zone="EU")
        context['zones_eu_launch'] = Zone.objects.filter(project__stage="Launch").filter(zone="EU")

        context['zones_naz_seed'] = (Zone.objects.filter(project__stage="Seed 1") | Zone.objects.filter(project__stage="Seed 2") | Zone.objects.filter(project__stage="Seed 3")).filter(zone="NAZ")
        context['zones_naz_seedlaunch'] = Zone.objects.filter(project__stage="Seed Launch").filter(zone="NAZ")
        context['zones_naz_launch'] = Zone.objects.filter(project__stage="Launch").filter(zone="NAZ")

        context['zones_maz_seed'] = (Zone.objects.filter(project__stage="Seed 1") | Zone.objects.filter(project__stage="Seed 2") | Zone.objects.filter(project__stage="Seed 3")).filter(zone="MAZ")
        context['zones_maz_seedlaunch'] = Zone.objects.filter(project__stage="Seed Launch").filter(zone="MAZ")
        context['zones_maz_launch'] = Zone.objects.filter(project__stage="Launch").filter(zone="MAZ")

        context['zones_lan_seed'] = (Zone.objects.filter(project__stage="Seed 1") | Zone.objects.filter(project__stage="Seed 2") | Zone.objects.filter(project__stage="Seed 3")).filter(zone="LAN LAS")
        context['zones_lan_seedlaunch'] = Zone.objects.filter(project__stage="Seed Launch").filter(zone="LAN LAS")
        context['zones_lan_launch'] = Zone.objects.filter(project__stage="Launch").filter(zone="LAN LAS")

        context['logs'] = Log.objects.all()

        return context


class DetailView(generic.DetailView):
    model = Project
    template_name = 'detail.html'

    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)

        if not self.request.user.is_superuser:
            if not Team.objects.filter(user=self.request.user,
                project__id=self.object.id).exists():
                raise Http404

        context['recent_activity'] = 'recent_activity.html'
        context['team'] = Team.objects.filter(project=self.object).filter(permission="edit")

        context['viewers'] = Team.objects.filter(project=self.object).filter(permission="view")
        context['comments'] = Comment.objects.filter(project=self.object).order_by('-created_at')
        context['files'] = File.objects.filter(project=self.object).order_by('-updated_at')
        context['links'] = Link.objects.filter(project=self.object).order_by('-updated_at')
        context['dvf_seed'] = Dvf.objects.filter(project=self.object).filter(stage="seed").order_by('-updated_at')
        context['dvf_seedlaunch'] = Dvf.objects.filter(project=self.object).filter(stage="seedlaunch").order_by('-updated_at')
        context['dvf_launch'] = Dvf.objects.filter(project=self.object).filter(stage="launch").order_by('-updated_at')
        context['permission'] = Team.objects.filter(project=self.object).filter(user=self.request.user).filter(permission="edit")
        context['fileform'] = FileForm()

        context['elevators'] = Elevator.objects.filter(project=self.object).order_by('-updated_at')
        context['problems'] = Problem.objects.filter(project=self.object).order_by('-updated_at')
        context['solutions'] = Solution.objects.filter(project=self.object).order_by('-updated_at')
        context['models'] = BusinessModel.objects.filter(project=self.object).order_by('-updated_at')
        context['seed_summary'] = Summary.objects.filter(project=self.object).filter(stage="seed").order_by('-updated_at')
        context['seedlaunch_summary'] = Summary.objects.filter(project=self.object).filter(stage="seedlaunch").order_by('-updated_at')
        context['launch_summary'] = Summary.objects.filter(project=self.object).filter(stage="launch").order_by('-updated_at')

        context['logs'] = Log.objects.all()

        return context
    # def dispatch(self, *args, **kwargs):
    #     if not Team.objects.filter(user=self.request.user,
    #             project__id=self.object.id).exists():
    #         raise Http404

    #     return super(DetailView, self).dispatch(*args, **kwargs)

class SeedView(generic.DetailView):
    model = Project
    template_name = 'seed.html'

    def get_context_data(self, **kwargs):
        context = super(SeedView, self).get_context_data(**kwargs)
        context['team'] = Team.objects.filter(project=self.object)
        context['permission'] = Team.objects.filter(project=self.object).filter(user=self.request.user).filter(permission="edit")
        context['comments'] = Comment.objects.filter(project=self.object)
        context['assumptions'] = Assumption.objects.filter(project=self.object).filter(stage="seed").order_by('dvf')
        context['objectives'] = Objective.objects.filter(project=self.object).filter(stage="seed").order_by('dvf')
        context['summary'] = Summary.objects.filter(project=self.object).filter(stage="seed").order_by('-updated_at')
        context['past'] = Past.objects.filter(project=self.object).filter(stage="seed").order_by('-updated_at')
        context['future'] = Future.objects.filter(project=self.object).filter(stage="seed").order_by('-updated_at')
        context['dvf_seed'] = Dvf.objects.filter(project=self.object).filter(stage="seed").order_by('-updated_at')

        return context

class SeedLaunchView(generic.DetailView):
    model = Project
    template_name = 'seed-launch.html'

    def get_context_data(self, **kwargs):
        context = super(SeedLaunchView, self).get_context_data(**kwargs)
        context['team'] = Team.objects.filter(project=self.object)
        context['comments'] = Comment.objects.filter(project=self.object)
        context['assumptions'] = Assumption.objects.filter(project=self.object).filter(stage="seedlaunch").order_by('dvf')
        context['objectives'] = Objective.objects.filter(project=self.object).filter(stage="seedlaunch").order_by('dvf')
        context['summary'] = Summary.objects.filter(project=self.object).filter(stage="seedlaunch").order_by('-updated_at')
        context['past'] = Past.objects.filter(project=self.object).filter(stage="seedlaunch").order_by('-updated_at')
        context['future'] = Future.objects.filter(project=self.object).filter(stage="seedlaunch").order_by('-updated_at')
        context['permission'] = Team.objects.filter(project=self.object).filter(user=self.request.user).filter(permission="edit")
        context['dvf_seedlaunch'] = Dvf.objects.filter(project=self.object).filter(stage="seedlaunch").order_by('-updated_at')

        return context

class LaunchView(generic.DetailView):
    model = Project
    template_name = 'launch.html'

    def get_context_data(self, **kwargs):
        context = super(LaunchView, self).get_context_data(**kwargs)
        context['team'] = Team.objects.filter(project=self.object)
        context['comments'] = Comment.objects.filter(project=self.object)
        context['assumptions'] = Assumption.objects.filter(project=self.object).filter(stage="launch").order_by('dvf')
        context['objectives'] = Objective.objects.filter(project=self.object).filter(stage="launch").order_by('dvf')
        context['summary'] = Summary.objects.filter(project=self.object).filter(stage="launch").order_by('-updated_at')
        context['past'] = Past.objects.filter(project=self.object).filter(stage="launch").order_by('-updated_at')
        context['future'] = Future.objects.filter(project=self.object).filter(stage="launch").order_by('-updated_at')
        context['permission'] = Team.objects.filter(project=self.object).filter(user=self.request.user).filter(permission="edit")
        context['dvf_launch'] = Dvf.objects.filter(project=self.object).filter(stage="launch").order_by('-updated_at')

        return context

class HomeView(generic.ListView):
    template_name = 'home.html'
    context_object_name = 'projects_list'
    model = Project


    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)

        self.request.session['session_var_name'] = "Value"

        if date.today() == self.request.user.date_joined.date():
            alert = True
        else:
            alert = False

        context['projects_list'] = Project.objects.filter(team__user=self.request.user).order_by('title')
        context['alert'] = alert

        return context

class AdminpanelView(generic.ListView):
    template_name = 'adminpanel.html'
    model = Project

    def get_context_data(self, **kwargs):
        context = super(AdminpanelView, self).get_context_data(**kwargs)

        if date.today() == self.request.user.date_joined.date():
            alert = True
        else:
            alert = False

        context['concept_list'] = Project.objects.filter(stage = "Concept")
        context['scale_list'] = Project.objects.filter(stage = "Scale")
        context['seed_list'] = Project.objects.filter(stage = "Seed 1" or "Seed 2" or "Seed 3")
        context['seedlaunch_list'] = Project.objects.filter(stage = "Seed Launch")
        context['launch_list'] = Project.objects.filter(stage = "Launch")

        # #APAC S projects list
        # context['APACSSeed_list'] = Project.objects.filter(zone = "APAC S", stage = "Seed 1")
        # context['APACSSeedLaunch_list'] = Project.objects.filter(zone = "APAC S", stage = "Seed Launch")
        # context['APACSLaunch_list'] = Project.objects.filter(zone = "APAC S", stage = "Launch")

        # #APAC N projects list
        # context['APACNSeed_list'] = Project.objects.filter(zone = "APAC N", stage = "Seed 1")
        # context['APACNSeedLaunch_list'] = Project.objects.filter(zone = "APAC N", stage = "Seed Launch")
        # context['ApacnLaunch_list'] = Project.objects.filter(zone = "APAC N", stage = "Launch")

        # #EU projects list
        # context['EUSeed_list'] = Project.objects.filter(zone = "EU", stage = "Seed 1")
        # context['EUSeedLaunch_list'] = Project.objects.filter(zone = "EU", stage = "Seed Launch")
        # context['EULaunch_list'] = Project.objects.filter(zone = "EU", stage = "Launch")

        # #NAZ projects list
        # context['NAZSeed_list'] = Project.objects.filter(zone = "NAZ", stage = "Seed 1")
        # context['NAZSeedLaunch_list'] = Project.objects.filter(zone = "NAZ", stage = "Seed Launch")
        # context['NAZLaunch_list'] = Project.objects.filter(zone = "NAZ", stage = "Launch")

        # #MAZ projects list
        # context['MAZSeed_list'] = Project.objects.filter(zone = "MAZ", stage = "Seed 1")
        # context['MAZSeedLaunch_list'] = Project.objects.filter(zone = "MAZ", stage = "Seed Launch")
        # context['MAZLaunch_list'] = Project.objects.filter(zone = "MAZ", stage = "Launch")

        # #LAS/LAN projects list
        # context['LANSeed_list'] = Project.objects.filter(zone = "LAN LAS", stage = "Seed 1")
        # context['LANSeedLaunch_list'] = Project.objects.filter(zone = "LAN LAS", stage = "Seed Launch")
        # context['LANLaunch_list'] = Project.objects.filter(zone = "LAN LAS", stage = "Launch")

        context['killed_list'] = Project.objects.filter(status = "Killed")
        context['active_list'] = Project.objects.filter(status = "Active")
        context['users_list'] = User.objects.filter()
        context['assumptions_list'] = Assumption.objects.filter()
        context['comments_list'] = Comment.objects.filter()

        context['alert'] = alert

        return context

class FaqView(generic.TemplateView):
    template_name = 'faq.html'

class TutorialView(generic.TemplateView):
    template_name = 'tutorial.html'

class InfoView(generic.CreateView):
    model = Profile
    form_class = ProfileForm
    template_name = 'registration/info.html'

    def form_valid(self, form):
        p = form.save(commit=False)
        p.user = self.request.user

        user = self.request.user
        user.first_name = self.request.POST.get('first_name', '')
        user.last_name = self.request.POST.get('last_name', '')
        user.save()



        #if there is an existent profile, edit it
        profile = Profile.objects.filter(user=self.request.user).first()
        if profile is not None:
            p.id = profile.id

        p.save()
        return redirect('/projects/')


@csrf_exempt
def model_form(request, name='', project_id=0, id=0):
    forms = {
        'summary': SummaryForm,
        'past': PastForm,
        'future': FutureForm,
        'elevator': ElevatorForm,
        'problem': ProblemForm,
        'solution': SolutionForm,
        'business_model': BusinessModelForm,
        'assumption': AssumptionForm,
        'dvf': DvfForm,
        'link': LinkForm,
        'project': ProjectForm,
        'file': FileForm,
        'objective':ObjectiveForm,
    }

    instances = {
        'summary': Summary,
        'past': Past,
        'future': Future,
        'elevator': Elevator,
        'problem': Problem,
        'solution': Solution,
        'business_model': BusinessModel,
        'assumption': Assumption,
        'dvf': Dvf,
        'link': Link,
        'project': Project,
        'file': File,
        'objective': Objective,
    }

    method = request.method

    if method == 'DELETE':
        obj = instances.get(name, None)
        if obj is None:
            raise Http404('instance name not found')

        doc = obj.objects.filter(pk=id).first()
        if doc is None:
            raise Http404('id not found')

        doc.user = request.user
        doc.delete()
        return JsonResponse({'status': 'ok'})

    form = forms.get(name, None)
    if form is None:
        raise Http404('name not found')

    if id == 0:
        f = form() if method == 'GET' else form(data=request.POST)
    else:
        obj = instances.get(name, None)
        if obj is None:
            raise Http404('instance name not found')

        try:
            if name == 'project':
                instance = obj.objects.get(pk=id)
            else:
                instance = obj.objects.get(project_id=project_id, pk=id)

            f = form(instance=instance) if method == 'GET' else form(instance=instance, data=request.POST)
        except:
            raise Http404('id not found')

    context = {
        'form': f,
        'name': name,
        'project_id': project_id,
        'id': id,
    }

    if name == 'project':
        context['showstage'] = True

    if method == 'GET':
        return render(request, 'form.html', context)

    if not f.is_valid():
        context['form'] = f
        return render(request, 'form.html', context, status=400)

    project = Project.objects.filter(pk=project_id).first()
    if project is None:
        raise Http404('project not foud')

    doc = f.save(commit=False)
    doc.user = request.user
    if name != 'project':
        doc.project = project
    doc.save()

    return JsonResponse({'status': 'ok'})

def project_form(request, id=0):
    method = request.method

    if id == 0:
        f = ProjectForm() if method == 'GET' else ProjectForm(data=request.POST)
    else:
        try:
            instance = Project.objects.get(pk=id)
            f = ProjectForm(instance=instance) if method == 'GET' else ProjectForm(instance=instance, data=request.POST)
        except:
            raise Http404('id not found')
    context = {
        'form': f,
        'id': id,
        'showstage': True,
        'error': '',
    }

    if method == 'GET':
        return render(request, 'form.html', context)

    if not f.is_valid():
        context['form'] = f
        return render(request, 'form.html', context, status=400)

    try:
        p = f.save(commit=False)
        p.slug = slugify(p.title)
        p.user = request.user
        p.save()

        if id==0:
            doc = Team()
            doc.permission = "edit"
            doc.user = request.user
            doc.project = p
            doc.save()
    except:
        context['error'] = 'Project name already taken'
        return render(request, 'form.html', context, status=400)

    return JsonResponse({'status': 'ok'})

def comment_save(request):
    if request.method != 'POST':
        raise Http404

    form = CommentForm(data=request.POST)
    if not form.is_valid():
        return JsonResponse(form.errors, status=400)

    doc = form.save(commit=False)
    doc.user = request.user
    doc.save()
    return JsonResponse({'status': 'ok'})

def file_save(request):
    if request.method != 'POST':
        raise Http404

    form = FileForm(request.POST, request.FILES)
    if not form.is_valid():
        return JsonResponse(form.errors, status=400)

    doc = form.save(commit=False)
    doc.user = request.user
    doc.save()
    return redirect(request.META['HTTP_REFERER'])


@csrf_exempt
def save_learn_progress(request, section=0, value=0):
    if request.method != 'POST':
        raise Http404

    doc = Progress.objects.filter(user=request.user).first()
    if doc is None:
        doc = Progress()

    section = int(section)
    value = int(value)
    opt = True if value == 1 else False

    if section == 0:
        doc.zx_dashboard = opt
    elif section == 1:
        doc.os_model = opt
    elif section == 2:
        doc.assumptions = opt
    elif section == 3:
        doc.elevator_pitch = opt
    elif section == 4:
        doc.problem = opt
    elif section == 5:
        doc.solution = opt
    elif section == 6:
        doc.business_model = opt
    elif section == 7:
        doc.checkpoint = opt
    elif section == 8:
        doc.assumption_list = opt
    elif section == 9:
        doc.traction = opt
    elif section == 10:
        doc.dashboard = opt
    elif section == 11:
        doc.next_steps = opt

    doc.user = request.user
    doc.save()
    return JsonResponse({'status': 'ok'})


def send_invite(request, project_id=0):
    if request.method not in ['POST', 'GET']:
        raise Http404

    project = Project.objects.filter(pk=project_id).first()
    if project is None:
        raise Http404

    context = {
        'form': InviteForm(),
        'project': project,
        'project_id': project_id,
    }

    if request.method == 'GET':
        return render(request, 'form.html', context)

    form = InviteForm(request.POST)
    if not form.is_valid():
        context['form'] = form
        return render(request, 'form.html', context, status=400)

    perm = Team.objects.filter(
        project__id=project_id,
        permission='edit',
        user=request.user
    ).exists()

    if not perm:
        raise Http404

    doc = form.save(commit=False)
    doc.user = request.user
    doc.key = get_random_string(length=32)
    doc.project = project
    doc.save()

    host = request.META['HTTP_HOST'] + '/invite/claim?key='

    plaintext = get_template('mails/invite.txt')
    context = {
        'link': host+doc.key,
        'project': project,
        'user': request.user,
    }

    text_content = plaintext.render(context)

    send_mail(
        'You have been invited to Box OS',
        text_content,
        'admin@box-os.com',
        [request.POST.get('email')],
        fail_silently=True,
    )

    return JsonResponse({'status': 'ok'})


@csrf_exempt
def leave_project(request, project_id):
    if request.method != 'POST':
        raise Http404

    Team.objects.filter(project__id=project_id, user=request.user).delete()
    return JsonResponse({'status': 'ok'})


def check_invite(request):
    if request.method != 'GET':
        raise Http404

    key = request.GET.get('key', None)
    if key is None:
        raise Http404

    invite = Invite.objects.filter(
        user=request.user,
        key=key,
        used=False).first()

    if invite is None:
        raise Http404

    doc = Team()
    doc.user = request.user
    doc.project = invite.project
    doc.permission = invite.permission
    doc.save()

    invite.used = True
    invite.save()

    return redirect('/')
