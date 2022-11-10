from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('logout', views.logoutUser, name='logout'),
    path('register', views.register_view, name='register'),
    path('profile', views.profile, name='profile'),
]
