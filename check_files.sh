#!/bin/bash

echo "=== VÉRIFICATION DES FICHIERS DU PROJET ==="
echo ""

# Liste des fichiers essentiels
essential_files=(
    "config/settings.py"
    "config/urls.py"
    "apps/__init__.py"
    "apps/core/__init__.py"
    "apps/core/models.py"
    "apps/core/views.py"
    "apps/core/urls.py"
    "apps/renaloc/__init__.py"
    "apps/renaloc/models.py"
    "apps/renaloc/views.py"
    "apps/renaloc/urls.py"
    "apps/eftp_formel/__init__.py"
    "apps/eftp_formel/models.py"
    "apps/eftp_formel/views.py"
    "apps/eftp_formel/urls.py"
    "apps/eftp_non_formel/__init__.py"
    "apps/eftp_non_formel/models.py"
    "apps/eftp_non_formel/views.py"
    "apps/eftp_non_formel/urls.py"
    "manage.py"
    "requirements.txt"
)

echo "Fichiers essentiels :"
echo "--------------------"
for file in "${essential_files[@]}"; do
    if [ -f "$file" ]; then
        echo "✅ $file"
    else
        echo "❌ $file (MANQUANT)"
    fi
done

echo ""
echo "Dossiers de migrations :"
echo "----------------------"
migration_dirs=(
    "apps/core/migrations"
    "apps/renaloc/migrations"
    "apps/eftp_formel/migrations"
    "apps/eftp_non_formel/migrations"
)

for dir in "${migration_dirs[@]}"; do
    if [ -d "$dir" ]; then
        echo "✅ $dir/"
        if [ -f "$dir/__init__.py" ]; then
            echo "  ✅ $dir/__init__.py"
        else
            echo "  ❌ $dir/__init__.py (MANQUANT)"
        fi
    else
        echo "❌ $dir/ (MANQUANT)"
    fi
done

echo ""
echo "Templates :"
echo "----------"
template_dirs=(
    "apps/core/templates/core"
    "apps/core/templates/core/backup"
    "apps/renaloc/templates/renaloc"
    "apps/eftp_formel/templates/eftp_formel"
    "apps/eftp_non_formel/templates/eftp_non_formel"
)

for dir in "${template_dirs[@]}"; do
    if [ -d "$dir" ]; then
        echo "✅ $dir/"
    else
        echo "❌ $dir/ (MANQUANT)"
    fi
done

echo ""
echo "Fichiers statiques :"
echo "------------------"
static_dirs=(
    "static/css"
    "static/js"
    "static/images"
)

for dir in "${static_dirs[@]}"; do
    if [ -d "$dir" ]; then
        echo "✅ $dir/"
    else
        echo "❌ $dir/ (MANQUANT)"
    fi
done

echo ""
echo "=== FIN DE LA VÉRIFICATION ==="
