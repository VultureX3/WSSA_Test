from django.conf.urls import url
from django.contrib.auth.views import LoginView, LogoutView
from .views import *
from .forms import BootstrapAuthenticationForm

urlpatterns = [
    url(r'^$', home, name='home'),
    url(r'^contact/$', contact, name='contact'),
    url(r'^about/$', about, name='about'),
    url(r'^test/$', test, name='test'),
    url(r'^login/$',
        LoginView.as_view(
            authentication_form=BootstrapAuthenticationForm,
            template_name='login.html',
            extra_context=
            {
                'title': 'Log in',
            }
        ),
        name='login'),
    url(r'^logout$', LogoutView.as_view(), name='logout'),
    url(r'^signup/$', signup, name='signup'),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
    ]