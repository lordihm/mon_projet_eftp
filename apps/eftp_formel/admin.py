from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
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
    list_display = ('code', 'nom', 'statut', 'zone', 'region', 'departement', 'type_etablissement', 'nb_apprenants')
    list_filter = ('statut', 'zone', 'type_etablissement', 'region', 'departement')
    search_fields = ('code', 'nom', 'region__nom', 'departement__nom', 'commune__nom')
    readonly_fields = ('created_at', 'updated_at')
    date_hierarchy = 'date_ouverture'
    
    fieldsets = (
        ('Identification', {
            'fields': ('nom', 'code', 'statut', 'zone')
        }),
        ('Localisation administrative', {
            'fields': ('region', 'departement', 'commune', 'quartier_village', 'adresse')
        }),
        ('Localisation pédagogique', {
            'fields': ('dre', 'ipde')
        }),
        ('Dates', {
            'fields': ('date_autorisation', 'date_ouverture')
        }),
        ('Coordonnées GPS', {
            'fields': ('longitude', 'latitude'),
            'classes': ('collapse',)
        }),
        ('Caractéristiques', {
            'fields': ('type_etablissement', 'regime', 'internat_fonctionnel')
        }),
        ('Métadonnées', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    inlines = [ApprenantInline, FiliereInline, FormateurInline]
    
    def nb_apprenants(self, obj):
        total = sum(app.masculin + app.feminin for app in obj.apprenants.all())
        return total
    nb_apprenants.short_description = "Total apprenants"
    
    def save_model(self, request, obj, form, change):
        if not change:  # Si c'est une création
            obj.created_by = request.user
        super().save_model(request, obj, form, change)

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