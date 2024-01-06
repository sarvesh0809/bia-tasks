from django.urls import path
from .import views

urlpatterns = [
    
    path('', views.task, name='task'),
    path('task1/', views.task1, name='task1'),
    path('task3/', views.Task3.as_view(), name='task3'),
    path('task4/', views.Task4.as_view(), name='task4'),
    path('task5/', views.Task5.as_view(), name='task5'),
]