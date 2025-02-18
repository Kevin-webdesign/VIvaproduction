from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('survey/', views.survey, name='survey'),
    path('dashboard/', views.adminIndex, name='dashboard'),
    path('surveyDetails/', views.surveyDetails, name='surveys'),
    path('register/', views.registration, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('analysis/', views.analysis, name='analysis'),
    path('gender/', views.gender, name='gender'),  
    path('region/', views.region, name='region'),
    path('purchase_location/', views.purchase, name='purchase_location'),
   path('source', views.source, name='source'),
   path('mattpye', views.mattype, name='mattype'),
   path('age', views.age, name='age'),
   path('statistic', views.gender_statistics, name='statistic')
]