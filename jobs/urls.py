from django.urls import path
from . import views

urlpatterns = [
    # job listings & details
    path('', views.job_list, name='job_list'),
    path('<int:job_id>/', views.job_detail, name='job_detail'),

    # create job (employer)
    path('create/', views.create_job, name='create_job'),
    path('employer/jobs/', views.employer_job_posts, name='employer_job_posts'),

    # apply job (candidate)
    path('apply/<int:job_id>/', views.apply_job, name='apply_job'),
    path('candidate/applications/', views.my_applications, name='my_applications'),
    
    path('applications/<int:job_id>/', views.view_applications, name='view_applications'),

]
