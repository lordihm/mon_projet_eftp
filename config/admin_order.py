# config/admin_order.py
"""
Configuration de l'ordre des applications et modèles dans l'administration Django
"""

import logging
logger = logging.getLogger(__name__)

# Ordre souhaité pour les modèles de Renaloc
RENALOC_MODEL_ORDER = ['region', 'departement', 'commune', 'quartiervillage']

# Ordre prioritaire des applications
APP_ORDER = ['eftp_formel', 'eftp_non_formel','renaloc','core']

def customize_admin_order():
    """
    Personnalise l'ordre d'affichage dans l'administration Django
    """
    from django.contrib import admin
    
    original_get_app_list = admin.AdminSite.get_app_list
    
    def get_app_list(self, request):
        """
        Version personnalisée de get_app_list
        """
        # Obtenir la liste originale
        app_list = original_get_app_list(self, request)
        
        # Réorganiser les applications
        ordered_app_list = []
        
        # D'abord, placer les applications prioritaires dans l'ordre souhaité
        for app_label in APP_ORDER:
            for app in app_list:
                if app['app_label'] == app_label:
                    # Réorganiser les modèles pour renaloc
                    if app_label == 'renaloc':
                        models_by_name = {m['object_name'].lower(): m for m in app['models']}
                        ordered_models = []
                        
                        for model_name in RENALOC_MODEL_ORDER:
                            if model_name in models_by_name:
                                ordered_models.append(models_by_name[model_name])
                        
                        # Ajouter les modèles non listés
                        for model_name, model in models_by_name.items():
                            if model_name not in RENALOC_MODEL_ORDER:
                                ordered_models.append(model)
                        
                        app['models'] = ordered_models
                    
                    ordered_app_list.append(app)
                    break
        
        # Ajouter les applications restantes
        for app in app_list:
            if app['app_label'] not in APP_ORDER:
                ordered_app_list.append(app)
        
        logger.debug(f"Admin réorganisé avec {len(ordered_app_list)} applications")
        return ordered_app_list
    
    # Remplacer la méthode
    admin.AdminSite.get_app_list = get_app_list
    logger.info("✅ Administration personnalisée avec succès")