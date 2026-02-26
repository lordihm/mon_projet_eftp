from django.urls import path
from . import views

app_name = 'eftp_non_formel'

urlpatterns = [
    path('structures/', views.structure_list, name='structure_list'),
    path('structures/create/', views.structure_create, name='structure_create'),
    path('structures/<int:pk>/', views.structure_detail, name='structure_detail'),
    path('structures/<int:pk>/edit/', views.structure_edit, name='structure_edit'),
    path('structures/<int:pk>/delete/', views.structure_delete, name='structure_delete'),
    path('import-export/', views.import_export, name='import_export'),
]