from datetime import datetime #récupération de la date
from enum import Enum #pour les énumérations
#importations des classes
from equipements import Routeur, Switch, Serveur, PointAccesWifi, Terminal
from topologie import Topologie
from paquets import Paquet
from securite import Firewall as FirewallSecurite, RegleFiltrage, Protocole, Action
from moniteur import MoniteurReseau

from utils import valider_adresse_ip


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

    def saisir_adresse_ip(self, message):
        while True:
            adresse_ip = input(message)

            try:
                return valider_adresse_ip(adresse_ip)
            except ValueError as erreur:
                print(erreur)

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
        adresse_ip = self.saisir_adresse_ip("Adresse IP : ")
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
        if self.topologie.ajouter_equipement(equipement):
            print(f"{nom} ajouté avec succès.")
        else:
            print("Ajout impossible.")

        if isinstance(equipement, FirewallPrincipal):
            self.firewall_principal = equipement

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
        source = self.saisir_adresse_ip("Adresse IP source : ")
        destination = self.saisir_adresse_ip("Adresse IP destination : ")

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

    def supprimer_vlan(self):
        switch = self.demander_equipement("Nom du switch : ")

        if switch and hasattr(switch, "supprimer_vlan"):
            vlan_id = self.saisir_entier("ID VLAN : ")
            switch.supprimer_vlan(vlan_id)
        else:
            print("Cet équipement ne gère pas les VLANs.")

    def ajouter_service(self):
        serveur = self.demander_equipement("Nom du serveur : ")

        if serveur and hasattr(serveur, "ajouter_service"):
            service = input("Nom du service : ")
            serveur.ajouter_service(service)
        else:
            print("Cet équipement ne gère pas les services.")

    def supprimer_service(self):
        serveur = self.demander_equipement("Nom du serveur : ")

        if serveur and hasattr(serveur, "supprimer_service"):
            service = input("Service à supprimer : ")
            serveur.supprimer_service(service)
        else:
            print("Cet équipement ne gère pas les services.")

    def demander_equipement(self, message):
        nom = input(message)
        equipement = self.topologie.trouver_equipement_par_nom(nom)

        if equipement is None:
            print("Équipement introuvable.")

        return equipement

    # =========================
    # SÉCURITÉ
    # =========================

    def ajouter_regle_firewall(self):
        firewall = self.firewall_principal

        if firewall is None:
            print("Aucun firewall principal configuré.")
            return

        ip_source = input("IP source ou plage à filtrer, vide pour toutes : ")

        if ip_source.strip() == "":
            ip_source = None

        protocole = self.choisir_protocole()

        port = input("Port destination, vide pour tous : ")
        port_destination = int(port) if port.strip().isdigit() else None

        action = self.choisir_action()

        login = input("Login admin : ")
        password = input("Mot de passe : ")

        regle = RegleFiltrage(
            ip_source=ip_source,
            protocole=protocole,
            port_destination=port_destination,
            action=action
        )

        if firewall.ajouter_regle(regle, login, password):
            print("Règle ajoutée.")
        else:
            print("Authentification incorrecte.")

    def afficher_journal_firewall(self):
        if self.firewall_principal:
            print(self.firewall_principal.journal.afficher())
        else:
            print("Aucun firewall principal.")

    def afficher_regles_firewall(self):
        if not self.firewall_principal:
            print("Aucun firewall principal.")
            return

        if not self.firewall_principal.regles:
            print("Aucune règle configurée.")
            return

        for index, regle in enumerate(self.firewall_principal.regles, start=1):
            print(f"{index}. {regle}")

    # =========================
    # MONITORING
    # =========================

    def enregistrer_monitoring(self, paquet, resultat):
        """
        Enregistre un paquet dans le moniteur.

        Cette méthode corrige l'incompatibilité entre MoniteurReseau
        et Paquet : MoniteurReseau attend source/destination, alors que
        Paquet possède adresse_source/adresse_destination.
        """

        self.moniteur.paquets_envoyes += 1

        if not resultat["succes"]:
            self.moniteur.paquets_perdus += 1

        self.moniteur.debit_total += paquet.taille

        protocole = paquet.protocole.value if isinstance(paquet.protocole, Enum) else paquet.protocole

        evenement = {
            "date": datetime.now(),
            "source": paquet.adresse_source,
            "destination": paquet.adresse_destination,
            "protocole": protocole,
            "taille": paquet.taille,
            "message": resultat["message"]
        }

        self.moniteur.historique.append(evenement)

        if len(self.moniteur.historique) > 10:
            self.moniteur.historique.pop(0)

    def afficher_statistiques(self):
        self.moniteur.afficher_statistiques()

    def afficher_historique(self):
        self.moniteur.afficher_historique()

    def generer_rapport(self):
        self.moniteur.generer_rapport()

    # =========================
    # BOUCLES DE MENUS
    # =========================

    def gestion_equipements(self):
        actions = {
            "1": self.ajouter_equipement,
            "2": self.afficher_infos_equipement,
            "3": self.connecter_equipements,
            "4": self.supprimer_equipement,
            "5": self.afficher_equipements
        }

        while True:
            self.afficher_menu("GESTION DES ÉQUIPEMENTS", {
                "1": "Ajouter un équipement",
                "2": "Afficher les informations d'un équipement",
                "3": "Connecter deux équipements",
                "4": "Supprimer un équipement",
                "5": "Afficher tous les équipements",
                "0": "Retour"
            })

            choix = input("Choix : ")

            if choix == "0":
                break

            action = actions.get(choix)

            if action:
                action()
            else:
                print("Choix invalide.")

            self.pause()

    def gestion_reseau(self):
        actions = {
            "1": self.afficher_topologie,
            "2": self.envoyer_paquet,
            "3": self.desactiver_equipement,
            "4": self.activer_equipement,
            "5": self.supprimer_route,
            "6": self.ajouter_interface,
            "7": self.ajouter_vlan,
            "8": self.supprimer_vlan,
            "9": self.ajouter_service,
            "10": self.supprimer_service
        }

        while True:
            self.afficher_menu("GESTION DU RÉSEAU", {
                "1": "Afficher la topologie",
                "2": "Envoyer un paquet",
                "3": "Désactiver un équipement",
                "4": "Activer un équipement",
                "5": "Supprimer une route",
                "6": "Ajouter une interface",
                "7": "Ajouter un VLAN",
                "8": "Supprimer un VLAN",
                "9": "Ajouter un service",
                "10": "Supprimer un service",
                "0": "Retour"
            })

            choix = input("Choix : ")

            if choix == "0":
                break

            action = actions.get(choix)

            if action:
                action()
            else:
                print("Choix invalide.")

            self.pause()

    def gestion_monitoring(self):
        actions = {
            "1": self.afficher_statistiques,
            "2": self.afficher_historique,
            "3": self.generer_rapport
        }

        while True:
            self.afficher_menu("MONITORING", {
                "1": "Afficher les statistiques",
                "2": "Afficher l'historique",
                "3": "Générer le rapport",
                "0": "Retour"
            })

            choix = input("Choix : ")

            if choix == "0":
                break

            action = actions.get(choix)

            if action:
                action()
            else:
                print("Choix invalide.")

            self.pause()

    def gestion_securite(self):
        actions = {
            "1": self.ajouter_regle_firewall,
            "2": self.afficher_journal_firewall,
            "3": self.afficher_regles_firewall
        }

        while True:
            self.afficher_menu("SÉCURITÉ", {
                "1": "Ajouter une règle de filtrage",
                "2": "Afficher le journal du firewall",
                "3": "Afficher les règles du firewall",
                "0": "Retour"
            })

            choix = input("Choix : ")

            if choix == "0":
                break

            action = actions.get(choix)

            if action:
                action()
            else:
                print("Choix invalide.")

            self.pause()

    def lancer(self):
        print("SIMNet initialisé.")
        print("Topologie de démonstration : Client-1 -> SW-1 -> FW-1 -> SRV-1")

        actions = {
            "1": self.gestion_equipements,
            "2": self.gestion_reseau,
            "3": self.gestion_monitoring,
            "4": self.gestion_securite
        }

        while True:
            self.afficher_menu("SIMNET", {
                "1": "Gestion des équipements",
                "2": "Gestion du réseau",
                "3": "Monitoring",
                "4": "Sécurité",
                "5": "Quitter"
            })

            choix = input("Choix : ")

            if choix == "5":
                print("Fermeture du simulateur SIMNet.")
                break

            action = actions.get(choix)

            if action:
                action()
            else:
                print("Choix invalide.")

            self.pause()


def main():
    simulateur = SimulateurSIMNet()
    simulateur.lancer()


if __name__ == "__main__":
    main()