from django import forms
from .models import StructureNonFormelle, MaitreArtisan, ApprentiNonFormel, MetierNonFormel
from apps.renaloc.models import Region, Departement, Commune, QuartierVillage

# ================ FORMULAIRE SIMPLIFIÉ POUR CRÉATION ================
# UNIQUEMENT les informations de base de la structure

class StructureNonFormelleSimpleForm(forms.ModelForm):
    """Formulaire simplifié pour la création initiale d'une structure
    - Uniquement les informations de base
    - Pas d'infrastructures, pas d'équipements
    """
    
    class Meta:
        model = StructureNonFormelle
        fields = [
            'code', 'nom', 'sigle', 'statut', 'zone', 'type_structure', 
            'autre_type_precision', 'region', 'departement', 'commune', 
            'quartier_village', 'adresse', 'a_document', 'ministere_tutelle',
            'type_document', 'reference_document', 'date_autorisation', 
            'date_ouverture', 'longitude', 'latitude'
        ]
        widgets = {
            'adresse': forms.Textarea(attrs={'rows': 2, 'class': 'form-control'}),
            'autre_type_precision': forms.TextInput(attrs={'class': 'form-control', 
                                                           'placeholder': 'Précisez le type...'}),
            'date_autorisation': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'date_ouverture': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'longitude': forms.NumberInput(attrs={'step': 'any', 'class': 'form-control', 
                                                  'placeholder': 'Ex: 2.123456'}),
            'latitude': forms.NumberInput(attrs={'step': 'any', 'class': 'form-control', 
                                                 'placeholder': 'Ex: 13.123456'}),
            'type_document': forms.TextInput(attrs={'class': 'form-control'}),
            'reference_document': forms.TextInput(attrs={'class': 'form-control'}),
            'ministere_tutelle': forms.TextInput(attrs={'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Ajouter la classe form-control à tous les champs
        for field_name, field in self.fields.items():
            if isinstance(field.widget, (forms.Select, forms.SelectMultiple)):
                field.widget.attrs['class'] = 'form-select'
            elif isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs['class'] = 'form-check-input'
            else:
                field.widget.attrs['class'] = 'form-control'
            
            # Ajouter des placeholders
            if field_name == 'nom':
                field.widget.attrs['placeholder'] = "Nom complet de la structure"
            elif field_name == 'sigle':
                field.widget.attrs['placeholder'] = "Ex: CFA, ATELIER..."
            elif field_name == 'code':
                field.widget.attrs['placeholder'] = "Code unique"
        
        # Rendre certains champs optionnels
        self.fields['quartier_village'].required = False
        self.fields['adresse'].required = False
        self.fields['sigle'].required = False
        self.fields['autre_type_precision'].required = False
        self.fields['ministere_tutelle'].required = False
        self.fields['type_document'].required = False
        self.fields['reference_document'].required = False
        self.fields['date_autorisation'].required = False
        self.fields['date_ouverture'].required = False
        self.fields['longitude'].required = False
        self.fields['latitude'].required = False


# ================ FORMULAIRE COMPLET POUR SAISIE DÉTAILLÉE ================
# TOUTES les données (infrastructures, équipements, personnel...)

class StructureNonFormelleCompletForm(forms.ModelForm):
    """Formulaire complet pour toutes les données d'une structure
    - Infrastructures, équipements, services, personnel
    """
    
    class Meta:
        model = StructureNonFormelle
        fields = [
            # Régime et formations
            'regime', 'delivre_attestation', 'formation_payante',
            
            # Financement et accompagnement
            'source_financement', 'type_accompagnement', 'mode_paiement',
            
            # Équipements de base
            'a_electricite', 'source_electricite',
            'a_point_eau', 'source_eau',
            
            # Infrastructures physiques
            'a_cloture', 'a_infirmerie', 'a_boite_pharmacie',
            'a_depotoir', 'nombre_depotoirs',
            'a_rampes_handicapes', 'a_cour_recreation',
            
            # Latrines
            'a_latrines', 'nombre_latrines', 'latrines_apprenants',
            'latrines_filles', 'latrines_personnel', 'latrines_handicapes',
            
            # Équipements pédagogiques
            'a_bibliotheque', 'a_connexion_internet', 'type_connexion', 'acces_internet',
            'a_terrain_sport', 'a_paysage', 'a_parking',
            'a_lavage_mains', 'a_collecte_ordures',
            
            # Personnel
            'nb_maitres_artisans_h', 'nb_maitres_artisans_f',
            'nb_formateurs_h', 'nb_formateurs_f',
        ]
        widgets = {
            'source_financement': forms.CheckboxSelectMultiple(),
            'type_accompagnement': forms.CheckboxSelectMultiple(),
            'mode_paiement': forms.CheckboxSelectMultiple(),
            'acces_internet': forms.CheckboxSelectMultiple(),
            'nombre_depotoirs': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'nombre_latrines': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'latrines_apprenants': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'latrines_filles': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'latrines_personnel': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'latrines_handicapes': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'nb_maitres_artisans_h': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'nb_maitres_artisans_f': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'nb_formateurs_h': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'nb_formateurs_f': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'source_electricite': forms.Select(attrs={'class': 'form-select'}),
            'source_eau': forms.Select(attrs={'class': 'form-select'}),
            'type_connexion': forms.Select(attrs={'class': 'form-select'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Ajouter la classe form-control aux champs appropriés
        for field_name, field in self.fields.items():
            if field_name in ['source_financement', 'type_accompagnement', 
                             'mode_paiement', 'acces_internet']:
                # Les champs CheckboxSelectMultiple gardent leur propre style
                continue
            elif isinstance(field.widget, (forms.Select, forms.SelectMultiple)):
                field.widget.attrs['class'] = 'form-select'
            elif isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs['class'] = 'form-check-input'
            else:
                field.widget.attrs['class'] = 'form-control'
        
        # Rendre certains champs optionnels
        optional_fields = [
            'source_financement', 'type_accompagnement', 'mode_paiement',
            'source_electricite', 'source_eau', 'type_connexion', 'acces_internet',
            'nombre_depotoirs', 'nombre_latrines', 'latrines_apprenants',
            'latrines_filles', 'latrines_personnel', 'latrines_handicapes',
            'nb_maitres_artisans_h', 'nb_maitres_artisans_f',
            'nb_formateurs_h', 'nb_formateurs_f'
        ]
        for field in optional_fields:
            if field in self.fields:
                self.fields[field].required = False


# ================ FORMULAIRES POUR LES MAÎTRES ARTISANS ================

class MaitreArtisanForm(forms.ModelForm):
    """Formulaire pour les maîtres artisans"""
    
    class Meta:
        model = MaitreArtisan
        exclude = ['structure', 'created_at', 'updated_at']
        widgets = {
            'nom_prenom': forms.TextInput(attrs={'class': 'form-control'}),
            'sexe': forms.Select(attrs={'class': 'form-select'}),
            'grade': forms.Select(attrs={'class': 'form-select'}),
            'formation_initiale': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'nb_formation_continue': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'qualification_certifiee': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'dernier_certificat': forms.TextInput(attrs={'class': 'form-control'}),
            'niveau_certificat': forms.TextInput(attrs={'class': 'form-control'}),
            'structure_certifiante': forms.TextInput(attrs={'class': 'form-control'}),
            'annee_certification': forms.NumberInput(attrs={'class': 'form-control', 'min': 1900, 'max': 2100}),
            'nationalite': forms.Select(attrs={'class': 'form-select'}),
            'a_recu_suivi': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Rendre certains champs optionnels
        optional_fields = [
            'dernier_certificat', 'niveau_certificat', 'structure_certifiante',
            'annee_certification', 'nb_formation_continue'
        ]
        for field in optional_fields:
            if field in self.fields:
                self.fields[field].required = False


# ================ FORMULAIRES POUR LES APPRENTIS ================

class ApprentiNonFormelForm(forms.ModelForm):
    """Formulaire pour les apprentis"""
    
    class Meta:
        model = ApprentiNonFormel
        exclude = ['structure', 'created_at', 'updated_at']
        widgets = {
            'secteur': forms.Select(attrs={'class': 'form-select'}),
            'duree_apprentissage': forms.Select(attrs={'class': 'form-select'}),
            'masculin': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'feminin': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'jeunes_inscrits_m': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'jeunes_inscrits_f': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'places_m': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'places_f': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'outilles_m': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'outilles_f': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
        }
    
    def clean(self):
        """Validation personnalisée"""
        cleaned_data = super().clean()
        
        # Vérifier que les jeunes inscrits ne dépassent pas les totaux
        jeunes_inscrits_m = cleaned_data.get('jeunes_inscrits_m', 0)
        jeunes_inscrits_f = cleaned_data.get('jeunes_inscrits_f', 0)
        
        if jeunes_inscrits_m > cleaned_data.get('masculin', 0):
            raise forms.ValidationError("Les jeunes inscrits M ne peuvent pas dépasser l'effectif M")
        
        if jeunes_inscrits_f > cleaned_data.get('feminin', 0):
            raise forms.ValidationError("Les jeunes inscrits F ne peuvent pas dépasser l'effectif F")
        
        return cleaned_data


# ================ FORMULAIRES POUR LES MÉTIERS ================

class MetierNonFormelForm(forms.ModelForm):
    """Formulaire pour les métiers"""
    
    class Meta:
        model = MetierNonFormel
        exclude = ['structure', 'created_at', 'updated_at']
        widgets = {
            'secteur': forms.Select(attrs={'class': 'form-select'}),
            'nom_metier': forms.TextInput(attrs={'class': 'form-control'}),
            'duree_apprentissage': forms.Select(attrs={'class': 'form-select'}),
            'promo_1_m': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'promo_1_f': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'promo_2_m': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'promo_2_f': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'promo_3_m': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'promo_3_f': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'handicapes_m': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'handicapes_f': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'refugies_m': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'refugies_f': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'retournes_m': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'retournes_f': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'deplaces_m': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'deplaces_f': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Rendre certains champs optionnels
        optional_fields = [
            'handicapes_m', 'handicapes_f', 'refugies_m', 'refugies_f',
            'retournes_m', 'retournes_f', 'deplaces_m', 'deplaces_f'
        ]
        for field in optional_fields:
            if field in self.fields:
                self.fields[field].required = False