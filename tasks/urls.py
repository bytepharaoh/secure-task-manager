from django.urls import path
from . import views
urlpatterns=[
    path('', views.index , name='home'),
    path('create/' , views.create_task_form , name='create_task'),
    path('create/submit/' , views.create_task , name='create_task_submit'),
    path ('edit/<int:pk>/' , views.edit_task , name='edit_task'),
    path('delete/<int:pk>/' , views.delete_task , name='delete_task'),
    path('toggle/<int:pk>/', views.toggle_complete , name='toggle_complete'),
    
    ]
