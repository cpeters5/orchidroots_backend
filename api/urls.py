from django.urls import include, path, re_path
from django.conf.urls import url


urlpatterns = [
    path('accounts/', include('accounts.urls')),

]