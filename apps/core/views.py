from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse, FileResponse
from django.core.management import call_command
from django.conf import settings
from .models import BackupHistory
import os
import json
from io import StringIO


def index(request):
    """Page d'accueil publique"""
    return render(request, 'core/index.html')

def user_login(request):
    """Vue de connexion personnalisée"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f"Bienvenue {user.username} !")
            return redirect('core:dashboard')
        else:
            messages.error(request, 'Nom d\'utilisateur ou mot de passe incorrect')
    
    return render(request, 'core/login.html')

def user_logout(request):
    """Vue de déconnexion"""
    logout(request)
    messages.info(request, "Vous avez été déconnecté")
    return redirect('core:index')

@login_required
def dashboard(request):
    """Tableau de bord (nécessite authentification)"""
    # Statistiques
    from apps.eftp_formel.models import EtablissementFormel
    from apps.eftp_non_formel.models import StructureNonFormelle
    from apps.renaloc.models import Region, Departement, Commune
    
    context = {
        'nb_etablissements_formels': EtablissementFormel.objects.count(),
        'nb_structures_non_formelles': StructureNonFormelle.objects.count(),
        'nb_regions': Region.objects.count(),
        'nb_departements': Departement.objects.count(),
        'nb_communes': Commune.objects.count(),
        'recent_backups': BackupHistory.objects.filter(statut='SUCCESS')[:5],
    }
    return render(request, 'core/dashboard.html', context)
    
# Vues pour les sauvegardes
@login_required
def backup_list(request):
    backups = BackupHistory.objects.all()
    
    stats = {
        'total': backups.count(),
        'success': backups.filter(statut='SUCCESS').count(),
        'failed': backups.filter(statut='FAILED').count(),
        'total_size': sum(b.taille_fichier for b in backups if b.statut == 'SUCCESS'),
        'last_backup': backups.filter(statut='SUCCESS').first(),
    }
    
    context = {
        'backups': backups,
        'stats': stats,
    }
    return render(request, 'core/backup/list.html', context)

@login_required
def backup_create(request):
    if request.method == 'POST':
        backup_type = request.POST.get('type', 'manual')
        comment = request.POST.get('comment', '')
        
        try:
            out = StringIO()
            call_command(
                'backup_database',
                type=backup_type,
                comment=comment,
                user_id=request.user.id,
                stdout=out
            )
            messages.success(request, "Sauvegarde créée avec succès")
            return redirect('core:backup_list')
        except Exception as e:
            messages.error(request, f"Erreur lors de la sauvegarde: {str(e)}")
    
    return render(request, 'core/backup/create.html')

@login_required
def backup_download(request, backup_id):
    backup = get_object_or_404(BackupHistory, id=backup_id)
    
    if backup.statut != 'SUCCESS':
        messages.error(request, "Cette sauvegarde n'est pas disponible")
        return redirect('core:backup_list')
    
    if os.path.exists(backup.chemin_fichier):
        response = FileResponse(
            open(backup.chemin_fichier, 'rb'),
            as_attachment=True,
            filename=backup.nom_fichier
        )
        return response
    else:
        messages.error(request, "Fichier de sauvegarde introuvable")
        return redirect('core:backup_list')

@login_required
def backup_restore(request, backup_id):
    backup = get_object_or_404(BackupHistory, id=backup_id)
    
    if request.method == 'POST':
        try:
            out = StringIO()
            call_command(
                'restore_database',
                backup_id,
                user_id=request.user.id,
                stdout=out
            )
            messages.success(request, "Base de données restaurée avec succès")
            return redirect('core:backup_list')
        except Exception as e:
            messages.error(request, f"Erreur lors de la restauration: {str(e)}")
    
    return render(request, 'core/backup/restore_confirm.html', {'backup': backup})

@login_required
def backup_delete(request, backup_id):
    backup = get_object_or_404(BackupHistory, id=backup_id)
    
    if request.method == 'POST':
        if os.path.exists(backup.chemin_fichier):
            os.remove(backup.chemin_fichier)
        
        backup.delete()
        messages.success(request, "Sauvegarde supprimée")
        return redirect('core:backup_list')
    
    return render(request, 'core/backup/delete_confirm.html', {'backup': backup})

@login_required
def backup_settings(request):
    config_file = os.path.join(settings.BASE_DIR, 'backup_config.json')
    config = {}
    
    if os.path.exists(config_file):
        with open(config_file, 'r') as f:
            config = json.load(f)
    
    if request.method == 'POST':
        config = {
            'auto_backup_enabled': request.POST.get('auto_backup_enabled') == 'on',
            'backup_frequency': request.POST.get('backup_frequency', 'daily'),
            'backup_time': request.POST.get('backup_time', '02:00'),
            'max_backups': int(request.POST.get('max_backups', 30)),
            'include_media': request.POST.get('include_media') == 'on',
            'notification_email': request.POST.get('notification_email', ''),
        }
        
        with open(config_file, 'w') as f:
            json.dump(config, f, indent=2)
        
        messages.success(request, "Configuration des sauvegardes enregistrée")
        return redirect('core:backup_settings')
    
    return render(request, 'core/backup/settings.html', {'config': config})