from django.urls import path
from . import views

app_name = 'portfolio'

urlpatterns = [
    path('', views.about_contact_view, name='about_contact'),
    path('services/', views.services_view, name='services'),
    path('projects/', views.projects_view, name='projects'),
    path('projects/<slug:slug>/', views.project_detail_view, name='project_detail'),
]