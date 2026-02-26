from django.contrib import admin
from django.utils.html import format_html
from .models import BackupHistory, RestoreHistory

@admin.register(BackupHistory)
class BackupHistoryAdmin(admin.ModelAdmin):
    list_display = ('nom_fichier', 'taille_formatee', 'date_creation', 'statut', 'type_backup', 'utilisateur')
    list_filter = ('statut', 'type_backup', 'date_creation')
    search_fields = ('nom_fichier', 'commentaire', 'logs')
    readonly_fields = ('date_creation', 'date_completion', 'taille_fichier', 'chemin_fichier')
    date_hierarchy = 'date_creation'
    
    fieldsets = (
        ('Informations générales', {
            'fields': ('nom_fichier', 'taille_fichier', 'chemin_fichier')
        }),
        ('Statut', {
            'fields': ('statut', 'type_backup', 'date_creation', 'date_completion')
        }),
        ('Utilisateur et commentaire', {
            'fields': ('utilisateur', 'commentaire')
        }),
        ('Logs', {
            'fields': ('logs',),
            'classes': ('collapse',)
        })
    )
    
    def taille_formatee(self, obj):
        return obj.taille_formatee()
    taille_formatee.short_description = "Taille"
    
    def save_model(self, request, obj, form, change):
        if not obj.utilisateur:
            obj.utilisateur = request.user
        super().save_model(request, obj, form, change)

@admin.register(RestoreHistory)
class RestoreHistoryAdmin(admin.ModelAdmin):
    list_display = ('backup', 'date_restauration', 'utilisateur', 'statut')
    list_filter = ('statut', 'date_restauration')
    search_fields = ('backup__nom_fichier', 'logs')
    readonly_fields = ('date_restauration',)
    
    fieldsets = (
        ('Informations', {
            'fields': ('backup', 'utilisateur', 'date_restauration', 'statut')
        }),
        ('Logs', {
            'fields': ('logs',),
            'classes': ('collapse',)
        })
    )