from django.db import models
from django.contrib.auth.models import User

class BackupHistory(models.Model):
    """Historique des sauvegardes de la base de données"""
    
    STATUS_CHOICES = [
        ('SUCCESS', 'Succès'),
        ('FAILED', 'Échec'),
        ('IN_PROGRESS', 'En cours'),
    ]
    
    BACKUP_TYPE_CHOICES = [
        ('MANUAL', 'Manuelle'),
        ('AUTOMATIC', 'Automatique'),
        ('SCHEDULED', 'Planifiée'),
    ]
    
    nom_fichier = models.CharField(max_length=255)
    taille_fichier = models.BigIntegerField(default=0, help_text="Taille en octets")
    date_creation = models.DateTimeField(auto_now_add=True)
    date_completion = models.DateTimeField(null=True, blank=True)
    statut = models.CharField(max_length=20, choices=STATUS_CHOICES, default='IN_PROGRESS')
    type_backup = models.CharField(max_length=20, choices=BACKUP_TYPE_CHOICES, default='MANUAL')
    utilisateur = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    commentaire = models.TextField(blank=True)
    chemin_fichier = models.CharField(max_length=500)
    logs = models.TextField(blank=True, help_text="Logs détaillés de la sauvegarde")
    
    class Meta:
        ordering = ['-date_creation']
        verbose_name = "Historique de sauvegarde"
        verbose_name_plural = "Historiques des sauvegardes"
    
    def __str__(self):
        return f"{self.nom_fichier} - {self.date_creation.strftime('%d/%m/%Y %H:%M')}"
    
    def taille_formatee(self):
        """Retourne la taille formatée (Ko, Mo, Go)"""
        size = self.taille_fichier
        for unit in ['octets', 'Ko', 'Mo', 'Go']:
            if size < 1024.0 or unit == 'Go':
                return f"{size:.2f} {unit}"
            size /= 1024.0
        return f"{self.taille_fichier} octets"

class RestoreHistory(models.Model):
    """Historique des restaurations"""
    
    STATUS_CHOICES = [
        ('SUCCESS', 'Succès'),
        ('FAILED', 'Échec'),
        ('IN_PROGRESS', 'En cours'),
    ]
    
    backup = models.ForeignKey(BackupHistory, on_delete=models.CASCADE, related_name='restaurations')
    date_restauration = models.DateTimeField(auto_now_add=True)
    utilisateur = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    statut = models.CharField(max_length=20, choices=STATUS_CHOICES, default='IN_PROGRESS')
    logs = models.TextField(blank=True)
    
    class Meta:
        ordering = ['-date_restauration']
        verbose_name = "Historique de restauration"
        verbose_name_plural = "Historiques des restaurations"
    
    def __str__(self):
        return f"Restauration de {self.backup.nom_fichier} - {self.date_restauration}"