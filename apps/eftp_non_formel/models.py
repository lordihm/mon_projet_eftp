from django.db import models
from apps.renaloc.models import Region, Departement, Commune, QuartierVillage

class StructureNonFormelle(models.Model):
    """Modèle pour les structures d'EFTP non formel"""
    
    # Identification
    nom = models.CharField(max_length=200, verbose_name="Nom de la structure")
    sigle = models.CharField(max_length=20, blank=True, verbose_name="Sigle")
    code = models.CharField(max_length=10, unique=True, verbose_name="Code")
    
    # Document administratif
    a_document = models.BooleanField(default=False, verbose_name="Document administratif")
    ministere_tutelle = models.CharField(max_length=100, blank=True, verbose_name="Ministère de tutelle")
    type_document = models.CharField(max_length=100, blank=True, verbose_name="Type de document")
    reference_document = models.CharField(max_length=100, blank=True, verbose_name="Référence du document")
    
    # Dates
    date_autorisation = models.DateField(null=True, blank=True, verbose_name="Date d'autorisation")
    date_ouverture = models.DateField(null=True, blank=True, verbose_name="Date d'ouverture")
    
    # Localisation
    region = models.ForeignKey(Region, on_delete=models.PROTECT, verbose_name="Région")
    departement = models.ForeignKey(Departement, on_delete=models.PROTECT, verbose_name="Département")
    commune = models.ForeignKey(Commune, on_delete=models.PROTECT, verbose_name="Commune")
    quartier_village = models.ForeignKey(QuartierVillage, on_delete=models.PROTECT, null=True, blank=True, 
                                        verbose_name="Quartier/Village")
    adresse = models.CharField(max_length=255, blank=True, verbose_name="Adresse")
    
    ZONE_CHOICES = [
        ('URBAINE', 'Urbaine'),
        ('RURALE', 'Rurale'),
    ]
    zone = models.CharField(max_length=20, choices=ZONE_CHOICES, verbose_name="Zone")
    
    STATUT_CHOICES = [
        ('PUBLIC', 'Public'),
        ('PRIVE', 'Privé'),
    ]
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, verbose_name="Statut")
    
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
    type_structure = models.CharField(max_length=20, choices=TYPE_STRUCTURE_CHOICES, verbose_name="Type de structure")
    autre_type_precision = models.CharField(max_length=200, blank=True, verbose_name="Précision autre type")
    
    # Financement (JSON pour stocker plusieurs choix)
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
    source_financement = models.JSONField(default=list, blank=True, verbose_name="Sources de financement")
    
    # Régime
    REGIME_CHOICES = [
        ('INTERNAT', 'Internat'),
        ('EXTERNAT', 'Externat'),
    ]
    regime = models.CharField(max_length=20, choices=REGIME_CHOICES, default='EXTERNAT', verbose_name="Régime")
    
    delivre_attestation = models.BooleanField(default=False, verbose_name="Délivre des attestations")
    
    # Pour les plateformes (accompagnement)
    TYPE_ACCOMPAGNEMENT_CHOICES = [
        ('ESPECES', 'En espèces'),
        ('MATERIEL', 'En matériel et outillage technique'),
        ('RENFORCEMENT', 'Renforcement des capacités techniques'),
        ('PLACEMENT', 'Placement'),
        ('AUTRE', 'Autre'),
    ]
    type_accompagnement = models.JSONField(default=list, blank=True, verbose_name="Types d'accompagnement")
    
    formation_payante = models.BooleanField(default=False, verbose_name="Formation payante")
    MODE_PAIEMENT_CHOICES = [
        ('ESPECES', 'Paiement en espèces'),
        ('CHEQUE', 'Paiement en chèque'),
        ('LIGNE', 'Paiement en ligne'),
        ('NATURE', 'Paiement en nature'),
    ]
    mode_paiement = models.JSONField(default=list, blank=True, verbose_name="Modes de paiement")
    
    # Coordonnées GPS
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True, verbose_name="Longitude")
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True, verbose_name="Latitude")
    
    # Équipements et services
    a_electricite = models.BooleanField(default=False, verbose_name="Alimentation électrique")
    SOURCE_ELECTRICITE_CHOICES = [
        ('GROUPE', 'Groupe électrogène'),
        ('SOLAIRE', 'Panneau solaire'),
        ('RESEAU', 'Réseau électrique'),
    ]
    source_electricite = models.CharField(max_length=20, choices=SOURCE_ELECTRICITE_CHOICES, blank=True, verbose_name="Source électricité")
    
    a_point_eau = models.BooleanField(default=False, verbose_name="Point d'eau potable")
    SOURCE_EAU_CHOICES = [
        ('ROBINET', 'Robinet'),
        ('AEP', 'AEP'),
        ('FORAGE', 'Forage'),
        ('PUITS', 'Puits cimenté'),
    ]
    source_eau = models.CharField(max_length=20, choices=SOURCE_EAU_CHOICES, blank=True, verbose_name="Source eau")
    
    a_cloture = models.BooleanField(default=False, verbose_name="Clôture")
    a_infirmerie = models.BooleanField(default=False, verbose_name="Infirmerie fonctionnelle")
    a_boite_pharmacie = models.BooleanField(default=False, verbose_name="Boîte à pharmacie")
    a_depotoir = models.BooleanField(default=False, verbose_name="Dépotoir")
    nombre_depotoirs = models.IntegerField(default=0, verbose_name="Nombre de dépotoirs")
    a_rampes_handicapes = models.BooleanField(default=False, verbose_name="Rampes pour handicapés")
    a_cour_recreation = models.BooleanField(default=False, verbose_name="Cour de récréation")
    
    a_latrines = models.BooleanField(default=False, verbose_name="Latrines")
    nombre_latrines = models.IntegerField(default=0, verbose_name="Nombre total de latrines")
    latrines_apprenants = models.IntegerField(default=0, verbose_name="Latrines pour apprenants")
    latrines_filles = models.IntegerField(default=0, verbose_name="Latrines pour filles")
    latrines_personnel = models.IntegerField(default=0, verbose_name="Latrines pour personnel")
    latrines_handicapes = models.IntegerField(default=0, verbose_name="Latrines pour handicapés")
    
    a_bibliotheque = models.BooleanField(default=False, verbose_name="Bibliothèque")
    a_connexion_internet = models.BooleanField(default=False, verbose_name="Connexion Internet")
    TYPE_CONNEXION_CHOICES = [
        ('ADSL', 'ADSL'),
        ('VSAT', 'VSAT'),
        ('MOBILE', 'Connexion mobile'),
        ('FIBRE', 'Fibre optique'),
        ('AUTRE', 'Autre'),
    ]
    type_connexion = models.CharField(max_length=20, choices=TYPE_CONNEXION_CHOICES, blank=True, verbose_name="Type de connexion")
    
    # Accès Internet (JSON)
    ACCES_INTERNET_CHOICES = [
        ('APPRENTIS', 'Apprentis'),
        ('FORMATEURS', 'Formateurs'),
        ('ADMIN', 'Personnel administratif'),
        ('EXTERNE', 'Externe'),
    ]
    acces_internet = models.JSONField(default=list, blank=True, verbose_name="Accès Internet")
    
    a_terrain_sport = models.BooleanField(default=False, verbose_name="Terrain de sport")
    a_paysage = models.BooleanField(default=False, verbose_name="Aménagement paysagé")
    a_parking = models.BooleanField(default=False, verbose_name="Parking")
    a_lavage_mains = models.BooleanField(default=False, verbose_name="Dispositif lavage mains")
    a_collecte_ordures = models.BooleanField(default=False, verbose_name="Collecte des ordures")
    
    # Personnel
    nb_maitres_artisans_h = models.IntegerField(default=0, verbose_name="Maîtres artisans H")
    nb_maitres_artisans_f = models.IntegerField(default=0, verbose_name="Maîtres artisans F")
    nb_formateurs_h = models.IntegerField(default=0, verbose_name="Formateurs H")
    nb_formateurs_f = models.IntegerField(default=0, verbose_name="Formateurs F")
    
    # Métadonnées
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True, verbose_name="Date de création")
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True, verbose_name="Date de modification")    
    
    class Meta:
        ordering = ['code']
        verbose_name = "Structure non formelle"
        verbose_name_plural = "Structures non formelles"
    
    def __str__(self):
        if self.sigle:
            return f"{self.sigle} - {self.nom}"
        return self.nom
    
    def get_completion_percentage(self):
        """Calcule le pourcentage de complétude de la structure"""
        champs_importants = [
            'nom', 'code', 'statut', 'zone', 'region', 'departement', 'commune',
            'type_structure', 'regime', 'date_autorisation', 'date_ouverture',
            'longitude', 'latitude', 'a_electricite', 'a_point_eau', 'a_latrines'
        ]
        
        filled = 0
        for champ in champs_importants:
            value = getattr(self, champ)
            if value not in [None, '', False, []]:
                filled += 1
        
        total = len(champs_importants)
        return int((filled / total) * 100) if total > 0 else 0


class MaitreArtisan(models.Model):
    """Modèle pour les maîtres artisans / formateurs du non formel"""
    
    structure = models.ForeignKey(StructureNonFormelle, on_delete=models.CASCADE, related_name='maitres_artisans')
    
    nom_prenom = models.CharField(max_length=200, verbose_name="Nom et prénom")
    
    SEXE_CHOICES = [
        ('M', 'Masculin'),
        ('F', 'Féminin'),
    ]
    sexe = models.CharField(max_length=1, choices=SEXE_CHOICES, verbose_name="Sexe")
    
    GRADE_CHOICES = [
        ('MAITRE', 'Maître artisan'),
        ('FORMATEUR', 'Formateur'),
    ]
    grade = models.CharField(max_length=20, choices=GRADE_CHOICES, verbose_name="Grade")
    
    formation_initiale = models.BooleanField(default=False, verbose_name="Formation initiale")
    nb_formation_continue = models.IntegerField(default=0, verbose_name="Nombre de formations continues")
    
    qualification_certifiee = models.BooleanField(default=False, verbose_name="Qualification certifiée")
    dernier_certificat = models.CharField(max_length=200, blank=True, verbose_name="Dernier certificat")
    niveau_certificat = models.CharField(max_length=100, blank=True, verbose_name="Niveau du certificat")
    structure_certifiante = models.CharField(max_length=200, blank=True, verbose_name="Structure certifiante")
    annee_certification = models.IntegerField(null=True, blank=True, verbose_name="Année de certification")
    
    NATIONALITE_CHOICES = [
        ('NIGERIEN', 'Nigérien'),
        ('UEMOA', 'UEMOA'),
        ('AUTRE', 'Autre'),
    ]
    nationalite = models.CharField(max_length=20, choices=NATIONALITE_CHOICES, default='NIGERIEN', verbose_name="Nationalité")
    
    a_recu_suivi = models.BooleanField(default=False, verbose_name="A reçu un suivi technico-pédagogique")
    
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)    

    class Meta:
        ordering = ['nom_prenom']
        verbose_name = "Maître artisan"
        verbose_name_plural = "Maîtres artisans"
    
    def __str__(self):
        return f"{self.nom_prenom} - {self.structure.nom}"


class ApprentiNonFormel(models.Model):
    """Modèle pour les apprentis du non formel"""
    
    structure = models.ForeignKey(StructureNonFormelle, on_delete=models.CASCADE, related_name='apprentis')
    
    SECTEUR_CHOICES = [
        ('PRIMAIRE', 'Secteur Primaire/Agricole'),
        ('SECONDAIRE', 'Secteur Secondaire/Industriel'),
        ('TERTIAIRE', 'Secteur Tertiaire/Service'),
    ]
    secteur = models.CharField(max_length=20, choices=SECTEUR_CHOICES, verbose_name="Secteur")
    
    DUREE_CHOICES = [
        ('<=3', '≤ 3 mois'),
        ('4-9', '4 à 9 mois'),
        ('>9', '> 9 mois'),
    ]
    duree_apprentissage = models.CharField(max_length=5, choices=DUREE_CHOICES, verbose_name="Durée d'apprentissage")
    
    masculin = models.IntegerField(default=0, verbose_name="Masculin")
    feminin = models.IntegerField(default=0, verbose_name="Féminin")
    
    # Jeunes accompagnés (pour les plateformes)
    jeunes_inscrits_m = models.IntegerField(default=0, verbose_name="Jeunes inscrits M")
    jeunes_inscrits_f = models.IntegerField(default=0, verbose_name="Jeunes inscrits F")
    places_m = models.IntegerField(default=0, verbose_name="Placés M")
    places_f = models.IntegerField(default=0, verbose_name="Placés F")
    outilles_m = models.IntegerField(default=0, verbose_name="Outillés M")
    outilles_f = models.IntegerField(default=0, verbose_name="Outillés F")
    
    # CORRIGÉ
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        ordering = ['secteur', 'duree_apprentissage']
        verbose_name = "Apprenti non formel"
        verbose_name_plural = "Apprentis non formels"
    
    def __str__(self):
        return f"{self.structure.nom} - {self.get_secteur_display()}"


class MetierNonFormel(models.Model):
    """Modèle pour les métiers enseignés dans le non formel"""
    
    structure = models.ForeignKey(StructureNonFormelle, on_delete=models.CASCADE, related_name='metiers')
    
    SECTEUR_CHOICES = [
        ('PRIMAIRE', 'Secteur Primaire/Agricole'),
        ('SECONDAIRE', 'Secteur Secondaire/Industriel'),
        ('TERTIAIRE', 'Secteur Tertiaire/Service'),
    ]
    secteur = models.CharField(max_length=20, choices=SECTEUR_CHOICES, verbose_name="Secteur")
    
    nom_metier = models.CharField(max_length=200, verbose_name="Nom du métier")
    DUREE_CHOICES = [
        ('<=3', '≤ 3 mois'),
        ('4-9', '4 à 9 mois'),
        ('>9', '> 9 mois'),
    ]
    duree_apprentissage = models.CharField(max_length=5, choices=DUREE_CHOICES, verbose_name="Durée d'apprentissage")
    
    # Promotions
    promo_1_m = models.IntegerField(default=0, verbose_name="Promotion I M")
    promo_1_f = models.IntegerField(default=0, verbose_name="Promotion I F")
    promo_2_m = models.IntegerField(default=0, verbose_name="Promotion II M")
    promo_2_f = models.IntegerField(default=0, verbose_name="Promotion II F")
    promo_3_m = models.IntegerField(default=0, verbose_name="Promotion III M")
    promo_3_f = models.IntegerField(default=0, verbose_name="Promotion III F")
    
    # Catégories spéciales
    handicapes_m = models.IntegerField(default=0, verbose_name="Handicapés M")
    handicapes_f = models.IntegerField(default=0, verbose_name="Handicapés F")
    refugies_m = models.IntegerField(default=0, verbose_name="Réfugiés M")
    refugies_f = models.IntegerField(default=0, verbose_name="Réfugiés F")
    retournes_m = models.IntegerField(default=0, verbose_name="Retournés M")
    retournes_f = models.IntegerField(default=0, verbose_name="Retournés F")
    deplaces_m = models.IntegerField(default=0, verbose_name="Déplacés M")
    deplaces_f = models.IntegerField(default=0, verbose_name="Déplacés F")
    
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    
    class Meta:
        ordering = ['secteur', 'nom_metier']
        verbose_name = "Métier non formel"
        verbose_name_plural = "Métiers non formels"
    
    def __str__(self):
        return self.nom_metier
    
    def total_promo_1(self):
        return self.promo_1_m + self.promo_1_f
    
    def total_promo_2(self):
        return self.promo_2_m + self.promo_2_f
    
    def total_promo_3(self):
        return self.promo_3_m + self.promo_3_f
    
    def total_apprentis(self):
        return self.total_promo_1() + self.total_promo_2() + self.total_promo_3()