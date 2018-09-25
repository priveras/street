from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views

from . import views

app_name = 'app'
urlpatterns = [
    url(r'^$', login_required(views.index), name='index'),
    url(r'^project/(?P<slug>[^\.]+)/$', login_required(views.DetailView.as_view()), name='detail'),
    url(r'^seed/(?P<slug>[^\.]+)/$', login_required(views.SeedView.as_view()), name='seed'),
    url(r'^seed-launch/(?P<slug>[^\.]+)/$', login_required(views.SeedLaunchView.as_view()), name='seed-launch'),
    url(r'^launch/(?P<slug>[^\.]+)/$', login_required(views.LaunchView.as_view()), name='launch'),
    url(r'^projects/$', login_required(views.HomeView.as_view()), name='home'),
    url(r'^accounts/info/$', login_required(views.InfoView.as_view()), name='info'),
    url(r'^learn/$', login_required(views.learn), name='learn'),
    url(r'^faq/$', login_required(views.FaqView.as_view()), name='faq'),

    url(r'^api/project/form$',
        login_required(views.project_form),
        name='project-form'),
    url(r'^api/project/form/(?P<id>[0-9]+)$',
        login_required(views.project_form),
        name='project-form'),

    url(r'^tutorial/$', login_required(views.TutorialView.as_view()), name='tutorial'),

    url(r'^api/model/form/(?P<name>[^\.]+)/project/(?P<project_id>[0-9]+)/id/(?P<id>[0-9]+)$',
        login_required(views.model_form),
        name='model-form'),
    url(r'^api/model/form/(?P<name>[^\.]+)/project/(?P<project_id>[0-9]+)$',
        login_required(views.model_form),
        name='model-form-id'),

    url(r'^api/comment',
        login_required(views.comment_save),
        name='comment-save'),
]
