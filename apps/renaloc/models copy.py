from django.db import models
from django.utils import timezone

class Region(models.Model):
    code = models.CharField(max_length=10, unique=True)
    nom = models.CharField(max_length=100)
    
    class Meta:
        ordering = ['nom']
        verbose_name = "Région"
        verbose_name_plural = "Régions"
    
    def __str__(self):
        return f"{self.nom}"

class Departement(models.Model):
    code = models.CharField(max_length=10, unique=True)
    nom = models.CharField(max_length=100)
    region = models.ForeignKey(Region, on_delete=models.CASCADE, related_name='departements')
    
    class Meta:
        ordering = ['nom']
        verbose_name = "Département"
        verbose_name_plural = "Départements"
    
    def __str__(self):
        return f"{self.nom} ({self.region.nom})"

class Commune(models.Model):
    code = models.CharField(max_length=10, unique=True)
    nom = models.CharField(max_length=100)
    departement = models.ForeignKey(Departement, on_delete=models.CASCADE, related_name='communes')
    type_commune = models.CharField(
        max_length=20,
        choices=[
            ('URBAINE', 'Urbaine'),
            ('RURALE', 'Rurale'),
        ],
        default='RURALE'
    )
    
    class Meta:
        ordering = ['nom']
        verbose_name = "Commune"
        verbose_name_plural = "Communes"
    
    def __str__(self):
        return f"{self.nom} ({self.departement.nom})"

class QuartierVillage(models.Model):
    code = models.CharField(max_length=10, unique=True)
    nom = models.CharField(max_length=100)
    commune = models.ForeignKey(Commune, on_delete=models.CASCADE, related_name='quartiers')
    
    class Meta:
        ordering = ['nom']
        verbose_name = "Quartier/Village"
        verbose_name_plural = "Quartiers/Villages"
    
    def __str__(self):
        return f"{self.nom} ({self.commune.nom})"