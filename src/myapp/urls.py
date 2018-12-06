from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views

from . import views

app_name = 'app'
urlpatterns = [
	url(r'^$', login_required(views.index), name='index'),
    url(r'^home/$', login_required(views.home), name='home'),
    url(r'^members/$', login_required(views.MembersView.as_view()), name='members'),
    url(r'^resources/$', login_required(views.ResourcesView.as_view()), name='resources'),
    url(r'^events/$', login_required(views.EventsView.as_view()), name='events'),
    url(r'^jobs/$', login_required(views.JobsView.as_view()), name='jobs'),
    url(r'^jobs/create/$', login_required(views.JobsCreateView.as_view()), name='jobs-create'),
    url(r'^jobs/update/(?P<pk>\d+)/$', login_required(views.JobsUpdateView.as_view()), name='jobs-update'),
    url(r'^members/(?P<username>[\w.@+-]+)/$', login_required(views.profile), name='profile'),
    url(r'^status/$', login_required(views.StatusView.as_view()), name='status'),
    
    url(r'^post/create/$', views.post_create, name='post_create'),
    url(r'^post/comment/create/$', views.comment_create, name='comment_create'),

    url(r'^accounts/info/$', login_required(views.InfoView.as_view()), name='info'),
    url(r'^accounts/info/update/(?P<pk>\d+)/$', login_required(views.InfoUpdateView.as_view()), name='info-update'),

    url(r'^api/delete/post/(?P<post_id>[0-9]+)',
        login_required(views.delete_post),
        name='delete-post'),
    url(r'^api/delete/comment/(?P<comment_id>[0-9]+)',
        login_required(views.delete_comment),
        name='delete-comment'),
    url(r'^api/delete/job/(?P<job_id>[0-9]+)',
        login_required(views.delete_job),
        name='delete-job'),
]
