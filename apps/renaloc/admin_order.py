"""
Ce fichier permet de réorganiser l'ordre des modèles dans l'administration
"""
from django.contrib import admin
from django.apps import apps

# Ordre souhaité pour les modèles de Renaloc
MODEL_ORDER = [
    'region',
    'departement',
    'commune',
    'quartiervillage',
]

def get_app_list(self, request):
    """Réorganise la liste des applications dans l'admin"""
    app_dict = self._build_app_dict(request)
    app_list = []
    
    for app_label in ['renaloc']:  # Seulement pour notre application
        if app_label in app_dict:
            app = app_dict[app_label]
            # Réorganiser les modèles selon MODEL_ORDER
            models = {m['object_name'].lower(): m for m in app['models']}
            app['models'] = [models[name] for name in MODEL_ORDER if name in models]
            app_list.append(app)
    
    # Ajouter les autres applications normalement
    for app_label, app in app_dict.items():
        if app_label not in ['renaloc']:
            app_list.append(app)
    
    return app_list

# Remplacer la méthode par défaut
admin.AdminSite.get_app_list = get_app_list