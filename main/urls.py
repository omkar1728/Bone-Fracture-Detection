from django.urls import path
from . import views

urlpatterns = [
    #path('', views.mainHome, name='mainHome'),
    path('', views.main_upload, name='mainHome'),
    path('services', views.services, name='services'),
    path('Home', views.Home, name='home'),
    path('about', views.aboutus, name='about'),
    path('upload', views.main_upload, name='upload'),
    path('prediction', views.predict, name='prediction'),


]