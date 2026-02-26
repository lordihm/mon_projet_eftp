from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'core'

urlpatterns = [
    # Pages principales
    path('', views.index, name='index'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    
    # URLs des sauvegardes
    path('backups/', views.backup_list, name='backup_list'),
    path('backups/create/', views.backup_create, name='backup_create'),
    path('backups/<int:backup_id>/download/', views.backup_download, name='backup_download'),
    path('backups/<int:backup_id>/restore/', views.backup_restore, name='backup_restore'),
    path('backups/<int:backup_id>/delete/', views.backup_delete, name='backup_delete'),
    path('backups/settings/', views.backup_settings, name='backup_settings'),
]

