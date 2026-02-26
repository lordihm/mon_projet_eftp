from django.db import models
from apps.renaloc.models import Region, Departement, Commune, QuartierVillage

class EtablissementFormel(models.Model):
    # Identification
    nom = models.CharField(max_length=200)
    code = models.CharField(max_length=10, unique=True)
    
    STATUT_CHOICES = [
        ('PUBLIC', 'Public'),
        ('PRIVE', 'Privé'),
    ]
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES)
    
    ZONE_CHOICES = [
        ('URBAINE', 'Urbaine'),
        ('RURALE', 'Rurale'),
    ]
    zone = models.CharField(max_length=20, choices=ZONE_CHOICES)
    
    # Localisation administrative
    region = models.ForeignKey(Region, on_delete=models.PROTECT)
    departement = models.ForeignKey(Departement, on_delete=models.PROTECT)
    commune = models.ForeignKey(Commune, on_delete=models.PROTECT)
    quartier_village = models.ForeignKey(QuartierVillage, on_delete=models.PROTECT)
    adresse = models.CharField(max_length=255, blank=True)
    
    # Localisation pédagogique
    dre = models.CharField(max_length=100, blank=True, verbose_name="DRE/FT/P")
    ipde = models.CharField(max_length=100, blank=True, verbose_name="IPDE/FT/P")
    
    # Dates
    date_autorisation = models.DateField(null=True, blank=True)
    date_ouverture = models.DateField(null=True, blank=True)
    
    # Coordonnées
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    
    # Type d'établissement
    TYPE_ETABLISSEMENT_CHOICES = [
        ('LP', 'Lycée Professionnel'),
        ('LT', 'Lycée Technique'),
        ('LTE', 'Lycée Technologique'),
        ('LA', 'Lycée Agricole'),
        ('CFPT', 'CFPT'),
        ('CFPP', 'CFPP'),
        ('CMCAN', 'CMCAN'),
        ('EI', 'Ecole/Institut'),
        ('CET', 'CET'),
        ('CFM', 'CFM'),
        ('CPJ', 'CPJ'),
        ('EFAC', 'EFAC'),
        ('CFPT_AMA', 'CFPT AMA'),
        ('ENI', 'ENI'),
        ('CENTRE_MUSEE', 'Centre éducatif du musée national'),
        ('CFJA', 'CFJA'),
        ('CFMAA', 'CFMAA'),
    ]
    type_etablissement = models.CharField(max_length=20, choices=TYPE_ETABLISSEMENT_CHOICES)
    
    # Cycles
    cycle_base_1 = models.BooleanField(default=False, verbose_name="Base 1 (CQP)")
    cycle_base_2 = models.BooleanField(default=False, verbose_name="Base 2 (CAP)")
    cycle_moyen_1 = models.BooleanField(default=False, verbose_name="Moyen 1 (BEP)")
    cycle_moyen_2 = models.BooleanField(default=False, verbose_name="Moyen 2 (BAC - BEPC+4 - BAC+1)")
    
    # Régime
    REGIME_CHOICES = [
        ('INTERNAT', 'Internat'),
        ('EXTERNAT', 'Externat'),
    ]
    regime = models.CharField(max_length=20, choices=REGIME_CHOICES)
    internat_fonctionnel = models.BooleanField(null=True, blank=True)
    
    # Autres informations
    patrimoine_foncier = models.CharField(max_length=50, blank=True)
    ministere_tutelle = models.CharField(max_length=100, blank=True)
    type_formation = models.CharField(max_length=50, blank=True)
    dispositif_orientation = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Établissement formel"
        verbose_name_plural = "Établissements formels"
    
    def __str__(self):
        return f"{self.nom} - {self.code}"

class ApprenantFormel(models.Model):
    etablissement = models.ForeignKey(EtablissementFormel, on_delete=models.CASCADE, related_name='apprenants')
    
    CYCLE_CHOICES = [
        ('BASE_1', 'Base 1 (CQP)'),
        ('BASE_2', 'Base 2 (CAP)'),
        ('MOYEN_1', 'Moyen 1 (BEP)'),
        ('MOYEN_2', 'Moyen 2 (BAC - BEPC+4 - BAC+1)'),
    ]
    cycle = models.CharField(max_length=20, choices=CYCLE_CHOICES)
    
    ANNEE_ETUDE_CHOICES = [
        ('1ERE', '1ère année'),
        ('2EME', '2ème année'),
        ('3EME', '3ème année'),
        ('4EME', '4ème année'),
    ]
    annee_etude = models.CharField(max_length=10, choices=ANNEE_ETUDE_CHOICES)
    
    masculin = models.IntegerField(default=0)
    feminin = models.IntegerField(default=0)
    redoublants_m = models.IntegerField(default=0)
    redoublants_f = models.IntegerField(default=0)
    
    class Meta:
        verbose_name = "Apprenant formel"
        verbose_name_plural = "Apprenants formels"

class FiliereFormel(models.Model):
    etablissement = models.ForeignKey(EtablissementFormel, on_delete=models.CASCADE, related_name='filieres')
    
    SECTEUR_CHOICES = [
        ('PRIMAIRE', 'Secteur Primaire/Agricole'),
        ('SECONDAIRE', 'Secteur Secondaire/Industriel'),
        ('TERTIAIRE', 'Secteur Tertiaire/Service'),
    ]
    secteur = models.CharField(max_length=20, choices=SECTEUR_CHOICES)
    
    nom_filiere = models.CharField(max_length=200)
    diplome_prepare = models.CharField(max_length=200)
    cycle = models.CharField(max_length=20, choices=ApprenantFormel.CYCLE_CHOICES)
    
    duree_formation = models.IntegerField(help_text="Durée en mois")
    nb_groupes_pedagogiques = models.IntegerField(default=1)
    heures_pratique_hebdo = models.IntegerField(default=0)
    stage_obligatoire = models.BooleanField(default=False)
    
    effectif_m = models.IntegerField(default=0)
    effectif_f = models.IntegerField(default=0)
    
    class Meta:
        verbose_name = "Filière formelle"
        verbose_name_plural = "Filières formelles"
    
    def __str__(self):
        return self.nom_filiere

class FormateurFormel(models.Model):
    etablissement = models.ForeignKey(EtablissementFormel, on_delete=models.CASCADE, related_name='formateurs')
    
    STATUT_CHOICES = [
        ('FONCTIONNAIRE', 'Fonctionnaire'),
        ('CONTRACTUEL', 'Contractuel'),
        ('ASCN', 'ASCN'),
        ('PERMANENT', 'Permanent'),
        ('VOLONTAIRE', 'Volontaire/Bénévole'),
    ]
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES)
    
    NATIONALITE_CHOICES = [
        ('NIGERIENNE', 'Nigérienne'),
        ('ETRANGERE', 'Étrangère'),
    ]
    nationalite = models.CharField(max_length=20, choices=NATIONALITE_CHOICES)
    
    nom_prenom = models.CharField(max_length=200)
    sexe = models.CharField(max_length=1, choices=[('M', 'Masculin'), ('F', 'Féminin')])
    date_naissance = models.DateField()
    annee_recrutement = models.IntegerField()
    
    diplome_academique = models.CharField(max_length=100, blank=True)
    diplome_professionnel = models.CharField(max_length=100, blank=True)
    
    disciplines_enseignees = models.TextField()
    volume_horaire_hebdo = models.IntegerField()
    
    a_recu_renforcement = models.BooleanField(default=False)
    a_ete_inspecte = models.BooleanField(default=False)
    
    class Meta:
        verbose_name = "Formateur formel"
        verbose_name_plural = "Formateurs formels"