from django.urls import path
from . import views

urlpatterns = [
    # Authentication URLs
    path('signup/', views.SignupView.as_view(), name='signup'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    
    # Task URLs
    path('', views.TaskListView.as_view(), name='task_list'),
    path('create/', views.TaskCreateView.as_view(), name='task_create'),
    path('update/<int:pk>/', views.TaskUpdateView.as_view(), name='task_update'),
    path('delete/<int:pk>/', views.TaskDeleteView.as_view(), name='task_delete'),
    path('toggle/<int:pk>/', views.TaskToggleView.as_view(), name='task_toggle'),
]

