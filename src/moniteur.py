from datetime import datetime #récupération de la date et de l'heure actuelle

#Définition de la classe Moniteur
class MoniteurReseau:

    """Classe chargée de surveiller le réseau"""

    def __init__(self):
        #Initialisation
        self.paquets_envoyes = 0
        self.paquets_perdus = 0
        self.debit_total = 0 #exprimée en octets

        #Liste des derniers évènements réseau
        self.historique = []

    #Methode d'enregistrement du paquet
    def enregistrer_paquet(self,paquet):
        #incrémentation du nombre de paquets et du débit
        self.paquets_envoyes += 1
        self.debit_total += paquet.taille

        evenement ={
            "date": datetime.now(),
            "source": paquet.source,
            "destination": paquet.destination,
            "protocole": paquet.protocole,
            "taille": paquet.taille
        }

        #Ajout et gestion des évènements dans l'historique
        self.historique.append(evenement)
        
        if len(self.historique) >10:
            #j'enlève l'élément le plus ancien
            self.historique.pop(0)

    #Méthode qui signale un paquet perdu
    def enregistrer_perte(self):
        self.paquets_perdus += 1
    
    #Affichage des statistiques
    def afficher_statistiques(self):
        print("\n===== STATISTIQUES =====")
        print(f"Paquets envoyés : {self.paquets_envoyes}")
        print(f"Paquests perdus : {self.paquets_perdus}")
        print(f"Débit cumulé : {self.debit_total} octets")
    
    #Affichage des derniers évènements
    def afficher_historique(self):
        print("\n===== HISTORIQUE =====")
        for event in self.historique:
            print(
                f"{event['date']} | "
                f"{event['source']} -> {event['destination']} | "
                f"{event['protocole']} | "
                f"{event['taille']} octets"
            )
    
    #Rapport
    def generer_rapport(self):
        with open("rapport_simnet.txt", "w", encoding="utf-8") as fichier:
            fichier.write("====== RAPPORT SIMNET =====\n\n")
            fichier.write(
                f"Paquets envoyés : {self.paquets_envoyes}\n"
            )
            fichier.write(
                f"Paquets perdus : {self.paquets_perdus}\n"
            )
            fichier.write(
                f"Débit cumulé : {self.debit_total} octets\n\n"
            )
            fichier.write("===== HISTORIQUE =====\n")
            for event in self.historique:
                fichier.write(
                    f"{event['date']} | "
                    f"{event['source']} -> "
                    f"{event['destination']} | "
                    f"{event['protocole']} | "
                    f"{event['taille']} octets\n"
                )
        
        print("Rapport généré avec succès.")
        
#Test du fichier
if __name__ == "__main__":
    class FauxPaquet:
        def __init__(self):
            self.source = "192.168.1.1"
            self.destination = "192.168.1.2"
            self.protocole = "TCP"
            self.taille = 500
    
    #Création du moniteur
    moniteur = MoniteurReseau()

    #Création du paquet de test
    paquet = FauxPaquet()

    #Enregistrement du paquet
    moniteur.enregistrer_paquet(paquet)

    #Affichage des stats
    moniteur.afficher_statistiques()

    #Historique
    moniteur.afficher_historique()

    #Rapport
    moniteur.generer_rapport()











