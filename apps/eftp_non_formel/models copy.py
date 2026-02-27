from django.db import models
from apps.renaloc.models import Region, Departement, Commune, QuartierVillage

class StructureNonFormelle(models.Model):
    # Identification
    nom = models.CharField(max_length=200)
    code = models.CharField(max_length=10, unique=True)
    
    # Document administratif
    a_document = models.BooleanField(default=False)
    ministere_tutelle = models.CharField(max_length=100, blank=True)
    type_document = models.CharField(max_length=100, blank=True)
    reference_document = models.CharField(max_length=100, blank=True)
    
    date_autorisation = models.DateField(null=True, blank=True)
    date_ouverture = models.DateField(null=True, blank=True)
    
    # Localisation
    region = models.ForeignKey(Region, on_delete=models.PROTECT)
    departement = models.ForeignKey(Departement, on_delete=models.PROTECT)
    commune = models.ForeignKey(Commune, on_delete=models.PROTECT)
    quartier_village = models.ForeignKey(QuartierVillage, on_delete=models.PROTECT)
    
    ZONE_CHOICES = [
        ('URBAINE', 'Urbaine'),
        ('RURALE', 'Rurale'),
    ]
    zone = models.CharField(max_length=20, choices=ZONE_CHOICES)
    
    STATUT_CHOICES = [
        ('PUBLIC', 'Public'),
        ('PRIVE', 'Privé'),
    ]
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES)
    
    # Type de structure
    TYPE_STRUCTURE_CHOICES = [
        ('SFMA', 'SFMA (SIFA)'),
        ('CFA', 'CFA'),
        ('ATELIER', 'Atelier'),
        ('SAA', 'SAA'),
        ('FOYER', 'Foyer'),
        ('GROUPEMENT', 'Groupement'),
        ('GARAGE', 'Garage'),
        ('COOPERATIVE', 'Coopérative/Association'),
        ('CABINET', 'Cabinet de formation'),
        ('PLATEFORME', "Plateforme d'orientation"),
        ('AUTRE', 'Autre structure'),
    ]
    type_structure = models.CharField(max_length=20, choices=TYPE_STRUCTURE_CHOICES)
    autre_type_precision = models.CharField(max_length=200, blank=True)
    
    # Financement
    SOURCE_FINANCEMENT_CHOICES = [
        ('ETAT', "État"),
        ('PTFS', "PTFs"),
        ('FAFPA', "FAFPA"),
        ('EPA', "EPA"),
        ('ONGS', "ONGs"),
        ('ASSOCIATIONS', "Associations"),
        ('FONDS_PROPRES', "Fonds propres"),
        ('AUTRE', "Autre"),
    ]
    source_financement = models.JSONField(default=list)  # Pour stocker plusieurs choix
    
    # Régime
    REGIME_CHOICES = [
        ('INTERNAT', 'Internat'),
        ('EXTERNAT', 'Externat'),
    ]
    regime = models.CharField(max_length=20, choices=REGIME_CHOICES)
    
    delivre_attestation = models.BooleanField(default=False)
    
    # Pour les plateformes
    TYPE_ACCOMPAGNEMENT_CHOICES = [
        ('ESPECES', 'En espèces'),
        ('MATERIEL', 'En matériel et outillage technique'),
        ('RENFORCEMENT', 'Renforcement des capacités techniques'),
        ('PLACEMENT', 'Placement'),
        ('AUTRE', 'Autre'),
    ]
    type_accompagnement = models.JSONField(default=list, blank=True)
    
    formation_payante = models.BooleanField(default=False)
    MODE_PAIEMENT_CHOICES = [
        ('ESPECES', 'Paiement en espèces'),
        ('CHEQUE', 'Paiement en chèque'),
        ('LIGNE', 'Paiement en ligne'),
        ('NATURE', 'Paiement en nature'),
    ]
    mode_paiement = models.JSONField(default=list, blank=True)
    
    # Coordonnées
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    
    # Équipements et services
    a_electricite = models.BooleanField(default=False)
    SOURCE_ELECTRICITE_CHOICES = [
        ('GROUPE', 'Groupe électrogène'),
        ('SOLAIRE', 'Panneau solaire'),
        ('RESEAU', 'Réseau électrique'),
    ]
    source_electricite = models.CharField(max_length=20, choices=SOURCE_ELECTRICITE_CHOICES, blank=True)
    
    a_point_eau = models.BooleanField(default=False)
    SOURCE_EAU_CHOICES = [
        ('ROBINET', 'Robinet'),
        ('AEP', 'AEP'),
        ('FORAGE', 'Forage'),
        ('PUITS', 'Puits cimenté'),
    ]
    source_eau = models.CharField(max_length=20, choices=SOURCE_EAU_CHOICES, blank=True)
    
    a_cloture = models.BooleanField(default=False)
    a_infirmerie = models.BooleanField(default=False)
    a_boite_pharmacie = models.BooleanField(default=False)
    a_depotoir = models.BooleanField(default=False)
    nombre_depotoirs = models.IntegerField(default=0)
    a_rampes_handicapes = models.BooleanField(default=False)
    a_cour_recreation = models.BooleanField(default=False)
    a_latrines = models.BooleanField(default=False)
    nombre_latrines = models.IntegerField(default=0)
    latrines_apprenants = models.IntegerField(default=0)
    latrines_filles = models.IntegerField(default=0)
    latrines_personnel = models.IntegerField(default=0)
    latrines_handicapes = models.IntegerField(default=0)
    a_bibliotheque = models.BooleanField(default=False)
    a_connexion_internet = models.BooleanField(default=False)
    type_connexion = models.CharField(max_length=50, blank=True)
    acces_internet = models.JSONField(default=list, blank=True)
    a_terrain_sport = models.BooleanField(default=False)
    a_paysage = models.BooleanField(default=False)
    a_parking = models.BooleanField(default=False)
    a_lavage_mains = models.BooleanField(default=False)
    a_collecte_ordures = models.BooleanField(default=False)
    
    nb_maitres_artisans_h = models.IntegerField(default=0)
    nb_maitres_artisans_f = models.IntegerField(default=0)
    nb_formateurs_h = models.IntegerField(default=0)
    nb_formateurs_f = models.IntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Structure non formelle"
        verbose_name_plural = "Structures non formelles"
    
    def __str__(self):
        return f"{self.nom} - {self.code}"

class ApprentiNonFormel(models.Model):
    structure = models.ForeignKey(StructureNonFormelle, on_delete=models.CASCADE, related_name='apprentis')
    
    SECTEUR_CHOICES = [
        ('PRIMAIRE', 'Secteur Primaire/Agricole'),
        ('SECONDAIRE', 'Secteur Secondaire/Industriel'),
        ('TERTIAIRE', 'Secteur Tertiaire/Service'),
    ]
    secteur = models.CharField(max_length=20, choices=SECTEUR_CHOICES)
    
    DUREE_CHOICES = [
        ('<=3', '≤ 3 mois'),
        ('4-9', '4 à 9 mois'),
        ('>9', '> 9 mois'),
    ]
    duree_apprentissage = models.CharField(max_length=5, choices=DUREE_CHOICES)
    
    masculin = models.IntegerField(default=0)
    feminin = models.IntegerField(default=0)
    
    # Jeunes accompagnés (pour les plateformes)
    jeunes_inscrits_m = models.IntegerField(default=0)
    jeunes_inscrits_f = models.IntegerField(default=0)
    places_m = models.IntegerField(default=0)
    places_f = models.IntegerField(default=0)
    outilles_m = models.IntegerField(default=0)
    outilles_f = models.IntegerField(default=0)
    
    class Meta:
        verbose_name = "Apprenti non formel"
        verbose_name_plural = "Apprentis non formels"

class MaitreArtisan(models.Model):
    structure = models.ForeignKey(StructureNonFormelle, on_delete=models.CASCADE, related_name='maitres_artisans')
    
    nom_prenom = models.CharField(max_length=200)
    sexe = models.CharField(max_length=1, choices=[('M', 'Masculin'), ('F', 'Féminin')])
    
    GRADE_CHOICES = [
        ('MAITRE', 'Maître artisan'),
        ('FORMATEUR', 'Formateur'),
    ]
    grade = models.CharField(max_length=20, choices=GRADE_CHOICES)
    
    formation_initiale = models.BooleanField(default=False)
    nb_formation_continue = models.IntegerField(default=0)
    
    qualification_certifiee = models.BooleanField(default=False)
    dernier_certificat = models.CharField(max_length=200, blank=True)
    niveau_certificat = models.CharField(max_length=100, blank=True)
    structure_certifiante = models.CharField(max_length=200, blank=True)
    annee_certification = models.IntegerField(null=True, blank=True)
    
    NATIONALITE_CHOICES = [
        ('NIGERIEN', 'Nigérien'),
        ('UEMOA', 'UEMOA'),
        ('AUTRE', 'Autre'),
    ]
    nationalite = models.CharField(max_length=20, choices=NATIONALITE_CHOICES, default='NIGERIEN')
    
    a_recu_suivi = models.BooleanField(default=False)
    
    class Meta:
        verbose_name = "Maître artisan"
        verbose_name_plural = "Maîtres artisans"
    
    def __str__(self):
        return self.nom_prenom

class MetierNonFormel(models.Model):
    structure = models.ForeignKey(StructureNonFormelle, on_delete=models.CASCADE, related_name='metiers')
    
    SECTEUR_CHOICES = [
        ('PRIMAIRE', 'Secteur Primaire/Agricole'),
        ('SECONDAIRE', 'Secteur Secondaire/Industriel'),
        ('TERTIAIRE', 'Secteur Tertiaire/Service'),
    ]
    secteur = models.CharField(max_length=20, choices=SECTEUR_CHOICES)
    
    nom_metier = models.CharField(max_length=200)
    duree_apprentissage = models.CharField(max_length=5, choices=ApprentiNonFormel.DUREE_CHOICES)
    
    # Promotions
    promo_1_m = models.IntegerField(default=0, verbose_name="Promotion I M")
    promo_1_f = models.IntegerField(default=0, verbose_name="Promotion I F")
    promo_2_m = models.IntegerField(default=0, verbose_name="Promotion II M")
    promo_2_f = models.IntegerField(default=0, verbose_name="Promotion II F")
    promo_3_m = models.IntegerField(default=0, verbose_name="Promotion III M")
    promo_3_f = models.IntegerField(default=0, verbose_name="Promotion III F")
    
    # Catégories spéciales
    handicapes_m = models.IntegerField(default=0)
    handicapes_f = models.IntegerField(default=0)
    refugies_m = models.IntegerField(default=0)
    refugies_f = models.IntegerField(default=0)
    retournes_m = models.IntegerField(default=0)
    retournes_f = models.IntegerField(default=0)
    deplaces_m = models.IntegerField(default=0)
    deplaces_f = models.IntegerField(default=0)
    
    class Meta:
        verbose_name = "Métier non formel"
        verbose_name_plural = "Métiers non formels"
    
    def __str__(self):
        return self.nom_metier