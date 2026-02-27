from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum, Count
from .models import EtablissementFormel, ApprenantFormel, FormateurFormel, FiliereFormel
from .forms import EtablissementFormelSimpleForm, EtablissementFormelCompletForm, ApprenantFormelForm, FormateurFormelForm, FiliereFormelForm
from apps.renaloc.models import Region

# ================ VUES POUR LES ÉTABLISSEMENTS ================

@login_required
def etablissement_list(request):
    """Liste des établissements formels"""
    etablissements = EtablissementFormel.objects.all().select_related('region', 'departement', 'commune')
    
    # Calcul des statistiques
    publics_count = etablissements.filter(statut='PUBLIC').count()
    prives_count = etablissements.filter(statut='PRIVE').count()
    
    # Récupérer tous les apprenants
    total_apprenants = 0
    
    # Pour les filtres
    regions = Region.objects.all()
    type_choices = EtablissementFormel.TYPE_ETABLISSEMENT_CHOICES
    
    context = {
        'etablissements': etablissements,
        'publics_count': publics_count,
        'prives_count': prives_count,
        'total_apprenants': total_apprenants,
        'regions': regions,
        'type_choices': type_choices,
    }
    return render(request, 'eftp_formel/etablissement_list.html', context)

@login_required
def etablissement_create(request):
    """Créer un nouvel établissement (formulaire simplifié)"""
    if request.method == 'POST':
        form = EtablissementFormelSimpleForm(request.POST)
        if form.is_valid():
            etablissement = form.save()
            messages.success(request, f"✅ Établissement {etablissement.nom} créé avec succès!")
            messages.info(request, "📝 Cliquez sur 'Saisie complète' pour renseigner toutes les données de l'établissement.")
            return redirect('eftp_formel:etablissement_detail', pk=etablissement.pk)
        else:
            messages.error(request, "❌ Veuillez corriger les erreurs ci-dessous.")
    else:
        form = EtablissementFormelSimpleForm()
    
    regions = Region.objects.all()
    context = {
        'form': form,
        'regions': regions,
        'is_simple_form': True,
        'titre': "Nouvel établissement - Informations de base"
    }
    return render(request, 'eftp_formel/etablissement_form_simple.html', context)

@login_required
def etablissement_detail(request, pk):
    """Détail d'un établissement"""
    etablissement = get_object_or_404(EtablissementFormel, pk=pk)
    
    # Statistiques
    total_apprenants = ApprenantFormel.objects.filter(etablissement=etablissement).aggregate(
        total=Sum('masculin') + Sum('feminin')
    )['total'] or 0
    
    apprenants_m = ApprenantFormel.objects.filter(etablissement=etablissement).aggregate(
        total=Sum('masculin')
    )['total'] or 0
    
    apprenants_f = ApprenantFormel.objects.filter(etablissement=etablissement).aggregate(
        total=Sum('feminin')
    )['total'] or 0
    
    total_formateurs = FormateurFormel.objects.filter(etablissement=etablissement).count()
    formateurs_m = FormateurFormel.objects.filter(etablissement=etablissement, sexe='M').count()
    formateurs_f = FormateurFormel.objects.filter(etablissement=etablissement, sexe='F').count()
    
    total_filieres = FiliereFormel.objects.filter(etablissement=etablissement).count()
    filieres = FiliereFormel.objects.filter(etablissement=etablissement)
    
    context = {
        'etablissement': etablissement,
        'total_apprenants': total_apprenants,
        'apprenants_m': apprenants_m,
        'apprenants_f': apprenants_f,
        'total_formateurs': total_formateurs,
        'formateurs_m': formateurs_m,
        'formateurs_f': formateurs_f,
        'total_filieres': total_filieres,
        'filieres': filieres,
    }
    return render(request, 'eftp_formel/etablissement_detail.html', context)

@login_required
def etablissement_edit(request, pk):
    """Modifier un établissement (formulaire complet)"""
    etablissement = get_object_or_404(EtablissementFormel, pk=pk)
    
    if request.method == 'POST':
        form = EtablissementFormelCompletForm(request.POST, instance=etablissement)
        if form.is_valid():
            form.save()
            messages.success(request, "Établissement modifié avec succès!")
            return redirect('eftp_formel:etablissement_detail', pk=etablissement.pk)
    else:
        form = EtablissementFormelCompletForm(instance=etablissement)
    
    context = {
        'form': form,
        'etablissement': etablissement,
        'titre': f"Modifier - {etablissement.nom}"
    }
    return render(request, 'eftp_formel/etablissement_form_complet.html', context)

@login_required
def etablissement_delete(request, pk):
    """Supprimer un établissement"""
    etablissement = get_object_or_404(EtablissementFormel, pk=pk)
    
    if request.method == 'POST':
        etablissement.delete()
        messages.success(request, "Établissement supprimé avec succès!")
        return redirect('eftp_formel:etablissement_list')
    
    return render(request, 'eftp_formel/etablissement_confirm_delete.html', {'etablissement': etablissement})

# ================ VUE CORRIGÉE POUR LA SAISIE COMPLÈTE ================

@login_required
def etablissement_complet(request, pk):
    """Tableau de bord complet de l'établissement avec tous les onglets"""
    etablissement = get_object_or_404(EtablissementFormel, pk=pk)
    
    # Récupérer les données associées
    apprenants = ApprenantFormel.objects.filter(etablissement=etablissement)
    formateurs = FormateurFormel.objects.filter(etablissement=etablissement)
    filieres = FiliereFormel.objects.filter(etablissement=etablissement)
    
    # Calculer les totaux
    total_apprenants = 0
    for app in apprenants:
        total_apprenants += (app.masculin or 0) + (app.feminin or 0)
    
    total_formateurs = formateurs.count()
    total_filieres = filieres.count()
    
    # Calculer la progression globale
    progression = 0
    champs_remplis = 0
    champs_total = 16  # Nombre total de sections/critères
    
    # Critères de progression
    if etablissement.nom: champs_remplis += 1
    if etablissement.sigle: champs_remplis += 1
    if etablissement.code: champs_remplis += 1
    if etablissement.statut: champs_remplis += 1
    if etablissement.zone: champs_remplis += 1
    if etablissement.region: champs_remplis += 1
    if etablissement.departement: champs_remplis += 1
    if etablissement.commune: champs_remplis += 1
    if etablissement.type_etablissement: champs_remplis += 1
    if etablissement.regime: champs_remplis += 1
    if etablissement.date_autorisation: champs_remplis += 1
    if etablissement.date_ouverture: champs_remplis += 1
    if etablissement.longitude and etablissement.latitude: champs_remplis += 1
    if apprenants.exists(): champs_remplis += 1
    if formateurs.exists(): champs_remplis += 1
    if filieres.exists(): champs_remplis += 1
    
    progression = int((champs_remplis / champs_total) * 100) if champs_total > 0 else 0
    
    context = {
        'etablissement': etablissement,
        'apprenants': apprenants,
        'formateurs': formateurs,
        'filieres': filieres,
        'total_apprenants': total_apprenants,
        'total_formateurs': total_formateurs,
        'total_filieres': total_filieres,
        'progression_globale': progression,
    }
    
    # IMPORTANT: Utiliser le template dashboard, pas le formulaire
    return render(request, 'eftp_formel/etablissement_dashboard.html', context)


# ================ VUES POUR LES APPRENANTS ================

@login_required
def apprenant_create(request, etablissement_id):
    """Ajouter des apprenants pour un établissement"""
    etablissement = get_object_or_404(EtablissementFormel, pk=etablissement_id)
    
    if request.method == 'POST':
        form = ApprenantFormelForm(request.POST)
        if form.is_valid():
            apprenant = form.save(commit=False)
            apprenant.etablissement = etablissement
            apprenant.save()
            messages.success(request, "✅ Apprenants ajoutés avec succès!")
            return redirect('eftp_formel:etablissement_complet', pk=etablissement.id)
        else:
            messages.error(request, "❌ Veuillez corriger les erreurs")
    else:
        form = ApprenantFormelForm()
    
    context = {
        'form': form,
        'etablissement': etablissement,
        'titre': f"Ajouter des apprenants - {etablissement.nom}"
    }
    return render(request, 'eftp_formel/apprenant_form.html', context)

@login_required
def apprenant_edit(request, pk):
    """Modifier des apprenants"""
    apprenant = get_object_or_404(ApprenantFormel, pk=pk)
    etablissement = apprenant.etablissement
    
    if request.method == 'POST':
        form = ApprenantFormelForm(request.POST, instance=apprenant)
        if form.is_valid():
            form.save()
            messages.success(request, "✅ Apprenants modifiés avec succès!")
            return redirect('eftp_formel:etablissement_complet', pk=etablissement.id)
    else:
        form = ApprenantFormelForm(instance=apprenant)
    
    context = {
        'form': form,
        'apprenant': apprenant,
        'etablissement': etablissement,
        'titre': f"Modifier les apprenants - {etablissement.nom}"
    }
    return render(request, 'eftp_formel/apprenant_form.html', context)

@login_required
def apprenant_delete(request, pk):
    """Supprimer des apprenants"""
    apprenant = get_object_or_404(ApprenantFormel, pk=pk)
    etablissement = apprenant.etablissement
    
    if request.method == 'POST':
        apprenant.delete()
        messages.success(request, "✅ Apprenants supprimés avec succès!")
        return redirect('eftp_formel:etablissement_complet', pk=etablissement.id)
    
    context = {
        'apprenant': apprenant,
        'etablissement': etablissement
    }
    return render(request, 'eftp_formel/apprenant_confirm_delete.html', context)


# ================ VUES POUR LES FORMATEURS ================

@login_required
def formateur_create(request, etablissement_id):
    """Ajouter un formateur pour un établissement"""
    etablissement = get_object_or_404(EtablissementFormel, pk=etablissement_id)
    
    if request.method == 'POST':
        form = FormateurFormelForm(request.POST)
        if form.is_valid():
            formateur = form.save(commit=False)
            formateur.etablissement = etablissement
            formateur.save()
            messages.success(request, "✅ Formateur ajouté avec succès!")
            return redirect('eftp_formel:etablissement_complet', pk=etablissement.id)
    else:
        form = FormateurFormelForm()
    
    context = {
        'form': form,
        'etablissement': etablissement,
        'titre': f"Ajouter un formateur - {etablissement.nom}"
    }
    return render(request, 'eftp_formel/formateur_form.html', context)

@login_required
def formateur_edit(request, pk):
    """Modifier un formateur"""
    formateur = get_object_or_404(FormateurFormel, pk=pk)
    etablissement = formateur.etablissement
    
    if request.method == 'POST':
        form = FormateurFormelForm(request.POST, instance=formateur)
        if form.is_valid():
            form.save()
            messages.success(request, "✅ Formateur modifié avec succès!")
            return redirect('eftp_formel:etablissement_complet', pk=etablissement.id)
    else:
        form = FormateurFormelForm(instance=formateur)
    
    context = {
        'form': form,
        'formateur': formateur,
        'etablissement': etablissement,
        'titre': f"Modifier le formateur - {etablissement.nom}"
    }
    return render(request, 'eftp_formel/formateur_form.html', context)

@login_required
def formateur_delete(request, pk):
    """Supprimer un formateur"""
    formateur = get_object_or_404(FormateurFormel, pk=pk)
    etablissement = formateur.etablissement
    
    if request.method == 'POST':
        formateur.delete()
        messages.success(request, "✅ Formateur supprimé avec succès!")
        return redirect('eftp_formel:etablissement_complet', pk=etablissement.id)
    
    context = {
        'formateur': formateur,
        'etablissement': etablissement
    }
    return render(request, 'eftp_formel/formateur_confirm_delete.html', context)


# ================ VUES POUR LES FILIÈRES ================

@login_required
def filiere_create(request, etablissement_id):
    """Ajouter une filière pour un établissement"""
    etablissement = get_object_or_404(EtablissementFormel, pk=etablissement_id)
    
    if request.method == 'POST':
        form = FiliereFormelForm(request.POST)
        if form.is_valid():
            filiere = form.save(commit=False)
            filiere.etablissement = etablissement
            filiere.save()
            messages.success(request, "✅ Filière ajoutée avec succès!")
            return redirect('eftp_formel:etablissement_complet', pk=etablissement.id)
    else:
        form = FiliereFormelForm()
    
    context = {
        'form': form,
        'etablissement': etablissement,
        'titre': f"Ajouter une filière - {etablissement.nom}"
    }
    return render(request, 'eftp_formel/filiere_form.html', context)

@login_required
def filiere_edit(request, pk):
    """Modifier une filière"""
    filiere = get_object_or_404(FiliereFormel, pk=pk)
    etablissement = filiere.etablissement
    
    if request.method == 'POST':
        form = FiliereFormelForm(request.POST, instance=filiere)
        if form.is_valid():
            form.save()
            messages.success(request, "✅ Filière modifiée avec succès!")
            return redirect('eftp_formel:etablissement_complet', pk=etablissement.id)
    else:
        form = FiliereFormelForm(instance=filiere)
    
    context = {
        'form': form,
        'filiere': filiere,
        'etablissement': etablissement,
        'titre': f"Modifier la filière - {etablissement.nom}"
    }
    return render(request, 'eftp_formel/filiere_form.html', context)

@login_required
def filiere_delete(request, pk):
    """Supprimer une filière"""
    filiere = get_object_or_404(FiliereFormel, pk=pk)
    etablissement = filiere.etablissement
    
    if request.method == 'POST':
        filiere.delete()
        messages.success(request, "✅ Filière supprimée avec succès!")
        return redirect('eftp_formel:etablissement_complet', pk=etablissement.id)
    
    context = {
        'filiere': filiere,
        'etablissement': etablissement
    }
    return render(request, 'eftp_formel/filiere_confirm_delete.html', context)


# ================ VUES POUR IMPORT/EXPORT ================

@login_required
def import_export(request):
    """Page d'import/export"""
    return render(request, 'eftp_formel/import_export.html')

@login_required
def import_data(request):
    """Importation des données depuis un fichier"""
    if request.method == 'POST' and request.FILES.get('file'):
        # Logique d'import à implémenter
        messages.success(request, "Import réussi (simulation)")
        return redirect('eftp_formel:import_export')
    
    messages.error(request, "Aucun fichier sélectionné")
    return redirect('eftp_formel:import_export')

@login_required
def export_data(request):
    """Exportation des données"""
    # Logique d'export à implémenter
    from django.http import HttpResponse
    return HttpResponse("Export en cours de développement")