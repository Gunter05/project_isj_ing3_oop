from datetime import datetime
from enum import Enum

from equipements import Routeur, Switch, Serveur, PointAccesWifi, Terminal
from topologie import Topologie
from paquets import Paquet
from securite import Firewall as FirewallSecurite, RegleFiltrage, Protocole, Action
from moniteur import MoniteurReseau


class FirewallPrincipal(FirewallSecurite):
  
   # Firewall principal utilisé par SIMNet. Cette classe complète le Firewall de securite.py avec afficher_infos(), car Equipement impose cette méthode abstraite.
  
    def afficher_infos(self):
        print(f"Nom : {self.nom}")
        print(f"IP : {self.adresse_ip}")
        print(f"Marque : {self.marque}")
        print(f"Statut : {'actif' if self.statut else 'inactif'}")
        print(f"Nombre de règles : {len(self.regles)}")
        print(f"Nombre de logs : {len(self.journal.logs)}")


class SimulateurSIMNet:
   
   # Classe principale du simulateur SIMNet.
    def __init__(self):
        self.topologie = Topologie()
        self.moniteur = MoniteurReseau()
        self.firewall_principal = None

    #outils
    def pause(self):
        input("\nAppuyez sur Entrée pour continuer...")

    def saisir_entier(self, message, valeur_defaut=None):
        while True:
            valeur = input(message)

            if valeur == "" and valeur_defaut is not None:
                return valeur_defaut

            try:
                return int(valeur)
            except ValueError:
                print("Veuillez entrer un entier valide.")

    def afficher_menu(self, titre, options):
        print(f"\n===== {titre} =====")
        for cle, texte in options.items():
            print(f"{cle}. {texte}")

    def choisir_protocole(self):
        options = {
            "1": Protocole.TCP,
            "2": Protocole.UDP,
            "3": Protocole.ICMP,
            "4": None
        }

        print("\n1. TCP")
        print("2. UDP")
        print("3. ICMP")
        print("4. Tous")

        return options.get(input("Protocole : "), None)

    def choisir_action(self):
        print("\n1. Autoriser")
        print("2. Bloquer")

        choix = input("Action : ")

        if choix == "1":
            return Action.AUTORISER

        return Action.BLOQUER

   #equipements

    def ajouter_equipement(self):
        print("\nType d'équipement :")
        print("1. Routeur")
        print("2. Switch")
        print("3. Serveur")
        print("4. Terminal")
        print("5. Point d'accès Wi-Fi")
        print("6. Firewall")

        choix = input("Choix : ")

        nom = input("Nom : ")
        adresse_ip = input("Adresse IP : ")
        marque = input("Marque : ")

        equipement = None

        if choix == "1":
            ports = self.saisir_entier("Nombre de ports : ")
            equipement = Routeur(nom, adresse_ip, marque, ports)

        elif choix == "2":
            ports = self.saisir_entier("Nombre de ports : ")
            equipement = Switch(nom, adresse_ip, marque, ports)

        elif choix == "3":
            equipement = Serveur(nom, adresse_ip, marque)

        elif choix == "4":
            type_terminal = input("Type de terminal : ")
            utilisateur = input("Utilisateur : ")
            equipement = Terminal(nom, adresse_ip, marque, type_terminal, utilisateur)

        elif choix == "5":
            ssid = input("SSID : ")
            frequence = input("Fréquence Wi-Fi : ")
            equipement = PointAccesWifi(nom, adresse_ip, marque, ssid, frequence)

        elif choix == "6":
            equipement = FirewallPrincipal(adresse_ip, nom, marque)

        else:
            print("Choix invalide.")
            return

        equipement.activer()
        self.topologie.ajouter_equipement(equipement)

        if isinstance(equipement, FirewallPrincipal):
            self.firewall_principal = equipement

        print(f"{nom} ajouté avec succès.")

    def afficher_equipements(self):
        if not self.topologie.equipements:
            print("Aucun équipement dans le réseau.")
            return

        print("\n===== ÉQUIPEMENTS =====")
        for equipement in self.topologie.equipements:
            print(f"- {equipement}")

    def afficher_infos_equipement(self):
        nom = input("Nom de l'équipement : ")
        equipement = self.topologie.trouver_equipement_par_nom(nom)

        if equipement is None:
            print("Équipement introuvable.")
            return

        equipement.afficher_infos()

    def supprimer_equipement(self):
        nom = input("Nom de l'équipement à supprimer : ")

        if self.topologie.supprimer_equipement(nom):
            print("Équipement supprimé.")
        else:
            print("Équipement introuvable.")

    def activer_equipement(self):
        nom = input("Nom de l'équipement : ")
        equipement = self.topologie.trouver_equipement_par_nom(nom)

        if equipement:
            equipement.activer()
        else:
            print("Équipement introuvable.")

    def desactiver_equipement(self):
        nom = input("Nom de l'équipement : ")
        equipement = self.topologie.trouver_equipement_par_nom(nom)

        if equipement:
            equipement.desactiver()
        else:
            print("Équipement introuvable.")

   #topologie

    def connecter_equipements(self):
        self.afficher_equipements()

        nom1 = input("\nPremier équipement : ")
        nom2 = input("Second équipement : ")

        if self.topologie.connecter(nom1, nom2):
            print("Connexion réussie.")
        else:
            print("Connexion impossible.")

    def afficher_topologie(self):
        print("\n===== TOPOLOGIE =====")

        self.afficher_equipements()

        print("\n===== LIENS =====")
        if not self.topologie.liens:
            print("Aucun lien.")
            return

        for lien in self.topologie.liens:
            print(
                f"- {lien.equipement1.nom} <--> {lien.equipement2.nom} "
                f"({lien.bande_passante} Mbps, {lien.latence} ms)"
            )

    def envoyer_paquet(self):
        source = input("Adresse IP source : ")
        destination = input("Adresse IP destination : ")

        print("\nService :")
        print("1. web")
        print("2. https")
        print("3. ping")
        print("4. dns")
        print("5. fichier")

        services = {
            "1": "web",
            "2": "https",
            "3": "ping",
            "4": "dns",
            "5": "fichier"
        }

        service = services.get(input("Choix : "), "web")

        paquet = Paquet(
            adresse_source=source,
            adresse_destination=destination,
            service=service
        )

        resultat = self.topologie.envoyer_paquet(paquet)
        self.enregistrer_monitoring(paquet, resultat)

        print("\n===== RÉSULTAT =====")
        print(resultat["message"])

        if resultat["chemin"]:
            chemin = " -> ".join(equipement.nom for equipement in resultat["chemin"])
            print(f"Chemin : {chemin}")

        print(f"Latence : {resultat['latence']} ms")
        print(f"Débit : {resultat['debit']} Mbps")

   #routeur/VLAN/service

    def supprimer_route(self):
        routeur = self.demander_equipement("Nom du routeur : ")

        if routeur and hasattr(routeur, "supprimer_route"):
            destination = input("Destination à supprimer : ")
            routeur.supprimer_route(destination)
        else:
            print("Cet équipement ne gère pas les routes.")

    def ajouter_interface(self):
        equipement = self.demander_equipement("Nom de l'équipement : ")

        if equipement and hasattr(equipement, "ajouter_interface"):
            interface = input("Nom de l'interface : ")
            equipement.ajouter_interface(interface)
        else:
            print("Cet équipement ne gère pas les interfaces.")

    def ajouter_vlan(self):
        switch = self.demander_equipement("Nom du switch : ")

        if switch and hasattr(switch, "ajouter_vlan"):
            vlan_id = self.saisir_entier("ID VLAN : ")
            nom_vlan = input("Nom VLAN : ")
            switch.ajouter_vlan(vlan_id, nom_vlan)
        else:
            print("Cet équipement ne gère pas les VLANs.")

   