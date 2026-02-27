from django.urls import path
from . import views

app_name = 'eftp_non_formel'

urlpatterns = [
    # Structures
    path('structures/', views.structure_list, name='structure_list'),
    path('structures/create/', views.structure_create, name='structure_create'),
    path('structures/<int:pk>/', views.structure_detail, name='structure_detail'),
    path('structures/<int:pk>/edit/', views.structure_edit, name='structure_edit'),
    path('structures/<int:pk>/delete/', views.structure_delete, name='structure_delete'),
    path('structures/<int:pk>/complet/', views.structure_complet, name='structure_complet'),
    path('structures/<int:pk>/json/', views.structure_complet_json, name='structure_complet_json'),
    
    # Maîtres artisans
    path('maitres/create/<int:structure_id>/', views.maitre_create, name='maitre_create'),
    path('maitres/<int:pk>/edit/', views.maitre_edit, name='maitre_edit'),
    path('maitres/<int:pk>/delete/', views.maitre_delete, name='maitre_delete'),
    
    # Apprentis
    path('apprentis/create/<int:structure_id>/', views.apprenti_create, name='apprenti_create'),
    path('apprentis/<int:pk>/edit/', views.apprenti_edit, name='apprenti_edit'),
    path('apprentis/<int:pk>/delete/', views.apprenti_delete, name='apprenti_delete'),
    
    # Métiers
    path('metiers/create/<int:structure_id>/', views.metier_create, name='metier_create'),
    path('metiers/<int:pk>/edit/', views.metier_edit, name='metier_edit'),
    path('metiers/<int:pk>/delete/', views.metier_delete, name='metier_delete'),
    
    # Import/Export
    path('import-export/', views.import_export, name='import_export'),
]