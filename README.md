# 🇳🇪 Projet EFTP - Recensement 2025-2026

Application Django pour la gestion des données des établissements d'enseignement et de formation techniques et professionnels (EFTP) du Niger.

## ✨ Fonctionnalités

- 🏫 **Gestion des établissements EFTP formels**
- 🔧 **Gestion des structures EFTP non formelles**
- 🗺️ **Intégration Renaloc** (localités du Niger : régions, départements, communes)
- 💾 **Système de sauvegarde avancé** (manuel, automatique, programmé)
- 📊 **Import/Export** Excel, CSV, JSON
- 📱 **Interface responsive** avec Bootstrap 5
- 🔐 **Authentification et gestion des utilisateurs**

## 🚀 Installation rapide

```bash
# Cloner le dépôt
git clone https://github.com/votre_nom/mon_projet_eftp.git
cd mon_projet_eftp

# Créer l'environnement virtuel
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou venv\Scripts\activate  # Windows

# Installer les dépendances
pip install -r requirements.txt

# Créer la base de données
python manage.py migrate

# Créer un superutilisateur
python manage.py createsuperuser

# Démarrer le serveur
python manage.py runserver

📁 Structure du projet
text

mon_projet_eftp/
├── apps/
│   ├── core/           # Fonctionnalités de base
│   ├── renaloc/        # Gestion des localités
│   ├── eftp_formel/    # EFTP formel
│   └── eftp_non_formel/# EFTP non formel
├── config/             # Configuration Django
├── templates/          # Templates globaux
├── static/            # Fichiers statiques
├── manage.py
└── requirements.txt

🛠️ Technologies utilisées

    Backend : Django 4.2

    Frontend : Bootstrap 5, Font Awesome

    Base de données : SQLite (développement), PostgreSQL (production)

    Import/Export : pandas, openpyxl

📝 Licence

MIT
👥 Auteur

[IDE HALIDOU MOUHAMADOUL-KAIROU]
lordihm@gmail.com
lordihm@yahoo.fr
Direction des Statistiques et de la Digitalisation - 
Ministère de l'Enseignement et la Formation Techniques et Professionnels
NIAMEY, NIGER

