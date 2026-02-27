from django import forms
from .models import EtablissementFormel, ApprenantFormel, FormateurFormel, FiliereFormel
from apps.renaloc.models import Region, Departement, Commune, QuartierVillage


class EtablissementFormelSimpleForm(forms.ModelForm):
    """Formulaire simplifié pour la création initiale d'un établissement"""
    class Meta:
        model = EtablissementFormel
        fields = ['code', 'nom', 'sigle', 'statut', 'zone', 'region', 'departement', 'commune', 
                  'quartier_village', 'adresse']
        widgets = {
            'adresse': forms.Textarea(attrs={'rows': 2, 'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Ajouter la classe form-control à tous les champs
        for field_name, field in self.fields.items():
            if isinstance(field.widget, (forms.Select, forms.SelectMultiple)):
                field.widget.attrs['class'] = 'form-select'
            else:
                field.widget.attrs['class'] = 'form-control'
            
            # Ajouter des placeholders
            if field_name == 'nom':
                field.widget.attrs['placeholder'] = "Nom complet de l'établissement"
            elif field_name == 'sigle':
                field.widget.attrs['placeholder'] = "Ex: LP, LT, CFPT..."
            elif field_name == 'code':
                field.widget.attrs['placeholder'] = "Code unique"
            
            # Rendre certains champs optionnels
            if field_name in ['quartier_village', 'adresse', 'sigle']:
                field.required = False

class EtablissementFormelCompletForm(forms.ModelForm):
    """Formulaire complet pour saisir toutes les données de l'établissement"""
    class Meta:
        model = EtablissementFormel
        fields = '__all__'
        widgets = {
            'date_autorisation': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'date_ouverture': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'longitude': forms.NumberInput(attrs={'step': 'any', 'class': 'form-control', 
                                                  'placeholder': 'Ex: 2.123456'}),
            'latitude': forms.NumberInput(attrs={'step': 'any', 'class': 'form-control', 
                                                 'placeholder': 'Ex: 13.123456'}),
            'adresse': forms.Textarea(attrs={'rows': 2, 'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Ajouter la classe form-control à tous les champs
        for field_name, field in self.fields.items():
            if field_name not in ['date_autorisation', 'date_ouverture', 'longitude', 'latitude']:
                if isinstance(field.widget, (forms.Select, forms.SelectMultiple)):
                    field.widget.attrs['class'] = 'form-select'
                else:
                    field.widget.attrs['class'] = 'form-control'
            
            # Ajouter des placeholders
            if field_name == 'nom':
                field.widget.attrs['placeholder'] = "Nom complet de l'établissement"
            elif field_name == 'sigle':
                field.widget.attrs['placeholder'] = "Ex: LP, LT, CFPT..."
            elif field_name == 'code':
                field.widget.attrs['placeholder'] = "Code unique"
            
            # Rendre certains champs optionnels
            if field_name in ['quartier_village', 'dre', 'ipde', 'adresse', 'longitude', 'latitude', 
                             'date_autorisation', 'date_ouverture', 'internat_fonctionnel', 
                             'patrimoine_foncier', 'ministere_tutelle', 'type_formation', 'sigle']:
                field.required = False


class ApprenantFormelForm(forms.ModelForm):
    class Meta:
        model = ApprenantFormel
        fields = ['cycle', 'annee_etude', 'masculin', 'feminin', 'redoublants_m', 'redoublants_f']
        widgets = {
            'cycle': forms.Select(attrs={'class': 'form-select'}),
            'annee_etude': forms.Select(attrs={'class': 'form-select'}),
            'masculin': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'feminin': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'redoublants_m': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'redoublants_f': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
        }
    
    def clean(self):
        cleaned_data = super().clean()
        masculin = cleaned_data.get('masculin', 0)
        feminin = cleaned_data.get('feminin', 0)
        redoublants_m = cleaned_data.get('redoublants_m', 0)
        redoublants_f = cleaned_data.get('redoublants_f', 0)
        
        if redoublants_m > masculin:
            raise forms.ValidationError("Les redoublants masculins ne peuvent pas dépasser l'effectif masculin")
        
        if redoublants_f > feminin:
            raise forms.ValidationError("Les redoublants féminins ne peuvent pas dépasser l'effectif féminin")
        
        return cleaned_data

class FormateurFormelForm(forms.ModelForm):
    class Meta:
        model = FormateurFormel
        exclude = ['etablissement']
        widgets = {
            'nom_prenom': forms.TextInput(attrs={'class': 'form-control'}),
            'sexe': forms.Select(attrs={'class': 'form-select'}),
            'date_naissance': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'annee_recrutement': forms.NumberInput(attrs={'class': 'form-control', 'min': 1900, 'max': 2100}),
            'statut': forms.Select(attrs={'class': 'form-select'}),
            'nationalite': forms.Select(attrs={'class': 'form-select'}),
            'diplome_academique': forms.TextInput(attrs={'class': 'form-control'}),
            'diplome_professionnel': forms.TextInput(attrs={'class': 'form-control'}),
            'disciplines_enseignees': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'volume_horaire_hebdo': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'a_recu_renforcement': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'a_ete_inspecte': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class FiliereFormelForm(forms.ModelForm):
    class Meta:
        model = FiliereFormel
        exclude = ['etablissement']
        widgets = {
            'nom_filiere': forms.TextInput(attrs={'class': 'form-control'}),
            'secteur': forms.Select(attrs={'class': 'form-select'}),
            'diplome_prepare': forms.TextInput(attrs={'class': 'form-control'}),
            'cycle': forms.Select(attrs={'class': 'form-select'}),
            'duree_formation': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'nb_groupes_pedagogiques': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'heures_pratique_hebdo': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'stage_obligatoire': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'effectif_m': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'effectif_f': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
        }                