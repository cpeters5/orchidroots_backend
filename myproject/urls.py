"""myproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from django.conf.urls import url
from django.contrib.auth.views import LogoutView
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.generic import TemplateView
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from myproject.views import orchid_home, home, private_home

urlpatterns = [
    # path('', TemplateView.as_view(template_name="index.html")),
    path('admin/', admin.site.urls),

    path('', orchid_home, name='orchid_home'),
    path('', include('frontend_authentication.urls')),
    # path('home/', orchid_home, name='orchid_home'),

    # Future migrations
    # path('search/', include('search.urls')),
    # path('orchidlist/', include('orchidlist.urls')),
    # path('detail/', include('detail.urls')),
    # path('documents/', include('documents.urls')),
    # path('donation/', include('donation.urls')),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns +=  url(r'^api/v1/', include('api.urls'), name='apis'),
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += staticfiles_urlpatterns()
