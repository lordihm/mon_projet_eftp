from django.urls import path
from . import views

app_name = 'renaloc'

urlpatterns = [
    path('import-export/', views.import_export, name='import_export'),
    path('export-data/', views.export_data, name='export_data'),
    
    # URLs pour l'admin
    path('admin-stats/', views.admin_stats, name='admin_stats'),
    path('get-communes/', views.get_communes, name='get_communes'),
    path('search/', views.search_locations, name='search_locations'),

    # Nouvelles URLs pour les départements et quartiers
    path('get-departements/', views.get_departements, name='get_departements'),
    path('get-quartiers/', views.get_quartiers, name='get_quartiers'),
]