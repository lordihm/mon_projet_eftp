#!/bin/bash

echo "=== VÉRIFICATION DES TEMPLATES ==="
echo ""

templates=(
    "apps/core/templates/core/base.html"
    "apps/core/templates/core/index.html"
    "apps/core/templates/core/login.html"
    "apps/core/templates/core/dashboard.html"
    "apps/core/templates/core/backup/list.html"
    "apps/core/templates/core/backup/create.html"
    "apps/core/templates/core/backup/settings.html"
    "apps/core/templates/core/backup/restore_confirm.html"
    "apps/core/templates/core/backup/delete_confirm.html"
    "apps/renaloc/templates/renaloc/import_export.html"
    "apps/eftp_formel/templates/eftp_formel/etablissement_list.html"
    "apps/eftp_non_formel/templates/eftp_non_formel/structure_list.html"
    "templates/base_generic.html"
)

for template in "${templates[@]}"; do
    if [ -f "$template" ]; then
        echo "✅ $template"
    else
        echo "❌ $template (MANQUANT)"
    fi
done

echo ""
echo "Dossiers de templates :"
echo "----------------------"
template_dirs=(
    "apps/core/templates/core"
    "apps/core/templates/core/backup"
    "apps/renaloc/templates/renaloc"
    "apps/eftp_formel/templates/eftp_formel"
    "apps/eftp_non_formel/templates/eftp_non_formel"
    "templates"
)

for dir in "${template_dirs[@]}"; do
    if [ -d "$dir" ]; then
        echo "✅ $dir/"
    else
        echo "❌ $dir/ (MANQUANT)"
    fi
done

echo ""
echo "=== FIN DE LA VÉRIFICATION ==="
