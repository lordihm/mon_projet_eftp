from django.urls import path
from . import views

app_name = 'eftp_formel'

urlpatterns = [
    path('etablissements/', views.etablissement_list, name='etablissement_list'),
    path('etablissements/create/', views.etablissement_create, name='etablissement_create'),
    path('etablissements/<int:pk>/', views.etablissement_detail, name='etablissement_detail'),
    path('etablissements/<int:pk>/edit/', views.etablissement_edit, name='etablissement_edit'),
    path('etablissements/<int:pk>/delete/', views.etablissement_delete, name='etablissement_delete'),
    path('import-export/', views.import_export, name='import_export'),
]