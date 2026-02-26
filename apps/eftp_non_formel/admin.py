from django.contrib import admin
from .models import (
    StructureNonFormelle, ApprentiNonFormel, 
    MaitreArtisan, MetierNonFormel
)

class ApprentiInline(admin.TabularInline):
    model = ApprentiNonFormel
    extra = 0
    fields = ('secteur', 'duree_apprentissage', 'masculin', 'feminin')

class MaitreArtisanInline(admin.TabularInline):
    model = MaitreArtisan
    extra = 0
    fields = ('nom_prenom', 'sexe', 'grade', 'qualification_certifiee')

class MetierInline(admin.TabularInline):
    model = MetierNonFormel
    extra = 0
    fields = ('nom_metier', 'secteur', 'duree_apprentissage', 'promo_1_m', 'promo_1_f')

@admin.register(StructureNonFormelle)
class StructureNonFormelleAdmin(admin.ModelAdmin):
    list_display = ('code', 'nom', 'statut', 'zone', 'region', 'type_structure', 'nb_apprentis')
    list_filter = ('statut', 'zone', 'type_structure', 'a_electricite', 'a_point_eau', 'a_connexion_internet')
    search_fields = ('code', 'nom', 'region__nom', 'departement__nom')
    readonly_fields = ('created_at', 'updated_at')
    date_hierarchy = 'date_ouverture'
    
    fieldsets = (
        ('Identification', {
            'fields': ('nom', 'code', 'statut', 'zone')
        }),
        ('Documents administratifs', {
            'fields': ('a_document', 'ministere_tutelle', 'type_document', 'reference_document')
        }),
        ('Dates', {
            'fields': ('date_autorisation', 'date_ouverture')
        }),
        ('Localisation', {
            'fields': ('region', 'departement', 'commune', 'quartier_village')
        }),
        ('Type de structure', {
            'fields': ('type_structure', 'autre_type_precision')
        }),
        ('Financement', {
            'fields': ('source_financement',)
        }),
        ('Caractéristiques', {
            'fields': ('regime', 'delivre_attestation', 'formation_payante')
        }),
        ('Infrastructures', {
            'fields': (
                'a_electricite', 'source_electricite',
                'a_point_eau', 'source_eau',
                'a_cloture', 'a_infirmerie', 'a_boite_pharmacie',
                'a_depotoir', 'nombre_depotoirs',
                'a_rampes_handicapes', 'a_cour_recreation',
                'a_latrines', 'nombre_latrines',
                'a_bibliotheque', 'a_connexion_internet', 'type_connexion',
                'a_terrain_sport', 'a_paysage', 'a_parking',
                'a_lavage_mains', 'a_collecte_ordures'
            ),
            'classes': ('collapse',)
        }),
        ('Personnel', {
            'fields': ('nb_maitres_artisans_h', 'nb_maitres_artisans_f', 
                      'nb_formateurs_h', 'nb_formateurs_f')
        }),
        ('Coordonnées GPS', {
            'fields': ('longitude', 'latitude'),
            'classes': ('collapse',)
        }),
        ('Métadonnées', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    inlines = [ApprentiInline, MaitreArtisanInline, MetierInline]
    
    def nb_apprentis(self, obj):
        total = sum(app.masculin + app.feminin for app in obj.apprentis.all())
        return total
    nb_apprentis.short_description = "Total apprentis"

@admin.register(ApprentiNonFormel)
class ApprentiNonFormelAdmin(admin.ModelAdmin):
    list_display = ('structure', 'secteur', 'duree_apprentissage', 'masculin', 'feminin', 'total')
    list_filter = ('secteur', 'duree_apprentissage', 'structure__region')
    search_fields = ('structure__nom', 'structure__code')
    
    def total(self, obj):
        return obj.masculin + obj.feminin
    total.short_description = "Total"

@admin.register(MaitreArtisan)
class MaitreArtisanAdmin(admin.ModelAdmin):
    list_display = ('nom_prenom', 'structure', 'sexe', 'grade', 'qualification_certifiee', 'nationalite')
    list_filter = ('sexe', 'grade', 'qualification_certifiee', 'nationalite', 'a_recu_suivi')
    search_fields = ('nom_prenom', 'structure__nom')
    
    fieldsets = (
        ('Informations personnelles', {
            'fields': ('nom_prenom', 'sexe', 'nationalite')
        }),
        ('Informations professionnelles', {
            'fields': ('structure', 'grade', 'formation_initiale', 'nb_formation_continue')
        }),
        ('Certifications', {
            'fields': ('qualification_certifiee', 'dernier_certificat', 
                      'niveau_certificat', 'structure_certifiante', 'annee_certification')
        }),
        ('Suivi', {
            'fields': ('a_recu_suivi',)
        })
    )

@admin.register(MetierNonFormel)
class MetierNonFormelAdmin(admin.ModelAdmin):
    list_display = ('nom_metier', 'structure', 'secteur', 'duree_apprentissage', 'effectif_total')
    list_filter = ('secteur', 'duree_apprentissage', 'structure__region')
    search_fields = ('nom_metier', 'structure__nom')
    
    fieldsets = (
        ('Informations', {
            'fields': ('structure', 'secteur', 'nom_metier', 'duree_apprentissage')
        }),
        ('Promotion I', {
            'fields': ('promo_1_m', 'promo_1_f')
        }),
        ('Promotion II', {
            'fields': ('promo_2_m', 'promo_2_f')
        }),
        ('Promotion III', {
            'fields': ('promo_3_m', 'promo_3_f')
        }),
        ('Catégories spéciales', {
            'fields': ('handicapes_m', 'handicapes_f',
                      'refugies_m', 'refugies_f',
                      'retournes_m', 'retournes_f',
                      'deplaces_m', 'deplaces_f'),
            'classes': ('collapse',)
        })
    )
    
    def effectif_total(self, obj):
        return (obj.promo_1_m + obj.promo_1_f + 
                obj.promo_2_m + obj.promo_2_f + 
                obj.promo_3_m + obj.promo_3_f)
    effectif_total.short_description = "Effectif total"