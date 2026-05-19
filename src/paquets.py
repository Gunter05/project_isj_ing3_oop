

class Paquet:
    def __init__(self, ip_source, ip_destination, protocole, taille, priorite):
        self.ip_source = ip_source
        self.ip_destination = ip_destination
        self.protocole = protocole
        self.taille = taille
        self.priorite = priorite
        self.trajet = []
        self.est_perdu = False

    def ajouter_saut(self, equipment):
        self.trajet.append(equipment)

    def marquer_perdu(self):
        self.est_perdu = True

    def __str__(self):
        return f"{self.protocole} {self.ip_source} -> {self.ip_destination}"