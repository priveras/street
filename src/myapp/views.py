from django.views import generic
from .models import Project, Team, Comment, Assumption, Problem, BusinessModel, Solution, Metric, File, Profile, Summary, Past, Future, Tutorial, Elevator
from django.contrib.auth.models import User
from django.db.models import Q
from .forms import ProfileForm
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from datetime import date

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

        return context

class SeedView(generic.DetailView):
    model = Project
    template_name = 'seed.html'

    def get_context_data(self, **kwargs):
        context = super(SeedView, self).get_context_data(**kwargs)
        context['team'] = Team.objects.filter(project=self.object)
        context['permission'] = Team.objects.filter(project=self.object).filter(user=self.request.user).filter(permission="edit")
        context['comments'] = Comment.objects.filter(project=self.object)
        context['assumptions'] = Assumption.objects.filter(project=self.object).filter(stage="seed")
        context['problems'] = Problem.objects.filter(project=self.object).filter(stage="seed")
        context['solutions'] = Solution.objects.filter(project=self.object).filter(stage="seed")
        context['models'] = BusinessModel.objects.filter(project=self.object).filter(stage="seed")
        context['metrics'] = Metric.objects.filter(project=self.object).filter(stage="seed")
        context['summary'] = Summary.objects.filter(project=self.object).filter(stage="seed")
        context['past'] = Past.objects.filter(project=self.object).filter(stage="seed")
        context['future'] = Future.objects.filter(project=self.object).filter(stage="seed")
        context['elevators'] = Elevator.objects.filter(project=self.object).filter(stage="seed")

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