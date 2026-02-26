from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib import messages
from .models import Region, Departement, Commune, QuartierVillage

@receiver(post_save, sender=Region)
def region_saved(sender, instance, created, **kwargs):
    """Action après la sauvegarde d'une région"""
    if created:
        print(f"✅ Nouvelle région créée : {instance.nom}")
    else:
        print(f"✏️ Région modifiée : {instance.nom}")

@receiver(post_save, sender=Departement)
def departement_saved(sender, instance, created, **kwargs):
    """Action après la sauvegarde d'un département"""
    if created:
        print(f"✅ Nouveau département créé : {instance.nom} dans {instance.region.nom}")

@receiver(post_delete, sender=Commune)
def commune_deleted(sender, instance, **kwargs):
    """Action après la suppression d'une commune"""
    print(f"❌ Commune supprimée : {instance.nom}")