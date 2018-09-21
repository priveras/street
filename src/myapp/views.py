from django.views import generic
from .models import Project, Team, Comment, Assumption, Problem, BusinessModel, Solution, Metric, File, Profile, Summary, Past, Future, Tutorial
from django.contrib.auth.models import User
from django.db.models import Q
from .forms import ProfileForm
from django.shortcuts import render

def learn(request):
    tutorial = Tutorial.objects.all()

    return render(request, 'learn.html',{'tutorial':tutorial})

class DetailView(generic.DetailView):
    model = Project
    template_name = 'detail.html'

    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)
        context['team'] = Team.objects.filter(project=self.object)
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
        context['comments'] = Comment.objects.filter(project=self.object)
        context['assumptions'] = Assumption.objects.filter(project=self.object)
        context['problems'] = Problem.objects.filter(project=self.object)
        context['solutions'] = Solution.objects.filter(project=self.object)
        context['models'] = BusinessModel.objects.filter(project=self.object)
        context['metrics'] = Metric.objects.filter(project=self.object)
        context['summary'] = Summary.objects.filter(project=self.object)
        context['past'] = Past.objects.filter(project=self.object)
        context['future'] = Future.objects.filter(project=self.object)

        return context

class HomeView(generic.ListView):
    template_name = 'home.html'
    context_object_name = 'projects_list'
    model = Project

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context['projects_list'] = Project.objects.filter(team__user=self.request.user)

        return context

class RegisterView(generic.CreateView):
    model = Profile
    form_class = ProfileForm
    template_name = 'registration/register.html'

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
        return redirect('/')