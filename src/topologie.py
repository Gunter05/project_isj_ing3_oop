from collections import deque

class Lien:
    """ Représente un lien physique entre deux équipements """

    def __init__(self, equipement1, equipement2, bande_passante=100, latence=5):
        self.equipement1 = equipement1
        self.equipement2 = equipement2
        self.latence = latence # en ms
        self.bande_passante = bande_passante # en Mbps
        self.actif = True

    def connecte(self, equipement):
        return self.equipement1 == equipement or self.equipement2 == equipement

    def autre_extremite(self, equipement):
        if self.equipement1 == equipement:
            return self.equipement2
        elif self.equipement2 == equipement:
            return self.equipement1
        else:
            return None

    def __str__(self):
        return f"{self.equipement1.nom} <--> {self.equipement2.nom}"

class Topologie:
    def __init__(self):
        self.equipements = []
        self.liens = []

    def ajouter_equipement(self, equipement):
        self.equipements.append(equipement)

    def supprimer_equipement(self, nom):
        equipement = self.trouver_equipement_par_nom(nom)

        if equipement:
            self.equipements.remove(equipement)
            self.liens = [
                lien for lien in self.liens
                if lien.equipement1 != equipement and lien.equipement2 != equipement
            ]
            return True

        return False

    def trouver_equipement_par_nom(self, nom):
        for equipement in self.equipements:
            if equipement.nom == nom:
                return equipement
        return None

    def trouver_equipement_par_ip(self, ip):
        for equipement in self.equipements:
            if equipement.ip == ip:
                return equipement
        return None

    def connecter(self, nom1, nom2, bande_passante=None, latence=None):
        equipement1 = self.trouver_equipement_par_nom(nom1)
        equipement2 = self.trouver_equipement_par_nom(nom2)

        if equipement1 is None or equipement2 is None:
            return False

        if bande_passante is None or latence is None:
            bande_passante, latence = self.determiner_caracteristiques_lien(
                equipement1,
                equipement2
            )

        lien = Lien(equipement1, equipement2, bande_passante, latence)
        self.liens.append(lien)
        return True

    def determiner_caracteristiques_lien(self, equipement1, equipement2):
        noms_classes = {
            equipement1.__class__.__name__,
            equipement2.__class__.__name__
        }

        if "PointAccesWifi" in noms_classes:
            return 54, 15

        if "Switch" in noms_classes and "Serveur" in noms_classes:
            return 1000, 2

        if "Switch" in noms_classes and "Routeur" in noms_classes:
            return 1000, 5

        if "Routeur" in noms_classes:
            return 100, 10

        return 100, 5

    def obtenir_voisins(self, equipement):
        voisins = []

        for lien in self.liens:
            if lien.actif and lien.connecte(equipement):
                voisin = lien.autre_extremite(equipement)
                if voisin is not None and voisin.statut:
                    voisins.append(voisin)

        return voisins

    def trouver_chemin(self, source, destination):
        file = deque()
        visites = set()

        file.append((source, [source]))
        visites.add(source)

        while file:
            equipement_actuel, chemin = file.popleft()

            if equipement_actuel == destination:
                return chemin

            for voisin in self.obtenir_voisins(equipement_actuel):
                if voisin not in visites:
                    visites.add(voisin)
                    file.append((voisin, chemin + [voisin]))

        return None

    def envoyer_paquet(self, paquet):
        source = self.trouver_equipement_par_ip(paquet.adresse_source)
        destination = self.trouver_equipement_par_ip(paquet.adresse_destination)

        if source is None:
            paquet.marquer_perdu()
            return {
                "succes": False,
                "message": "Source introuvable",
                "chemin": [],
                "latence": 0,
                "debit": 0
            }

        if destination is None:
            paquet.marquer_perdu()
            return {
                "succes": False,
                "message": "Destination introuvable",
                "chemin": [],
                "latence": 0,
                "debit": 0
            }

        chemin = self.trouver_chemin(source, destination)

        if chemin is None:
            paquet.marquer_perdu()
            return {
                "succes": False,
                "message": "Destination inatteignable",
                "chemin": [],
                "latence": 0,
                "debit": 0
            }

        for equipement in chemin:
            paquet.ajouter_saut(equipement)

            if hasattr(equipement, "filtrer"):
                autorise = equipement.filtrer(paquet)
                if not autorise:
                    paquet.marquer_perdu()
                    return {
                        "succes": False,
                        "message": "Paquet bloqué par le firewall",
                        "chemin": paquet.trajet,
                        "latence": self.calculer_latence_chemin(paquet.trajet),
                        "debit": self.calculer_debit_chemin(paquet.trajet)
                    }

        return {
            "succes": True,
            "message": "Paquet transmis avec succès",
            "chemin": paquet.trajet,
            "latence": self.calculer_latence_chemin(chemin),
            "debit": self.calculer_debit_chemin(chemin)
        }

    def obtenir_lien(self, equipement1, equipement2):
        for lien in self.liens:
            if (
                lien.equipement1 == equipement1 and lien.equipement2 == equipement2
            ) or (
                lien.equipement1 == equipement2 and lien.equipement2 == equipement1
            ):
                return lien

        return None

    def calculer_latence_chemin(self, chemin):
        latence_totale = 0

        for i in range(len(chemin) - 1):
            lien = self.obtenir_lien(chemin[i], chemin[i+1])
            if lien:
                latence_totale += lien.latence

        return latence_totale

    def calculer_debit_chemin(self, chemin):
        debits = []

        for i in range(len(chemin) - 1):
            lien = self.obtenir_lien(chemin[i], chemin[i+1])
            if lien:
                debits.append(lien.bande_passante)

        if not debits:
            return 0

        return min(debits)