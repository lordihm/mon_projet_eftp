for app in core renaloc eftp_formel eftp_non_formel; do
    echo "Vérification de apps/$app/urls.py"
    if [ -f "apps/$app/urls.py" ]; then
        echo "OK - apps/$app/urls.py existe"
    else
        echo "ERREUR - apps/$app/urls.py manquant"
    fi
done