from django.db import models
from django.core.validators import RegexValidator
from django.utils import timezone

# Autorise uniquement les lettres (minuscules/majuscules)
alpha_only = RegexValidator(r'^[a-zA-Z]*$', 'Seules les lettres sont autorisées.')
# Autorise uniquement les chiffres
chiffre_only = RegexValidator(r'^[0-9]*$', 'Seuls les chiffres sont autorisés.')

class Region(models.Model):
    code = models.CharField(max_length=2, unique=True, validators=[chiffre_only]) # Code à 2 caractères pour les régions
    nom = models.CharField(max_length=100) # Nom de la région, limité à 50 caractères
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    
    class Meta:
        ordering = ['nom']
        verbose_name = "Région"
        verbose_name_plural = "Régions"
    
    def __str__(self):
        return f"{self.nom}"

class Departement(models.Model):
    code = models.CharField(max_length=3, unique=True, validators=[chiffre_only]) # Code numérique unique pour chaque département  
    nom = models.CharField(max_length=100)
    region = models.ForeignKey(Region, on_delete=models.CASCADE, related_name='departements')
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    
    class Meta:
        ordering = ['nom']
        verbose_name = "Département"
        verbose_name_plural = "Départements"
    
    def __str__(self):
        return f"{self.nom} ({self.region.nom})"

class Commune(models.Model):
    code = models.CharField(max_length=5, unique=True, validators=[chiffre_only]) # Code numérique unique pour chaque commune
    nom = models.CharField(max_length=100)
    departement = models.ForeignKey(Departement, on_delete=models.CASCADE, related_name='communes')
    TYPE_CHOICES = [
        ('URBAINE', 'Urbaine'),
        ('RURALE', 'Rurale'),
    ]
    type_commune = models.CharField(max_length=20, choices=TYPE_CHOICES, default='RURALE')
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    
    class Meta:
        ordering = ['nom']
        verbose_name = "Commune"
        verbose_name_plural = "Communes"
    
    def __str__(self):
        return f"{self.nom} ({self.departement.nom})"

class QuartierVillage(models.Model):
    code = models.CharField(max_length=8, unique=True, validators=[chiffre_only]) # Code numérique unique pour chaque quartier/village
    nom = models.CharField(max_length=100)
    commune = models.ForeignKey(Commune, on_delete=models.CASCADE, related_name='quartiers')
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    
    class Meta:
        ordering = ['nom']
        verbose_name = "Quartier/Village"
        verbose_name_plural = "Quartiers/Villages"
    
    def __str__(self):
        return f"{self.nom} ({self.commune.nom})"