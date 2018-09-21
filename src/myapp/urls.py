from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views

from . import views

app_name = 'app'
urlpatterns = [
    url(r'^project/(?P<slug>[^\.]+)/$', login_required(views.DetailView.as_view()), name='detail'),
    url(r'^seed/(?P<slug>[^\.]+)/$', login_required(views.SeedView.as_view()), name='seed'),
    url(r'^seed-launch/(?P<slug>[^\.]+)/$', login_required(views.SeedLaunchView.as_view()), name='seed-launch'),
    url(r'^launch/(?P<slug>[^\.]+)/$', login_required(views.LaunchView.as_view()), name='launch'),
    url(r'^home/$', login_required(views.HomeView.as_view()), name='home'),
    url(r'^accounts/login/$', auth_views.login, name='login', kwargs={'redirect_authenticated_user': True}),
    url(r'^accounts/logout/$', auth_views.logout, name='logout'),
    url(r'^accounts/info/$', login_required(views.InfoView.as_view()), name='info'),
    url(r'^learn/$', login_required(views.learn), name='learn'),
    url(r'^faq/$', login_required(views.FaqView.as_view()), name='faq'),
]