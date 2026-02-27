from django.urls import path
from . import views

app_name = 'eftp_formel'

urlpatterns = [
    # Établissements
    path('etablissements/', views.etablissement_list, name='etablissement_list'),
    path('etablissements/create/', views.etablissement_create, name='etablissement_create'),
    path('etablissements/<int:pk>/complet/', views.etablissement_complet, name='etablissement_complet'),
    path('etablissements/<int:pk>/', views.etablissement_detail, name='etablissement_detail'),
    path('etablissements/<int:pk>/edit/', views.etablissement_edit, name='etablissement_edit'),
    path('etablissements/<int:pk>/delete/', views.etablissement_delete, name='etablissement_delete'),
    
    # Import/Export
    path('import-export/', views.import_export, name='import_export'),
    path('import-data/', views.import_data, name='import_data'),
    path('export-data/', views.export_data, name='export_data'),
    
    # Apprenants
    path('apprenants/create/<int:etablissement_id>/', views.apprenant_create, name='apprenant_create'),
    path('apprenants/<int:pk>/edit/', views.apprenant_edit, name='apprenant_edit'),
    path('apprenants/<int:pk>/delete/', views.apprenant_delete, name='apprenant_delete'),
    
    # Formateurs
    path('formateurs/create/<int:etablissement_id>/', views.formateur_create, name='formateur_create'),
    path('formateurs/<int:pk>/edit/', views.formateur_edit, name='formateur_edit'),
    path('formateurs/<int:pk>/delete/', views.formateur_delete, name='formateur_delete'),
    
    # Filières
    path('filieres/create/<int:etablissement_id>/', views.filiere_create, name='filiere_create'),
    path('filieres/<int:pk>/edit/', views.filiere_edit, name='filiere_edit'),
    path('filieres/<int:pk>/delete/', views.filiere_delete, name='filiere_delete'),
]