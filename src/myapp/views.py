from django.views import generic
from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import render, redirect, Http404
from django.views.decorators.csrf import csrf_exempt
from datetime import date
from django.http import JsonResponse
from django.utils.text import slugify

from .forms import ProfileForm, SummaryForm, PastForm, FutureForm, ProjectForm
from .forms import ElevatorForm, ProblemForm, SolutionForm, BusinessModelForm
from .forms import AssumptionForm, CommentForm

from .models import Project, Team, Comment, Assumption, Problem, BusinessModel
from .models import Solution, Metric, File, Profile, Summary, Past, Future, Link, Dvf
from .models import Elevator, Tutorial
from django.http import HttpResponseRedirect

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

    return render(request, 'learn.html',{'tutorial':tutorial})

class DetailView(generic.DetailView):
    model = Project
    template_name = 'detail.html'

    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)
        context['team'] = Team.objects.filter(project=self.object).filter(permission="edit")
        context['viewers'] = Team.objects.filter(project=self.object).filter(permission="view")
        context['comments'] = Comment.objects.filter(project=self.object)
        context['files'] = File.objects.filter(project=self.object).order_by('-updated_at')
        context['links'] = Link.objects.filter(project=self.object).order_by('-updated_at')
        context['dvf_seed'] = Dvf.objects.filter(project=self.object).filter(stage="seed").order_by('-updated_at')
        context['dvf_seedlaunch'] = Dvf.objects.filter(project=self.object).filter(stage="seedlaunch").order_by('-updated_at')
        context['dvf_launch'] = Dvf.objects.filter(project=self.object).filter(stage="launch").order_by('-updated_at')
        context['permission'] = Team.objects.filter(project=self.object).filter(user=self.request.user).filter(permission="edit")

        return context

class SeedView(generic.DetailView):
    model = Project
    template_name = 'seed.html'

    def get_context_data(self, **kwargs):
        context = super(SeedView, self).get_context_data(**kwargs)
        context['team'] = Team.objects.filter(project=self.object)
        context['permission'] = Team.objects.filter(project=self.object).filter(user=self.request.user).filter(permission="edit")
        context['comments'] = Comment.objects.filter(project=self.object)
        context['assumptions'] = Assumption.objects.filter(project=self.object).filter(stage="seed").order_by('dvf')
        context['problems'] = Problem.objects.filter(project=self.object).filter(stage="seed").order_by('-updated_at')
        context['solutions'] = Solution.objects.filter(project=self.object).filter(stage="seed").order_by('-updated_at')
        context['models'] = BusinessModel.objects.filter(project=self.object).filter(stage="seed").order_by('-updated_at')
        context['metrics'] = Metric.objects.filter(project=self.object).filter(stage="seed").order_by('-updated_at')
        context['summary'] = Summary.objects.filter(project=self.object).filter(stage="seed").order_by('-updated_at')
        context['past'] = Past.objects.filter(project=self.object).filter(stage="seed").order_by('-updated_at')
        context['future'] = Future.objects.filter(project=self.object).filter(stage="seed").order_by('-updated_at')
        context['elevators'] = Elevator.objects.filter(project=self.object).filter(stage="seed").order_by('-updated_at')
        context['dvf_seed'] = Dvf.objects.filter(project=self.object).filter(stage="seed").order_by('-updated_at')

        return context

class SeedLaunchView(generic.DetailView):
    model = Project
    template_name = 'seed-launch.html'

    def get_context_data(self, **kwargs):
        context = super(SeedLaunchView, self).get_context_data(**kwargs)
        context['team'] = Team.objects.filter(project=self.object)
        context['comments'] = Comment.objects.filter(project=self.object)
        context['assumptions'] = Assumption.objects.filter(project=self.object).filter(stage="seedlaunch")
        context['problems'] = Problem.objects.filter(project=self.object).filter(stage="seedlaunch").order_by('-updated_at')
        context['solutions'] = Solution.objects.filter(project=self.object).filter(stage="seedlaunch").order_by('-updated_at')
        context['models'] = BusinessModel.objects.filter(project=self.object).filter(stage="seedlaunch").order_by('-updated_at')
        context['metrics'] = Metric.objects.filter(project=self.object).filter(stage="seedlaunch").order_by('-updated_at')
        context['summary'] = Summary.objects.filter(project=self.object).filter(stage="seedlaunch").order_by('-updated_at')
        context['past'] = Past.objects.filter(project=self.object).filter(stage="seedlaunch").order_by('-updated_at')
        context['future'] = Future.objects.filter(project=self.object).filter(stage="seedlaunch").order_by('-updated_at')
        context['elevators'] = Elevator.objects.filter(project=self.object).filter(stage="seedlaunch").order_by('-updated_at')
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
        context['assumptions'] = Assumption.objects.filter(project=self.object).filter(stage="launch")
        context['problems'] = Problem.objects.filter(project=self.object).filter(stage="launch").order_by('-updated_at')
        context['solutions'] = Solution.objects.filter(project=self.object).filter(stage="launch").order_by('-updated_at')
        context['models'] = BusinessModel.objects.filter(project=self.object).filter(stage="launch").order_by('-updated_at')
        context['metrics'] = Metric.objects.filter(project=self.object).filter(stage="launch").order_by('-updated_at')
        context['summary'] = Summary.objects.filter(project=self.object).filter(stage="launch").order_by('-updated_at')
        context['past'] = Past.objects.filter(project=self.object).filter(stage="launch").order_by('-updated_at')
        context['future'] = Future.objects.filter(project=self.object).filter(stage="launch").order_by('-updated_at')
        context['elevators'] = Elevator.objects.filter(project=self.object).filter(stage="launch").order_by('-updated_at')
        context['permission'] = Team.objects.filter(project=self.object).filter(user=self.request.user).filter(permission="edit")
        context['dvf_launch'] = Dvf.objects.filter(project=self.object).filter(stage="launch").order_by('-updated_at')

        return context

class HomeView(generic.ListView):
    template_name = 'home.html'
    context_object_name = 'projects_list'
    model = Project

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)

        if date.today() == self.request.user.date_joined.date():
            alert = True
        else:
            alert = False

        context['projects_list'] = Project.objects.filter(team__user=self.request.user)
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
    }

    method = request.method

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

    if method == 'GET':
        return render(request, 'form.html', context)

    if not f.is_valid():
        context['form'] = f
        return JsonResponse(f.errors, status=400)

    project = Project.objects.filter(pk=project_id).first()
    if project is None:
        raise Http404('project not foud')

    doc = f.save(commit=False)
    doc.user = request.user
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
        doc = f.save(commit=False)
        doc.slug = slugify(doc.title)
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
