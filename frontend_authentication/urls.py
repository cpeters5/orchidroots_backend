from django.urls import path
from . import views


urlpatterns = [
    path('login/', views.index ),
    path('forgetpassword/', views.index ),
    path('resetpassword/', views.index ),
    path('signup/', views.index ),
    path('verification/', views.index ),
    path('logout/', views.logout ),
]