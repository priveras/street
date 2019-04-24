from django.views import generic
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, Http404, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from datetime import date, datetime, timezone
from django.http import JsonResponse, HttpResponse
from django.template import Context
from django.core import serializers
from django.core.mail import send_mail
from .forms import *

from .models import *
from django.http import HttpResponseRedirect

class HubView(generic.ListView):
    template_name = 'hub.html'
    context_object_name = 'announcements'
    model = Announcement


    def get_context_data(self, **kwargs):
        context = super(HubView, self).get_context_data(**kwargs)
        context = {
            'announcements' : Announcement.objects.order_by('-created_at')[:5],
            'articles' : Article.objects.order_by('-created_at')[:20],
            'teams' : Team.objects.order_by('-created_at')[:20],
            'feature' : Feature.objects.order_by('-created_at')[:1],
            'members': User.objects.order_by('-date_joined').filter(profile__isnull=False).filter(profile__status='Active')[:10],
            'total_members': Profile.objects.count(),
            'total_resources': Resource.objects.count(),
            'total_teams': Team.objects.count(),
        }

        return context

@csrf_exempt
def delete_vendor(request, vendor_id):
    if request.method != 'POST':
        raise Http404

    Vendor.objects.filter(id=vendor_id, user=request.user).delete()
    return JsonResponse({'status': 'ok'})

@csrf_exempt
def delete_post(request, post_id):
    if request.method != 'POST':
        raise Http404

    Post.objects.filter(id=post_id, user=request.user).delete()
    return JsonResponse({'status': 'ok'})

@csrf_exempt
def delete_comment(request, comment_id):
    if request.method != 'POST':
        raise Http404

    Comment.objects.filter(id=comment_id, user=request.user).delete()
    return JsonResponse({'status': 'ok'})

@csrf_exempt
def delete_event(request, event_id):
    if request.method != 'POST':
        raise Http404

    Event.objects.filter(id=event_id, user=request.user).delete()
    return JsonResponse({'status': 'ok'})

@csrf_exempt
def delete_job(request, job_id):
    if request.method != 'POST':
        raise Http404

    Job.objects.filter(id=job_id, user=request.user).delete()
    return JsonResponse({'status': 'ok'})

class VendorsView(generic.ListView):
    template_name = 'vendors.html'
    context_object_name = 'vendors'
    model = Vendor


    def get_context_data(self, **kwargs):
        context = super(VendorsView, self).get_context_data(**kwargs)
        context['vendors'] = Vendor.objects.order_by('title')

        return context

class VendorCreateView(generic.CreateView):
    model = Vendor
    form_class = VendorForm
    template_name = 'vendor_create.html'

    def form_valid(self, form):
        p = form.save(commit=False)
        p.user = self.request.user
        p.save()
        return redirect('/vendors/')

class VendorUpdateView(generic.UpdateView):
    model = Vendor
    form_class = VendorForm
    template_name = 'vendor_create.html'

    def user_passes_test(self, request):
        if request.user.is_authenticated():
            self.object = self.get_object()
            return self.object.user == request.user
        return False

    def dispatch(self, request, *args, **kwargs):
        if not self.user_passes_test(request):
            return HttpResponseRedirect('/')
        return super(VendorUpdateView, self).dispatch(
            request, *args, **kwargs)

    def form_valid(self, form):
        p = form.save(commit=False)
        p.user = self.request.user
        p.save()
        return redirect('/vendors/')

class EventCreateView(generic.CreateView):
    model = Event
    form_class = EventForm
    template_name = 'events_create.html'

    def form_valid(self, form):
        p = form.save(commit=False)
        p.user = self.request.user
        p.save()
        return redirect('/events/')

class EventUpdateView(generic.UpdateView):
    model = Event
    form_class = EventForm
    template_name = 'events_create.html'

    def user_passes_test(self, request):
        if request.user.is_authenticated():
            self.object = self.get_object()
            return self.object.user == request.user
        return False

    def dispatch(self, request, *args, **kwargs):
        if not self.user_passes_test(request):
            return HttpResponseRedirect('/')
        return super(EventUpdateView, self).dispatch(
            request, *args, **kwargs)

    def form_valid(self, form):
        p = form.save(commit=False)
        p.user = self.request.user
        p.save()
        return redirect('/events/')

class EventsView(generic.ListView):
    template_name = 'events.html'
    context_object_name = 'events'
    model = Event


    def get_context_data(self, **kwargs):
        context = super(EventsView, self).get_context_data(**kwargs)
        context['events'] = Event.objects.order_by('datetime')

        return context

def profile(request, username):
    member = get_object_or_404(User, username=username)
    posts = Post.objects.filter(user=member).order_by('-created_at')[:10]

    return render(request,
                  'profile.html',
                  {
                      'member': member,
                      'posts': posts,
                  })

def index(request):
    return redirect('/home/')

def home(
    request,
    template='home.html',
    page_template='home_page.html'):

    if date.today() == request.user.date_joined.date():
        alert = True
    else:
        alert = False

    context = {
        'posts': Post.objects.order_by('-created_at'),
        'resources': Resource.objects.order_by('-created_at')[:3],
        'members': User.objects.order_by('-date_joined').filter(profile__isnull=False).filter(profile__status='Active')[:10],
        'post_block': 'post_block.html',
        'post_comment': 'post_comment.html',
    }

    if request.is_ajax():
        template = page_template
    return render(request, template, context)

class JobCreateView(generic.CreateView):
    model = Job
    form_class = JobForm
    template_name = 'jobs_create.html'

    def form_valid(self, form):
        p = form.save(commit=False)
        p.user = self.request.user
        p.save()
        return redirect('/jobs/')

class JobUpdateView(generic.UpdateView):
    model = Job
    form_class = JobForm
    template_name = 'jobs_create.html'

    def user_passes_test(self, request):
        if request.user.is_authenticated():
            self.object = self.get_object()
            return self.object.user == request.user
        return False

    def dispatch(self, request, *args, **kwargs):
        if not self.user_passes_test(request):
            return HttpResponseRedirect('/')
        return super(JobUpdateView, self).dispatch(
            request, *args, **kwargs)

    def form_valid(self, form):
        p = form.save(commit=False)
        p.user = self.request.user
        p.save()
        return redirect('/jobs/')

class InfoView(generic.CreateView):
    model = Profile
    form_class = ProfileForm
    template_name = 'registration/info.html'

    def form_valid(self, form):

        p = form.save(commit=False)
        p.user = self.request.user
        p.status = 'Pending'

        user = self.request.user
        user.first_name = self.request.POST.get('first_name', '')
        user.last_name = self.request.POST.get('last_name', '')
        user.save()

        p.save()
        return redirect('/home/')

class InfoUpdateView(generic.UpdateView):
    model = Profile
    form_class = ProfileForm
    template_name = 'registration/info.html'

    def user_passes_test(self, request):
        if request.user.is_authenticated():
            self.object = self.get_object()
            return self.object.user == request.user
        return False

    def dispatch(self, request, *args, **kwargs):
        if not self.user_passes_test(request):
            return HttpResponseRedirect('/')
        return super(InfoUpdateView, self).dispatch(
            request, *args, **kwargs)

    def form_valid(self, form):
        p = form.save(commit=False)
        p.user = self.request.user
        p.status = 'Active'

        user = self.request.user
        user.first_name = self.request.POST.get('first_name', '')
        user.last_name = self.request.POST.get('last_name', '')
        user.save()

        p.save()
        return redirect('/home/')

@csrf_exempt
def post_create(request):
    template = 'post_block.html'
    if request.method != 'POST':
        resp = JsonResponse({'error':'method not allowed'})
        resp.status_code = 400
        return  resp

    if not request.user.is_authenticated:
        resp = JsonResponse({'error':'user is not authenticated'})
        resp.status_code = 400
        return  resp

    p = PostForm(request.POST)
    if not p.is_valid():
        resp = JsonResponse(p.errors)
        resp.status_code = 400
        return resp

    post = p.save(commit=False)
    post.user = request.user
    post.save()

    context = {
            'post': post,
            'post_comment': 'post_comment.html',
            }

    return render(request, template, context)

@csrf_exempt
def comment_create(request):
    template = 'post_comment.html'
    if request.method != 'POST':
        resp = JsonResponse({'error':'method not allowed'})
        resp.status_code = 400
        return  resp

    if not request.user.is_authenticated:
        resp = JsonResponse({'error':'user is not authenticated'})
        resp.status_code = 400
        return  resp

    f = CommentForm(request.POST)
    if not f.is_valid():
        resp = JsonResponse(f.errors)
        resp.status_code = 400
        return resp

    comment = f.save(commit=False)
    comment.user = request.user
    comment.save()
    #send_mail('New Comment', 'Hi! Just wanted to let you know that your post has a new comment. Login to VC Platform to see the message.', 'hello@attomik.com', [comment.post.user.email])

    context = {'comment': comment}
    return render(request, template, context)

class MembersAdminView(generic.ListView):
    template_name = 'admin/members.html'
    context_object_name = 'members'
    model = User


    def get_context_data(self, **kwargs):
        context = super(MembersAdminView, self).get_context_data(**kwargs)
        context['members'] = User.objects.order_by('-date_joined')

        return context

class MembersView(generic.ListView):
    template_name = 'members.html'
    context_object_name = 'members'
    model = User


    def get_context_data(self, **kwargs):
        context = super(MembersView, self).get_context_data(**kwargs)
        context['members'] = User.objects.filter(profile__isnull=False).filter(profile__status='Active').order_by('first_name')

        return context


class ResourcesView(generic.ListView):
    template_name = 'resources.html'
    context_object_name = 'resources'
    model = Resource


    def get_context_data(self, **kwargs):
        context = super(ResourcesView, self).get_context_data(**kwargs)
        context['resources'] = Resource.objects.order_by('-created_at')

        return context

class JobsView(generic.ListView):
    template_name = 'jobs.html'
    context_object_name = 'jobs'
    model = Job


    def get_context_data(self, **kwargs):
        context = super(JobsView, self).get_context_data(**kwargs)
        context['jobs'] = Job.objects.order_by('-created_at')

        return context

class StatusView(generic.TemplateView):
    template_name = "status.html"

def analytics(request):


    how_many_days = 30
    today = dt.date.today()

    context = {
        'contributors': Log.objects.values('user').annotate(total=Count('user_id')).order_by('-total'),
        'projects_month': Project.objects.filter(created_at__gte=datetime.now()-timedelta(days=how_many_days)),
        'users_month': User.objects.filter(date_joined__gte=datetime.now()-timedelta(days=how_many_days)),
        'assumptions_month': Assumption.objects.filter(created_at__gte=datetime.now()-timedelta(days=how_many_days)),
        'activity_month': Log.objects.filter(timestamp__gte=datetime.now()-timedelta(days=how_many_days)),
        'projects' : Project.objects.all(),
        'projects_active' : Project.objects.filter(status='Active').count(),
        'projects_draft' : Project.objects.filter(status='Draft').count(),
        'projects_killed' : Project.objects.filter(status='Killed').count(),
        'users': User.objects.count(),
        'users_list': User.objects.order_by('-date_joined'),
        'assumptions': Assumption.objects.count(),
        'assumptions_validated': Assumption.objects.filter(status='Validated').count(),
        'assumptions_inprogress': Assumption.objects.filter(status='In Progress').count(),
        'assumptions_invalidated': Assumption.objects.filter(status='Invalidated').count(),
        'activity': Log.objects.count(),
        'logs': Log.objects.order_by('-timestamp')[:50],

    }

    return render(request, 'dashboard/analytics.html', context)

# Error Pages
def server_error(request):
    return render(request, 'errors/500.html')

def not_found(request):
    return render(request, 'errors/404.html')

def permission_denied(request):
    return render(request, 'errors/403.html')

def bad_request(request):
    return render(request, 'errors/400.html')