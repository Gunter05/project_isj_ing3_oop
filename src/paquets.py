

class Paquet:
    def __init__(self, adresse_source, adresse_destination, protocole, taille, priorite, port_destination=None):
        self.adresse_source = adresse_source
        self.adresse_destination = adresse_destination
        self.protocole = protocole
        self.taille = taille
        self.priorite = priorite
        self.port_destination = port_destination

        self.trajet = []
        self.est_perdu = False

    def ajouter_saut(self, equipment):
        self.trajet.append(equipment)

    def marquer_perdu(self):
        self.est_perdu = True

    def __str__(self):
        return f"{self.protocole} {self.adresse_source} -> {self.adresse_destination}"