from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_user, name='login'),  # default route
    path('register/', views.register, name='register'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),

    # dashboards
    path('dashboard/', views.dashboard, name='dashboard'),
    path('employer/dashboard/', views.employer_dashboard, name='employer_dashboard'),
    path('candidate/dashboard/', views.candidate_dashboard, name='candidate_dashboard'),
]
