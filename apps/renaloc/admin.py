"""
Configuration de l'interface d'administration pour le module Renaloc
Gestion des localités du Niger : Régions, Départements, Communes, Quartiers/Villages
"""

from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from django.db.models import Count
from .models import Region, Departement, Commune, QuartierVillage

class DepartementInline(admin.TabularInline):
    """
    Affichage des départements dans la page d'une région
    """
    model = Departement
    extra = 0
    fields = ('code', 'nom', 'nb_communes_display', 'lien_vers_communes')
    readonly_fields = ('nb_communes_display', 'lien_vers_communes')
    show_change_link = True
    can_delete = True
    classes = ['collapse']
    
    def nb_communes_display(self, obj):
        return obj.communes.count()
    nb_communes_display.short_description = "Nombre de communes"
    
    def lien_vers_communes(self, obj):
        if obj.pk:
            url = reverse('admin:renaloc_commune_changelist') + f'?departement__id__exact={obj.pk}'
            return format_html('<a class="button" href="{}">Voir les communes</a>', url)
        return "-"
    lien_vers_communes.short_description = "Actions"

class CommuneInline(admin.TabularInline):
    """
    Affichage des communes dans la page d'un département
    """
    model = Commune
    extra = 0
    fields = ('code', 'nom', 'type_commune', 'nb_quartiers_display', 'lien_vers_quartiers')
    readonly_fields = ('nb_quartiers_display', 'lien_vers_quartiers')
    show_change_link = True
    can_delete = True
    classes = ['collapse']
    
    def nb_quartiers_display(self, obj):
        return obj.quartiers.count()
    nb_quartiers_display.short_description = "Nombre de quartiers"
    
    def lien_vers_quartiers(self, obj):
        if obj.pk:
            url = reverse('admin:renaloc_quartiervillage_changelist') + f'?commune__id__exact={obj.pk}'
            return format_html('<a class="button" href="{}">Voir les quartiers</a>', url)
        return "-"
    lien_vers_quartiers.short_description = "Actions"

class QuartierInline(admin.TabularInline):
    """
    Affichage des quartiers dans la page d'une commune
    """
    model = QuartierVillage
    extra = 1
    fields = ('code', 'nom')
    show_change_link = True
    classes = ['collapse']

@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    """
    Administration des régions du Niger
    """
    # Configuration de la liste
    list_display = ('code', 'nom', 'nb_departements', 'nb_communes', 'apercu_departements', 'date_creation')
    list_filter = ('code',)
    search_fields = ('code', 'nom')
    search_help_text = "Rechercher par code ou nom de région"
    ordering = ('code',)
    
    # Configuration du détail
    fieldsets = (
        ('Informations principales', {
            'fields': ('code', 'nom'),
            'description': 'Les informations de base de la région'
        }),
        ('Statistiques', {
            'fields': ('nb_departements_display', 'nb_communes_display'),
            'classes': ('wide',),
            'description': 'Aperçu des entités administratives'
        }),
        ('Métadonnées', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
            'description': 'Informations de création et modification'
        }),
    )
    
    readonly_fields = ('created_at', 'updated_at', 'nb_departements_display', 'nb_communes_display')
    inlines = [DepartementInline]
    
    # Actions personnalisées
    actions = ['exporter_selection', 'dupliquer_region']
    
    def get_queryset(self, request):
        """Optimisation des requêtes"""
        return super().get_queryset(request).prefetch_related('departements__communes')
    
    def nb_departements(self, obj):
        """Nombre de départements dans la région"""
        count = obj.departements.count()
        url = reverse('admin:renaloc_departement_changelist') + f'?region__id__exact={obj.id}'
        return format_html('<a href="{}">{} département(s)</a>', url, count)
    nb_departements.short_description = "Départements"
    nb_departements.admin_order_field = 'departements_count'
    
    def nb_communes(self, obj):
        """Nombre total de communes dans la région"""
        count = Commune.objects.filter(departement__region=obj).count()
        url = reverse('admin:renaloc_commune_changelist') + f'?departement__region__id__exact={obj.id}'
        return format_html('<a href="{}">{} commune(s)</a>', url, count)
    nb_communes.short_description = "Communes"
    
    def nb_departements_display(self, obj):
        """Affichage pour les champs readonly"""
        return obj.departements.count()
    nb_departements_display.short_description = "Nombre de départements"
    
    def nb_communes_display(self, obj):
        """Affichage pour les champs readonly"""
        return Commune.objects.filter(departement__region=obj).count()
    nb_communes_display.short_description = "Nombre de communes"
    
    def apercu_departements(self, obj):
        """Aperçu des premiers départements"""
        deps = obj.departements.all()[:3]
        return ", ".join([d.nom for d in deps]) + ("..." if obj.departements.count() > 3 else "")
    apercu_departements.short_description = "Départements (aperçu)"
    
    def date_creation(self, obj):
        """Date de création formatée"""
        return obj.created_at.strftime("%d/%m/%Y %H:%M") if obj.created_at else "-"
    date_creation.short_description = "Créé le"
    date_creation.admin_order_field = 'created_at'
    
    def exporter_selection(self, request, queryset):
        """Action pour exporter les régions sélectionnées"""
        from django.http import HttpResponse
        import csv
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="regions_export.csv"'
        
        writer = csv.writer(response)
        writer.writerow(['Code', 'Nom', 'Nombre départements', 'Date création'])
        
        for region in queryset:
            writer.writerow([
                region.code,
                region.nom,
                region.departements.count(),
                region.created_at.strftime("%d/%m/%Y") if region.created_at else ""
            ])
        
        self.message_user(request, f"{queryset.count()} région(s) exportée(s)")
        return response
    exporter_selection.short_description = "Exporter les régions sélectionnées (CSV)"
    
    def dupliquer_region(self, request, queryset):
        """Action pour dupliquer une région"""
        for region in queryset:
            region.pk = None
            region.code = f"COPY_{region.code}"
            region.nom = f"{region.nom} (copie)"
            region.save()
        self.message_user(request, f"{queryset.count()} région(s) dupliquée(s)")
    dupliquer_region.short_description = "Dupliquer les régions sélectionnées"
    
    class Media:
        css = {
            'all': ('css/admin_renaloc.css',)
        }
        js = ('js/admin_renaloc.js',)

@admin.register(Departement)
class DepartementAdmin(admin.ModelAdmin):
    """
    Administration des départements du Niger
    """
    list_display = ('code', 'nom', 'region', 'nb_communes', 'apercu_communes', 'type_zone')
    list_filter = ('region', 'communes__type_commune')
    search_fields = ('code', 'nom', 'region__nom')
    search_help_text = "Rechercher par code, nom ou région"
    ordering = ('region__code', 'code')
    list_select_related = ('region',)
    list_per_page = 25
    
    fieldsets = (
        ('Informations principales', {
            'fields': ('code', 'nom', 'region'),
            'description': 'Les informations de base du département'
        }),
        ('Statistiques', {
            'fields': ('nb_communes_display', 'apercu_communes_display'),
            'classes': ('wide',),
        }),
        ('Carte', {
            'fields': ('visualisation_carte',),
            'classes': ('collapse',),
            'description': 'Visualisation sur la carte'
        }),
    )
    
    readonly_fields = ('nb_communes_display', 'apercu_communes_display', 'visualisation_carte')
    inlines = [CommuneInline]
    
    actions = ['exporter_selection', 'changer_region']
    
    def get_queryset(self, request):
        """Optimisation des requêtes"""
        return super().get_queryset(request).prefetch_related('communes')
    
    def nb_communes(self, obj):
        """Nombre de communes dans le département"""
        count = obj.communes.count()
        url = reverse('admin:renaloc_commune_changelist') + f'?departement__id__exact={obj.id}'
        return format_html('<a href="{}">{} commune(s)</a>', url, count)
    nb_communes.short_description = "Communes"
    nb_communes.admin_order_field = 'communes_count'
    
    def nb_communes_display(self, obj):
        """Affichage pour les champs readonly"""
        return obj.communes.count()
    nb_communes_display.short_description = "Nombre de communes"
    
    def apercu_communes(self, obj):
        """Aperçu des premières communes"""
        comms = obj.communes.all()[:3]
        return ", ".join([c.nom for c in comms]) + ("..." if obj.communes.count() > 3 else "")
    apercu_communes.short_description = "Communes (aperçu)"
    
    def apercu_communes_display(self, obj):
        """Affichage détaillé pour les champs readonly"""
        comms = obj.communes.all()
        if comms:
            return format_html("<br>".join([f"• {c.nom} ({c.type_commune})" for c in comms[:5]]))
        return "Aucune commune"
    apercu_communes_display.short_description = "Liste des communes"
    
    def type_zone(self, obj):
        """Détermine si le département est plutôt urbain ou rural"""
        communes = obj.communes.all()
        if communes:
            urbaines = communes.filter(type_commune='URBAINE').count()
            if urbaines > communes.count() / 2:
                return format_html('<span style="color: #28a745;">🏙️ Urbain</span>')
            else:
                return format_html('<span style="color: #6c757d;">🌾 Rural</span>')
        return "-"
    type_zone.short_description = "Tendance"
    
    def visualisation_carte(self, obj):
        """Placeholder pour une visualisation cartographique"""
        return format_html(
            '<div style="background: #f8f9fa; padding: 20px; text-align: center; border: 1px dashed #dee2e6;">'
            '<i class="fas fa-map-marked-alt" style="font-size: 48px; color: #6c757d;"></i>'
            '<p style="margin-top: 10px; color: #6c757d;">Carte du département {0} à intégrer</p>'
            '</div>',
            obj.nom
        )
    visualisation_carte.short_description = "Visualisation"
    
    def changer_region(self, request, queryset):
        """Action pour changer la région de plusieurs départements"""
        from django.contrib import messages
        if 'apply' in request.POST:
            region_id = request.POST.get('region')
            if region_id:
                region = Region.objects.get(id=region_id)
                count = queryset.update(region=region)
                self.message_user(request, f"{count} département(s) déplacé(s) vers {region.nom}")
            return None
        
        # Afficher un formulaire intermédiaire
        from django.shortcuts import render
        from django.template.response import TemplateResponse
        
        context = {
            'departements': queryset,
            'regions': Region.objects.all(),
            'action': 'changer_region',
            'action_checkbox_name': admin.ACTION_CHECKBOX_NAME,
        }
        return TemplateResponse(request, 'admin/renaloc/departement/change_region.html', context)
    changer_region.short_description = "Changer la région des départements sélectionnés"
    
    def exporter_selection(self, request, queryset):
        """Action pour exporter les départements sélectionnés"""
        from django.http import HttpResponse
        import csv
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="departements_export.csv"'
        
        writer = csv.writer(response)
        writer.writerow(['Code', 'Nom', 'Région', 'Nombre communes'])
        
        for dept in queryset:
            writer.writerow([
                dept.code,
                dept.nom,
                dept.region.nom,
                dept.communes.count()
            ])
        
        self.message_user(request, f"{queryset.count()} département(s) exporté(s)")
        return response
    exporter_selection.short_description = "Exporter les départements sélectionnés (CSV)"

@admin.register(Commune)
class CommuneAdmin(admin.ModelAdmin):
    """
    Administration des communes du Niger
    """
    list_display = ('code', 'nom', 'departement', 'region', 'type_commune_badge', 'nb_quartiers', 'apercu_quartiers')
    list_filter = ('type_commune', 'departement__region', 'departement')
    search_fields = ('code', 'nom', 'departement__nom', 'departement__region__nom')
    search_help_text = "Rechercher par code, nom, département ou région"
    ordering = ('departement__code', 'code')
    list_select_related = ('departement', 'departement__region')
    list_per_page = 25
    
    fieldsets = (
        ('Informations principales', {
            'fields': ('code', 'nom', 'departement', 'type_commune'),
            'description': 'Les informations de base de la commune'
        }),
        ('Statistiques', {
            'fields': ('nb_quartiers_display', 'population_estimate'),
            'classes': ('wide',),
        }),
        ('Géolocalisation', {
            'fields': ('coordonnees',),
            'classes': ('collapse',),
        }),
    )
    
    readonly_fields = ('nb_quartiers_display', 'region_display', 'population_estimate', 'coordonnees')
    inlines = [QuartierInline]
    
    actions = ['exporter_selection', 'marquer_urbain', 'marquer_rural']
    
    def get_queryset(self, request):
        """Optimisation des requêtes"""
        return super().get_queryset(request).prefetch_related('quartiers')
    
    def region(self, obj):
        """Région de la commune"""
        return obj.departement.region.nom
    region.short_description = "Région"
    region.admin_order_field = 'departement__region__nom'
    
    def region_display(self, obj):
        """Affichage pour les champs readonly"""
        return obj.departement.region.nom
    region_display.short_description = "Région"
    
    def type_commune_badge(self, obj):
        """Affichage du type avec un badge coloré"""
        if obj.type_commune == 'URBAINE':
            return format_html('<span style="background-color: #28a745; color: white; padding: 3px 8px; border-radius: 3px;">🏙️ Urbaine</span>')
        else:
            return format_html('<span style="background-color: #6c757d; color: white; padding: 3px 8px; border-radius: 3px;">🌾 Rurale</span>')
    type_commune_badge.short_description = "Type"
    
    def nb_quartiers(self, obj):
        """Nombre de quartiers dans la commune"""
        count = obj.quartiers.count()
        url = reverse('admin:renaloc_quartiervillage_changelist') + f'?commune__id__exact={obj.id}'
        return format_html('<a href="{}">{} quartier(s)</a>', url, count)
    nb_quartiers.short_description = "Quartiers"
    nb_quartiers.admin_order_field = 'quartiers_count'
    
    def nb_quartiers_display(self, obj):
        """Affichage pour les champs readonly"""
        return obj.quartiers.count()
    nb_quartiers_display.short_description = "Nombre de quartiers"
    
    def apercu_quartiers(self, obj):
        """Aperçu des premiers quartiers"""
        quarts = obj.quartiers.all()[:3]
        return ", ".join([q.nom for q in quarts]) + ("..." if obj.quartiers.count() > 3 else "")
    apercu_quartiers.short_description = "Quartiers (aperçu)"
    
    def population_estimate(self, obj):
        """Estimation de la population (placeholder)"""
        return format_html(
            '<span style="color: #6c757d;">Donnée à importer</span>'
        )
    population_estimate.short_description = "Population estimée"
    
    def coordonnees(self, obj):
        """Placeholder pour les coordonnées GPS"""
        return format_html(
            '<div style="background: #f8f9fa; padding: 10px;">'
            'Latitude: --, Longitude: --<br>'
            '<small class="text-muted">Coordonnées à importer</small>'
            '</div>'
        )
    coordonnees.short_description = "Coordonnées GPS"
    
    def marquer_urbain(self, request, queryset):
        """Action pour marquer les communes comme urbaines"""
        count = queryset.update(type_commune='URBAINE')
        self.message_user(request, f"{count} commune(s) marquée(s) comme urbaine(s)")
    marquer_urbain.short_description = "Marquer comme urbaine"
    
    def marquer_rural(self, request, queryset):
        """Action pour marquer les communes comme rurales"""
        count = queryset.update(type_commune='RURALE')
        self.message_user(request, f"{count} commune(s) marquée(s) comme rurale(s)")
    marquer_rural.short_description = "Marquer comme rurale"
    
    def exporter_selection(self, request, queryset):
        """Action pour exporter les communes sélectionnées"""
        from django.http import HttpResponse
        import csv
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="communes_export.csv"'
        
        writer = csv.writer(response)
        writer.writerow(['Code', 'Nom', 'Département', 'Région', 'Type', 'Nombre quartiers'])
        
        for commune in queryset:
            writer.writerow([
                commune.code,
                commune.nom,
                commune.departement.nom,
                commune.departement.region.nom,
                commune.type_commune,
                commune.quartiers.count()
            ])
        
        self.message_user(request, f"{queryset.count()} commune(s) exportée(s)")
        return response
    exporter_selection.short_description = "Exporter les communes sélectionnées (CSV)"

@admin.register(QuartierVillage)
class QuartierVillageAdmin(admin.ModelAdmin):
    """
    Administration des quartiers et villages du Niger
    """
    list_display = ('code', 'nom', 'commune', 'departement', 'region', 'type_quartier_icon')
    list_filter = ('commune__departement__region', 'commune__departement', 'commune')
    search_fields = ('code', 'nom', 'commune__nom', 'commune__departement__nom')
    search_help_text = "Rechercher par code, nom, commune ou département"
    ordering = ('commune__code', 'code')
    list_select_related = ('commune', 'commune__departement', 'commune__departement__region')
    list_per_page = 50
    
    fieldsets = (
        ('Informations', {
            'fields': ('code', 'nom', 'commune'),
            'description': 'Les informations du quartier/village'
        }),
        ('Localisation complète', {
            'fields': ('localisation_complete',),
            'classes': ('wide',),
        }),
    )
    
    readonly_fields = ('localisation_complete',)
    
    actions = ['exporter_selection']
    
    def get_queryset(self, request):
        """Optimisation des requêtes"""
        return super().get_queryset(request).select_related(
            'commune', 'commune__departement', 'commune__departement__region'
        )
    
    def departement(self, obj):
        """Département du quartier"""
        return obj.commune.departement.nom
    departement.short_description = "Département"
    departement.admin_order_field = 'commune__departement__nom'
    
    def region(self, obj):
        """Région du quartier"""
        return obj.commune.departement.region.nom
    region.short_description = "Région"
    region.admin_order_field = 'commune__departement__region__nom'
    
    def type_quartier_icon(self, obj):
        """Icône selon le type (village ou quartier)"""
        if 'quartier' in obj.nom.lower() or 'Q' in obj.code:
            return format_html('<span style="font-size: 1.2em;">🏘️</span>')
        return format_html('<span style="font-size: 1.2em;">🏕️</span>')
    type_quartier_icon.short_description = ""
    
    def localisation_complete(self, obj):
        """Affiche la localisation complète"""
        return format_html(
            '<div style="background: #f8f9fa; padding: 15px; border-left: 4px solid #17a2b8;">'
            '<strong style="font-size: 1.1em;">{0}</strong><br>'
            '📍 Commune de {1}<br>'
            '🗺️ Département de {2}<br>'
            '🌍 Région de {3}'
            '</div>',
            obj.nom,
            obj.commune.nom,
            obj.commune.departement.nom,
            obj.commune.departement.region.nom
        )
    localisation_complete.short_description = "Localisation"
    
    def exporter_selection(self, request, queryset):
        """Action pour exporter les quartiers sélectionnés"""
        from django.http import HttpResponse
        import csv
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="quartiers_export.csv"'
        
        writer = csv.writer(response)
        writer.writerow(['Code', 'Nom', 'Commune', 'Département', 'Région'])
        
        for quartier in queryset:
            writer.writerow([
                quartier.code,
                quartier.nom,
                quartier.commune.nom,
                quartier.commune.departement.nom,
                quartier.commune.departement.region.nom
            ])
        
        self.message_user(request, f"{queryset.count()} quartier(s) exporté(s)")
        return response
    exporter_selection.short_description = "Exporter les quartiers sélectionnés (CSV)"