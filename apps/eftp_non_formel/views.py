from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib import messages
from django.db.models import Sum, Count
from django.http import JsonResponse
from .models import StructureNonFormelle, MaitreArtisan, ApprentiNonFormel, MetierNonFormel
from .forms import (
    StructureNonFormelleSimpleForm, StructureNonFormelleCompletForm,
    MaitreArtisanForm, ApprentiNonFormelForm, MetierNonFormelForm
)
from apps.renaloc.models import Region

# ================ VUES POUR LES STRUCTURES ================

@login_required
def structure_list(request):
    """Liste des structures non formelles"""
    structures = StructureNonFormelle.objects.all().select_related('region', 'departement', 'commune')
    
    # Calcul des statistiques
    publiques_count = structures.filter(statut='PUBLIC').count()
    privees_count = structures.filter(statut='PRIVE').count()
    
    # Pour les filtres
    regions = Region.objects.all()
    type_choices = StructureNonFormelle.TYPE_STRUCTURE_CHOICES
    
    context = {
        'structures': structures,
        'publiques_count': publiques_count,
        'privees_count': privees_count,
        'regions': regions,
        'type_choices': type_choices,
    }
    return render(request, 'eftp_non_formel/structure_list.html', context)


@login_required
def structure_create(request):
    """Créer une nouvelle structure (formulaire simplifié)"""
    if request.method == 'POST':
        form = StructureNonFormelleSimpleForm(request.POST)
        if form.is_valid():
            structure = form.save()
            messages.success(request, f"✅ Structure {structure.nom} créée avec succès!")
            messages.info(request, "📝 Cliquez sur 'Saisie complète' pour renseigner toutes les données.")
            return redirect('eftp_non_formel:structure_detail', pk=structure.pk)
        else:
            messages.error(request, "❌ Veuillez corriger les erreurs ci-dessous.")
    else:
        form = StructureNonFormelleSimpleForm()
    
    regions = Region.objects.all()
    context = {
        'form': form,
        'regions': regions,
        'titre': "Nouvelle structure - Informations de base"
    }
    return render(request, 'eftp_non_formel/structure_form_simple.html', context)


@login_required
def structure_detail(request, pk):
    """Détail d'une structure"""
    structure = get_object_or_404(StructureNonFormelle, pk=pk)
    
    # Statistiques
    total_apprentis = ApprentiNonFormel.objects.filter(structure=structure).aggregate(
        total=Sum('masculin') + Sum('feminin')
    )['total'] or 0
    
    total_maitres = MaitreArtisan.objects.filter(structure=structure).count()
    total_metiers = MetierNonFormel.objects.filter(structure=structure).count()
    
    context = {
        'structure': structure,
        'total_apprentis': total_apprentis,
        'total_maitres': total_maitres,
        'total_metiers': total_metiers,
    }
    return render(request, 'eftp_non_formel/structure_detail.html', context)


@login_required
def structure_edit(request, pk):
    """Modifier une structure (informations de base)"""
    structure = get_object_or_404(StructureNonFormelle, pk=pk)
    
    if request.method == 'POST':
        form = StructureNonFormelleSimpleForm(request.POST, instance=structure)
        if form.is_valid():
            form.save()
            messages.success(request, "✅ Structure modifiée avec succès!")
            return redirect('eftp_non_formel:structure_detail', pk=structure.pk)
    else:
        form = StructureNonFormelleSimpleForm(instance=structure)
    
    context = {
        'form': form,
        'structure': structure,
        'titre': f"Modifier - {structure.nom}"
    }
    return render(request, 'eftp_non_formel/structure_form_simple.html', context)


@login_required
def structure_delete(request, pk):
    """Supprimer une structure"""
    structure = get_object_or_404(StructureNonFormelle, pk=pk)
    
    if request.method == 'POST':
        structure.delete()
        messages.success(request, "✅ Structure supprimée avec succès!")
        return redirect('eftp_non_formel:structure_list')
    
    return render(request, 'eftp_non_formel/structure_confirm_delete.html', {'structure': structure})


@login_required
def structure_complet(request, pk):
    """Tableau de bord complet de la structure avec tous les onglets"""
    structure = get_object_or_404(StructureNonFormelle, pk=pk)
    
    # Récupérer les données associées
    apprentis = ApprentiNonFormel.objects.filter(structure=structure)
    maitres = MaitreArtisan.objects.filter(structure=structure)
    metiers = MetierNonFormel.objects.filter(structure=structure)
    
    # Calculer les totaux correctement
    total_apprentis = 0
    for app in apprentis:
        total_apprentis += (app.masculin or 0) + (app.feminin or 0)
    
    # Alternative avec agrégation (plus performant)
    from django.db.models import Sum
    total_apprentis_agg = apprentis.aggregate(
        total=Sum('masculin') + Sum('feminin')
    )['total'] or 0
    
    # Utiliser la valeur agrégée pour être sûr
    total_apprentis = total_apprentis_agg
    
    total_maitres = maitres.count()
    total_metiers = metiers.count()
    
    # Calculer le total des apprentis par métier (optionnel)
    total_apprentis_metiers = 0
    for metier in metiers:
        total_apprentis_metiers += metier.total_apprentis()
    
    # Progression
    progression = structure.get_completion_percentage()
    
    context = {
        'structure': structure,
        'apprentis': apprentis,
        'maitres': maitres,
        'metiers': metiers,
        'total_apprentis': total_apprentis,
        'total_apprentis_metiers': total_apprentis_metiers,
        'total_maitres': total_maitres,
        'total_metiers': total_metiers,
        'progression_globale': progression,
    }
    
    return render(request, 'eftp_non_formel/structure_dashboard.html', context)

# ================ VUES POUR LES MAÎTRES ARTISANS ================

@login_required
def maitre_create(request, structure_id):
    """Ajouter un maître artisan à une structure"""
    structure = get_object_or_404(StructureNonFormelle, pk=structure_id)
    
    if request.method == 'POST':
        form = MaitreArtisanForm(request.POST)
        if form.is_valid():
            maitre = form.save(commit=False)
            maitre.structure = structure
            maitre.save()
            messages.success(request, "✅ Maître artisan ajouté avec succès!")
            return redirect('eftp_non_formel:structure_complet', pk=structure.id)
    else:
        form = MaitreArtisanForm()
    
    context = {
        'form': form,
        'structure': structure,
        'titre': f"Ajouter un maître artisan - {structure.nom}"
    }
    return render(request, 'eftp_non_formel/maitre_form.html', context)


@login_required
def maitre_edit(request, pk):
    """Modifier un maître artisan"""
    maitre = get_object_or_404(MaitreArtisan, pk=pk)
    structure = maitre.structure
    
    if request.method == 'POST':
        form = MaitreArtisanForm(request.POST, instance=maitre)
        if form.is_valid():
            form.save()
            messages.success(request, "✅ Maître artisan modifié avec succès!")
            return redirect('eftp_non_formel:structure_complet', pk=structure.id)
    else:
        form = MaitreArtisanForm(instance=maitre)
    
    context = {
        'form': form,
        'maitre': maitre,
        'structure': structure,
        'titre': f"Modifier le maître artisan - {structure.nom}"
    }
    return render(request, 'eftp_non_formel/maitre_form.html', context)


@login_required
def maitre_delete(request, pk):
    """Supprimer un maître artisan"""
    maitre = get_object_or_404(MaitreArtisan, pk=pk)
    structure = maitre.structure
    
    if request.method == 'POST':
        maitre.delete()
        messages.success(request, "✅ Maître artisan supprimé avec succès!")
        return redirect('eftp_non_formel:structure_complet', pk=structure.id)
    
    context = {
        'maitre': maitre,
        'structure': structure
    }
    return render(request, 'eftp_non_formel/maitre_confirm_delete.html', context)


# ================ VUES POUR LES APPRENTIS ================

@login_required
def apprenti_create(request, structure_id):
    """Ajouter des apprentis à une structure"""
    structure = get_object_or_404(StructureNonFormelle, pk=structure_id)
    
    if request.method == 'POST':
        form = ApprentiNonFormelForm(request.POST)
        if form.is_valid():
            apprenti = form.save(commit=False)
            apprenti.structure = structure
            apprenti.save()
            messages.success(request, "✅ Apprentis ajoutés avec succès!")
            return redirect('eftp_non_formel:structure_complet', pk=structure.id)
        else:
            messages.error(request, "❌ Veuillez corriger les erreurs")
    else:
        form = ApprentiNonFormelForm()
    
    context = {
        'form': form,
        'structure': structure,
        'titre': f"Ajouter des apprentis - {structure.nom}"
    }
    return render(request, 'eftp_non_formel/apprenti_form.html', context)

@login_required
def apprenti_edit(request, pk):
    """Modifier des apprentis"""
    apprenti = get_object_or_404(ApprentiNonFormel, pk=pk)
    structure = apprenti.structure
    
    if request.method == 'POST':
        form = ApprentiNonFormelForm(request.POST, instance=apprenti)
        if form.is_valid():
            form.save()
            messages.success(request, "✅ Apprentis modifiés avec succès!")
            return redirect('eftp_non_formel:structure_complet', pk=structure.id)
        else:
            messages.error(request, "❌ Veuillez corriger les erreurs")
    else:
        form = ApprentiNonFormelForm(instance=apprenti)
    
    context = {
        'form': form,
        'apprenti': apprenti,
        'structure': structure,
        'titre': f"Modifier les apprentis - {structure.nom}"
    }
    return render(request, 'eftp_non_formel/apprenti_form.html', context)

@login_required
def apprenti_delete(request, pk):
    """Supprimer des apprentis"""
    apprenti = get_object_or_404(ApprentiNonFormel, pk=pk)
    structure = apprenti.structure
    
    if request.method == 'POST':
        apprenti.delete()
        messages.success(request, "✅ Apprentis supprimés avec succès!")
        return redirect('eftp_non_formel:structure_complet', pk=structure.id)
    
    context = {
        'apprenti': apprenti,
        'structure': structure
    }
    return render(request, 'eftp_non_formel/apprenti_confirm_delete.html', context)

# ================ VUES POUR LES MÉTIERS ================

@login_required
def metier_create(request, structure_id):
    """Ajouter un métier à une structure"""
    structure = get_object_or_404(StructureNonFormelle, pk=structure_id)
    
    if request.method == 'POST':
        form = MetierNonFormelForm(request.POST)
        if form.is_valid():
            metier = form.save(commit=False)
            metier.structure = structure
            metier.save()
            messages.success(request, "✅ Métier ajouté avec succès!")
            return redirect('eftp_non_formel:structure_complet', pk=structure.id)
    else:
        form = MetierNonFormelForm()
    
    context = {
        'form': form,
        'structure': structure,
        'titre': f"Ajouter un métier - {structure.nom}"
    }
    return render(request, 'eftp_non_formel/metier_form.html', context)


@login_required
def metier_edit(request, pk):
    """Modifier un métier"""
    metier = get_object_or_404(MetierNonFormel, pk=pk)
    structure = metier.structure
    
    if request.method == 'POST':
        form = MetierNonFormelForm(request.POST, instance=metier)
        if form.is_valid():
            form.save()
            messages.success(request, "✅ Métier modifié avec succès!")
            return redirect('eftp_non_formel:structure_complet', pk=structure.id)
    else:
        form = MetierNonFormelForm(instance=metier)
    
    context = {
        'form': form,
        'metier': metier,
        'structure': structure,
        'titre': f"Modifier le métier - {structure.nom}"
    }
    return render(request, 'eftp_non_formel/metier_form.html', context)


@login_required
def metier_delete(request, pk):
    """Supprimer un métier"""
    metier = get_object_or_404(MetierNonFormel, pk=pk)
    structure = metier.structure
    
    if request.method == 'POST':
        metier.delete()
        messages.success(request, "✅ Métier supprimé avec succès!")
        return redirect('eftp_non_formel:structure_complet', pk=structure.id)
    
    context = {
        'metier': metier,
        'structure': structure
    }
    return render(request, 'eftp_non_formel/metier_confirm_delete.html', context)


# ================ VUES POUR IMPORT/EXPORT ================

@login_required
def import_export(request):
    """Page d'import/export"""
    return render(request, 'eftp_non_formel/import_export.html')

@login_required
def structure_complet_json(request, pk):
    """Version JSON du tableau de bord pour les mises à jour AJAX"""
    try:
        structure = get_object_or_404(StructureNonFormelle, pk=pk)
        
        # Récupérer les données
        apprentis = ApprentiNonFormel.objects.filter(structure=structure)
        maitres = MaitreArtisan.objects.filter(structure=structure)
        metiers = MetierNonFormel.objects.filter(structure=structure)
        
        # Calculer les totaux
        total_apprentis = apprentis.aggregate(
            total=Sum('masculin') + Sum('feminin')
        )['total'] or 0
        
        # Compter les entités
        apprentis_count = apprentis.count()
        maitres_count = maitres.count()
        metiers_count = metiers.count()
        
        # Calculer les totaux par secteur (optionnel)
        secteurs_data = {}
        for secteur_code, secteur_label in ApprentiNonFormel.SECTEUR_CHOICES:
            secteur_apprentis = apprentis.filter(secteur=secteur_code)
            total = secteur_apprentis.aggregate(
                total=Sum('masculin') + Sum('feminin')
            )['total'] or 0
            if total > 0:
                secteurs_data[secteur_label] = total
        
        data = {
            'success': True,
            'structure_id': structure.id,
            'structure_nom': structure.nom,
            'total_apprentis': total_apprentis,
            'apprentis_count': apprentis_count,
            'maitres_count': maitres_count,
            'metiers_count': metiers_count,
            'secteurs': secteurs_data,
            'timestamp': str(timezone.now()),
        }
        
        return JsonResponse(data)
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)

