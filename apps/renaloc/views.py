from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Count
from .models import Region, Departement, Commune, QuartierVillage

@login_required
def import_export(request):
    return render(request, 'renaloc/import_export.html')

@login_required
def export_data(request):
    # Logique d'export à implémenter
    from django.http import HttpResponse
    return HttpResponse("Export en cours de développement")


@staff_member_required
def admin_stats(request):
    """Vue pour les statistiques en temps réel dans l'admin"""
    stats = {
        'regions': Region.objects.count(),
        'departements': Departement.objects.count(),
        'communes': Commune.objects.count(),
        'quartiers': QuartierVillage.objects.count(),
    }
    return JsonResponse(stats)
@staff_member_required
def get_departements(request):
    """Vue pour obtenir les départements d'une région"""
    region_id = request.GET.get('region_id')
    if region_id:
        departements = Departement.objects.filter(region_id=region_id).values('id', 'nom', 'code')
        return JsonResponse({'departements': list(departements)})
    return JsonResponse({'departements': []})

@staff_member_required
def get_communes(request):
    """Vue pour obtenir les communes d'un département"""
    departement_id = request.GET.get('departement_id')
    if departement_id:
        communes = Commune.objects.filter(departement_id=departement_id).values('id', 'nom', 'code')
        return JsonResponse({'communes': list(communes)})
    return JsonResponse({'communes': []})

@staff_member_required
def get_quartiers(request):
    """Vue pour obtenir les quartiers d'une commune"""
    commune_id = request.GET.get('commune_id')
    if commune_id:
        quartiers = QuartierVillage.objects.filter(commune_id=commune_id).values('id', 'nom', 'code')
        return JsonResponse({'quartiers': list(quartiers)})
    return JsonResponse({'quartiers': []})
    
@staff_member_required
def get_communes(request):
    """Vue pour obtenir les communes d'un département"""
    departement_id = request.GET.get('departement_id')
    if departement_id:
        communes = Commune.objects.filter(
            departement_id=departement_id
        ).values('id', 'nom', 'code')
        return JsonResponse({'communes': list(communes)})
    return JsonResponse({'communes': []})

@staff_member_required
def search_locations(request):
    """Vue pour l'auto-complétion dans l'admin"""
    term = request.GET.get('term', '')
    results = []
    
    # Recherche dans les régions
    regions = Region.objects.filter(nom__icontains=term)[:5]
    for r in regions:
        results.append({'label': f"Région: {r.nom}", 'value': r.nom, 'type': 'region'})
    
    # Recherche dans les départements
    depts = Departement.objects.filter(nom__icontains=term)[:5]
    for d in depts:
        results.append({'label': f"Département: {d.nom}", 'value': d.nom, 'type': 'departement'})
    
    # Recherche dans les communes
    communes = Commune.objects.filter(nom__icontains=term)[:5]
    for c in communes:
        results.append({'label': f"Commune: {c.nom}", 'value': c.nom, 'type': 'commune'})
    
    return JsonResponse(results, safe=False)