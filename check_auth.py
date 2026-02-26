#!/usr/bin/env python
"""
Script pour vérifier la configuration d'authentification
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.urls import reverse, resolve
from django.conf import settings

def check_auth_config():
    """Vérifie la configuration d'authentification"""
    print("\n🔍 Vérification de la configuration d'authentification...\n")
    
    # Vérifier les URLs
    try:
        login_url = reverse('login')
        print(f"✅ URL de connexion : {login_url}")
    except:
        print("❌ URL 'login' non trouvée")
    
    try:
        logout_url = reverse('logout')
        print(f"✅ URL de déconnexion : {logout_url}")
    except:
        print("❌ URL 'logout' non trouvée")
    
    try:
        dashboard_url = reverse('core:dashboard')
        print(f"✅ URL du tableau de bord : {dashboard_url}")
    except:
        print("❌ URL 'core:dashboard' non trouvée")
    
    # Vérifier les paramètres
    print(f"\n📋 Paramètres d'authentification :")
    print(f"   LOGIN_URL : {settings.LOGIN_URL}")
    print(f"   LOGIN_REDIRECT_URL : {settings.LOGIN_REDIRECT_URL}")
    print(f"   LOGOUT_REDIRECT_URL : {settings.LOGOUT_REDIRECT_URL}")
    
    print("\n✅ Vérification terminée")

if __name__ == '__main__':
    check_auth_config()
