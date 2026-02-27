from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from .models import EtablissementFormel, ApprenantFormel, FiliereFormel, FormateurFormel
from django.contrib import admin
from django.utils.html import format_html
from .models import EtablissementFormel, ApprenantFormel, FiliereFormel, FormateurFormel

class ApprenantInline(admin.TabularInline):
    model = ApprenantFormel
    extra = 0
    fields = ('cycle', 'annee_etude', 'masculin', 'feminin')
    readonly_fields = ('cycle', 'annee_etude')

class FiliereInline(admin.TabularInline):
    model = FiliereFormel
    extra = 0
    fields = ('nom_filiere', 'secteur', 'cycle', 'effectif_m', 'effectif_f')
    readonly_fields = ('nom_filiere', 'secteur')

class FormateurInline(admin.TabularInline):
    model = FormateurFormel
    extra = 0
    fields = ('nom_prenom', 'sexe', 'statut', 'disciplines_enseignees')
    readonly_fields = ('nom_prenom',)

@admin.register(EtablissementFormel)
class EtablissementFormelAdmin(admin.ModelAdmin):
    list_display = ('code', 'sigle', 'nom', 'statut_badge', 'zone', 'region', 'departement', 
                   'type_etablissement', 'nb_apprenants')
    list_filter = ('statut', 'zone', 'type_etablissement', 'region', 'departement')
    search_fields = ('code', 'sigle', 'nom', 'region__nom', 'departement__nom', 'commune__nom')
    readonly_fields = ('created_at', 'updated_at')
    date_hierarchy = 'date_ouverture'
    
    fieldsets = (
        ('Identification', {
            'fields': ('nom', 'sigle', 'code', 'statut', 'zone'),
            'description': 'Informations de base de l\'établissement'
        }),
        ('Localisation administrative', {
            'fields': ('region', 'departement', 'commune', 'quartier_village', 'adresse'),
            'description': 'Localisation géographique'
        }),
        ('Localisation pédagogique', {
            'fields': ('dre', 'ipde'),
            'classes': ('collapse',)
        }),
        ('Dates', {
            'fields': ('date_autorisation', 'date_ouverture'),
            'classes': ('wide',)
        }),
        ('Coordonnées GPS', {
            'fields': ('longitude', 'latitude'),
            'classes': ('collapse',)
        }),
        ('Caractéristiques', {
            'fields': ('type_etablissement', 'regime', 'internat_fonctionnel'),
            'description': 'Caractéristiques pédagogiques'
        }),
        ('Cycles proposés', {
            'fields': ('cycle_base_1', 'cycle_base_2', 'cycle_moyen_1', 'cycle_moyen_2'),
            'classes': ('wide',)
        }),
        ('Informations complémentaires', {
            'fields': ('patrimoine_foncier', 'ministere_tutelle', 'type_formation', 'dispositif_orientation'),
            'classes': ('collapse',)
        }),
        ('Métadonnées', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    inlines = [ApprenantInline, FiliereInline, FormateurInline]
    actions = ['exporter_selection']
    
    def statut_badge(self, obj):
        if obj.statut == 'PUBLIC':
            return format_html('<span style="background-color: #28a745; color: white; padding: 3px 8px; border-radius: 3px;">Public</span>')
        else:
            return format_html('<span style="background-color: #ffc107; color: black; padding: 3px 8px; border-radius: 3px;">Privé</span>')
    statut_badge.short_description = "Statut"
    
    def nb_apprenants(self, obj):
        total = sum(app.masculin + app.feminin for app in obj.apprenants.all())
        return total
    nb_apprenants.short_description = "Total apprenants"
    
    def exporter_selection(self, request, queryset):
        from django.http import HttpResponse
        import csv
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="etablissements_export.csv"'
        
        writer = csv.writer(response)
        writer.writerow(['Code', 'Sigle', 'Nom', 'Statut', 'Région', 'Type', 'Apprenants'])
        
        for etab in queryset:
            writer.writerow([
                etab.code,
                etab.sigle,
                etab.nom,
                etab.get_statut_display(),
                etab.region.nom,
                etab.get_type_etablissement_display(),
                etab.apprenants.count()
            ])
        
        self.message_user(request, f"{queryset.count()} établissement(s) exporté(s)")
        return response
    exporter_selection.short_description = "Exporter la sélection (CSV)"
    
    class Media:
        css = {
            'all': ('css/admin_eftp.css',)
        }

@admin.register(ApprenantFormel)
class ApprenantFormelAdmin(admin.ModelAdmin):
    list_display = ('etablissement', 'cycle', 'annee_etude', 'masculin', 'feminin', 'total')
    list_filter = ('cycle', 'annee_etude', 'etablissement__region')
    search_fields = ('etablissement__nom', 'etablissement__code')
    
    def total(self, obj):
        return obj.masculin + obj.feminin
    total.short_description = "Total"

@admin.register(FiliereFormel)
class FiliereFormelAdmin(admin.ModelAdmin):
    list_display = ('nom_filiere', 'etablissement', 'secteur', 'cycle', 'effectif_total', 'duree_formation')
    list_filter = ('secteur', 'cycle', 'stage_obligatoire', 'etablissement__region')
    search_fields = ('nom_filiere', 'etablissement__nom', 'diplome_prepare')
    
    def effectif_total(self, obj):
        return obj.effectif_m + obj.effectif_f
    effectif_total.short_description = "Effectif total"

@admin.register(FormateurFormel)
class FormateurFormelAdmin(admin.ModelAdmin):
    list_display = ('nom_prenom', 'etablissement', 'sexe', 'statut', 'nationalite', 'volume_horaire_hebdo')
    list_filter = ('sexe', 'statut', 'nationalite', 'a_recu_renforcement', 'a_ete_inspecte')
    search_fields = ('nom_prenom', 'etablissement__nom', 'disciplines_enseignees')
    date_hierarchy = 'date_naissance'
    
    fieldsets = (
        ('Informations personnelles', {
            'fields': ('nom_prenom', 'sexe', 'date_naissance', 'nationalite')
        }),
        ('Informations professionnelles', {
            'fields': ('etablissement', 'statut', 'annee_recrutement')
        }),
        ('Diplômes', {
            'fields': ('diplome_academique', 'diplome_professionnel')
        }),
        ('Enseignement', {
            'fields': ('disciplines_enseignees', 'volume_horaire_hebdo')
        }),
        ('Évaluations', {
            'fields': ('a_recu_renforcement', 'a_ete_inspecte')
        })
    )