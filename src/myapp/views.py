from django.views import generic
from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import render, redirect, Http404
from django.views.decorators.csrf import csrf_exempt
from datetime import date
from django.http import JsonResponse

from .forms import ProfileForm, SummaryForm, PastForm, FutureForm
from .forms import ElevatorForm, ProblemForm, SolutionForm, BusinessModelForm
from .forms import AssumptionForm

from .models import Project, Team, Comment, Assumption, Problem, BusinessModel
from .models import Solution, Metric, File, Profile, Summary, Past, Future
from .models import Elevator, Tutorial


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
        context['assumptions'] = Assumption.objects.filter(project=self.object)
        context['problems'] = Problem.objects.filter(project=self.object)
        context['solutions'] = Solution.objects.filter(project=self.object)
        context['models'] = BusinessModel.objects.filter(project=self.object)
        context['metrics'] = Metric.objects.filter(project=self.object)
        context['files'] = File.objects.filter(project=self.object)
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
        context['assumptions'] = Assumption.objects.filter(project=self.object).filter(stage="seed").order_by('-updated_at')
        context['problems'] = Problem.objects.filter(project=self.object).filter(stage="seed").order_by('-updated_at')
        context['solutions'] = Solution.objects.filter(project=self.object).filter(stage="seed").order_by('-updated_at')
        context['models'] = BusinessModel.objects.filter(project=self.object).filter(stage="seed").order_by('-updated_at')
        context['metrics'] = Metric.objects.filter(project=self.object).filter(stage="seed").order_by('-updated_at')
        context['summary'] = Summary.objects.filter(project=self.object).filter(stage="seed").order_by('-updated_at')
        context['past'] = Past.objects.filter(project=self.object).filter(stage="seed").order_by('-updated_at')
        context['future'] = Future.objects.filter(project=self.object).filter(stage="seed").order_by('-updated_at')
        context['elevators'] = Elevator.objects.filter(project=self.object).filter(stage="seed").order_by('-updated_at')

        return context

class SeedLaunchView(generic.DetailView):
    model = Project
    template_name = 'seed-launch.html'

    def get_context_data(self, **kwargs):
        context = super(SeedLaunchView, self).get_context_data(**kwargs)
        context['team'] = Team.objects.filter(project=self.object)
        context['comments'] = Comment.objects.filter(project=self.object)
        context['assumptions'] = Assumption.objects.filter(project=self.object).filter(stage="seedlaunch")
        context['problems'] = Problem.objects.filter(project=self.object).filter(stage="seedlaunch")
        context['solutions'] = Solution.objects.filter(project=self.object).filter(stage="seedlaunch")
        context['models'] = BusinessModel.objects.filter(project=self.object).filter(stage="seedlaunch")
        context['metrics'] = Metric.objects.filter(project=self.object).filter(stage="seedlaunch")
        context['summary'] = Summary.objects.filter(project=self.object).filter(stage="seedlaunch")
        context['past'] = Past.objects.filter(project=self.object).filter(stage="seedlaunch")
        context['future'] = Future.objects.filter(project=self.object).filter(stage="seedlaunch")
        context['elevators'] = Elevator.objects.filter(project=self.object).filter(stage="seedlaunch")
        context['permission'] = Team.objects.filter(project=self.object).filter(user=self.request.user).filter(permission="edit")

        return context

class LaunchView(generic.DetailView):
    model = Project
    template_name = 'launch.html'

    def get_context_data(self, **kwargs):
        context = super(LaunchView, self).get_context_data(**kwargs)
        context['team'] = Team.objects.filter(project=self.object)
        context['comments'] = Comment.objects.filter(project=self.object)
        context['assumptions'] = Assumption.objects.filter(project=self.object).filter(stage="launch")
        context['problems'] = Problem.objects.filter(project=self.object).filter(stage="launch")
        context['solutions'] = Solution.objects.filter(project=self.object).filter(stage="launch")
        context['models'] = BusinessModel.objects.filter(project=self.object).filter(stage="launch")
        context['metrics'] = Metric.objects.filter(project=self.object).filter(stage="launch")
        context['summary'] = Summary.objects.filter(project=self.object).filter(stage="launch")
        context['past'] = Past.objects.filter(project=self.object).filter(stage="launch")
        context['future'] = Future.objects.filter(project=self.object).filter(stage="launch")
        context['elevators'] = Elevator.objects.filter(project=self.object).filter(stage="launch")
        context['permission'] = Team.objects.filter(project=self.object).filter(user=self.request.user).filter(permission="edit")

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
