from collections import deque

class Lien:
    """ Représente un lien physique entre deux équipements """

    def __init__(self, equipement1, equipement2, latence, bande_passante):
        self.equipement1 = equipement1
        self.equipement2 = equipement2
        self.latence = latence
        self.bande_passante = bande_passante
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

    def connecter(self, nom1, nom2, bande_passante, latence):
        equipement1 = self.trouver_equipement_par_nom(nom1)
        equipement2 = self.trouver_equipement_par_nom(nom2)

        if equipement1 is None or equipement2 is None:
            return False

        lien = Lien(equipement1, equipement2, bande_passante, latence)
        self.liens.append(lien)
        return True

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