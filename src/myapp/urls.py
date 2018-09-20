from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views

from . import views

app_name = 'app'
urlpatterns = [
    url(r'^project/(?P<slug>[^\.]+)/$', login_required(views.DetailView.as_view()), name='detail'),
    url(r'^seed/(?P<slug>[^\.]+)/$', login_required(views.SeedView.as_view()), name='seed'),
    url(r'^home/$', login_required(views.HomeView.as_view()), name='home'),
    url(r'^accounts/login/$', auth_views.login, name='login', kwargs={'redirect_authenticated_user': True}),
    url(r'^accounts/logout/$', auth_views.logout, name='logout'),
    url(r'^register/$', login_required(views.RegisterView.as_view()), name='register'),
]