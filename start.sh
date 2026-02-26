#!/bin/bash

# Script de démarrage du projet EFTP
echo "🚀 Démarrage du projet EFTP"

# Vérifier si venv est activé
if [[ -z "${VIRTUAL_ENV}" ]]; then
    echo "🔧 Activation de l'environnement virtuel..."
    source venv/bin/activate
    if [ $? -ne 0 ]; then
        echo "❌ Erreur : Impossible d'activer l'environnement virtuel"
        exit 1
    fi
    echo "✅ Environnement virtuel activé"
fi

# Vérifier les dépendances
echo "📦 Vérification des dépendances..."
python -c "import decouple" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "❌ decouple manquant, installation..."
    pip install python-decouple
fi

# Démarrer le serveur
echo "🌐 Démarrage du serveur Django..."
python manage.py runserver

# En cas d'arrêt
echo "👋 Serveur arrêté"