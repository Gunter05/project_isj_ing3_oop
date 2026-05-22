# ==============================
# IMPORTATIONS
# ==============================

from datetime import datetime
from enum import Enum

from equipements import Routeur, Switch, Serveur, PointAccesWifi, Terminal
from topologie import Topologie
from paquets import Paquet
from securite import Firewall as FirewallSecurite, RegleFiltrage, Protocole, Action
from moniteur import MoniteurReseau


# ==============================
# FIREWALL COMPATIBLE AVEC ABC
# ==============================
# La classe Firewall de securite.py hérite de Equipement.
# Si Equipement impose afficher_infos() en abstractmethod,
# il faut que le firewall possède aussi afficher_infos().

class FirewallPrincipal(FirewallSecurite):
    """Firewall principal utilisé dans l'interface console."""

    def afficher_infos(self):
        """Affiche les informations du firewall."""
        print(f"Nom : {self.nom}")
        print(f"IP : {self.adresse_ip}")
        print(f"Marque : {self.marque}")
        statut = "actif" if self.statut else "inactif"
        print(f"Statut : {statut}")
        print(f"Nombre de règles : {len(self.regles)}")
        print(f"Nombre de logs : {len(self.journal.logs)}")


# ==============================
# FONCTIONS UTILITAIRES
# ==============================

def saisir_entier(message, valeur_defaut=None):
    """Demande un entier à l'utilisateur avec gestion d'erreur."""
    while True:
        valeur = input(message)

        if valeur == "" and valeur_defaut is not None:
            return valeur_defaut

        try:
            return int(valeur)
        except ValueError:
            print("Veuillez entrer un nombre entier valide.")


def pause():
    """Pause simple pour améliorer la lisibilité."""
    input("\nAppuyez sur Entrée pour continuer...")


def afficher_liste_equipements(topologie):
    """Affiche tous les équipements de la topologie."""
    if not topologie.equipements:
        print("Aucun équipement dans la topologie.")
        return

    print("\n===== ÉQUIPEMENTS =====")
    for equipement in topologie.equipements:
        print(f"- {equipement}")


def afficher_liste_liens(topologie):
    """Affiche tous les liens de la topologie."""
    if not topologie.liens:
        print("Aucun lien dans la topologie.")
        return

    print("\n===== LIENS =====")
    for lien in topologie.liens:
        print(
            f"- {lien.equipement1.nom} <--> {lien.equipement2.nom} "
            f"({lien.bande_passante} Mbps, {lien.latence} ms)"
        )


def choisir_protocole():
    """Permet de choisir un protocole pour une règle de filtrage."""
    print("\nProtocole :")
    print("1. TCP")
    print("2. UDP")
    print("3. ICMP")
    print("4. Tous les protocoles")

    choix = input("Choix : ")

    if choix == "1":
        return Protocole.TCP
    if choix == "2":
        return Protocole.UDP
    if choix == "3":
        return Protocole.ICMP
    if choix == "4":
        return None

    print("Choix invalide. Tous les protocoles seront pris par défaut.")
    return None


def choisir_action():
    """Permet de choisir l'action d'une règle de filtrage."""
    print("\nAction :")
    print("1. Autoriser")
    print("2. Bloquer")

    choix = input("Choix : ")

    if choix == "1":
        return Action.AUTORISER
    if choix == "2":
        return Action.BLOQUER

    print("Choix invalide. Action BLOQUER prise par défaut.")
    return Action.BLOQUER


def enregistrer_resultat_moniteur(moniteur, paquet, resultat):
    """
    Enregistre le résultat d'un envoi de paquet dans le moniteur.

    Cette fonction est compatible avec la classe Paquet actuelle :
    adresse_source, adresse_destination, protocole, taille.
    """
    moniteur.paquets_envoyes += 1

    if not resultat["succes"]:
        moniteur.paquets_perdus += 1

    moniteur.debit_total += paquet.taille

    protocole = paquet.protocole.value if isinstance(paquet.protocole, Enum) else paquet.protocole

    evenement = {
        "date": datetime.now(),
        "source": paquet.adresse_source,
        "destination": paquet.adresse_destination,
        "protocole": protocole,
        "taille": paquet.taille,
        "message": resultat["message"]
    }

    moniteur.historique.append(evenement)

    if len(moniteur.historique) > 10:
        moniteur.historique.pop(0)


# ==============================
# MENUS
# ==============================

def menu_principal():
    print("\n===== SIMNET =====")
    print("1. Gestion des équipements")
    print("2. Gestion du réseau")
    print("3. Monitoring")
    print("4. Sécurité")
    print("5. Quitter")


def menu_equipement():
    print("\n===== GESTION DES ÉQUIPEMENTS =====")
    print("1. Ajouter un équipement")
    print("2. Afficher les informations d'un équipement")
    print("3. Connecter deux équipements")
    print("4. Supprimer un équipement")
    print("5. Afficher tous les équipements")
    print("0. Retour")


def menu_reseau():
    print("\n===== GESTION DU RÉSEAU =====")
    print("1. Afficher la topologie")
    print("2. Envoyer un paquet")
    print("3. Désactiver un équipement")
    print("4. Activer un équipement")
    print("5. Supprimer une route")
    print("6. Ajouter une interface")
    print("7. Ajouter un VLAN")
    print("8. Supprimer un VLAN")
    print("9. Ajouter un service")
    print("10. Supprimer un service")
    print("0. Retour")


def menu_monitoring():
    print("\n===== MONITORING =====")
    print("1. Afficher les statistiques")
    print("2. Afficher l'historique")
    print("3. Générer le rapport")
    print("0. Retour")


def menu_securite():
    print("\n===== SÉCURITÉ =====")
    print("1. Ajouter une règle de filtrage")
    print("2. Afficher le journal du firewall")
    print("3. Afficher les règles du firewall")
    print("0. Retour")


# ==============================
# GESTION DES ÉQUIPEMENTS
# ==============================

def ajouter_equipement(topologie):
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
        nombre_ports = saisir_entier("Nombre de ports : ")
        equipement = Routeur(nom, adresse_ip, marque, nombre_ports)

    elif choix == "2":
        nombre_ports = saisir_entier("Nombre de ports : ")
        equipement = Switch(nom, adresse_ip, marque, nombre_ports)

    elif choix == "3":
        equipement = Serveur(nom, adresse_ip, marque)

    elif choix == "4":
        type_terminal = input("Type de terminal (PC, smartphone, imprimante...) : ")
        utilisateur = input("Utilisateur : ")
        equipement = Terminal(nom, adresse_ip, marque, type_terminal, utilisateur)

    elif choix == "5":
        ssid = input("SSID : ")
        frequence = input("Fréquence Wi-Fi (ex: 2.4 ou 5) : ")
        equipement = PointAccesWifi(nom, adresse_ip, marque, ssid, frequence)

    elif choix == "6":
        equipement = FirewallPrincipal(adresse_ip, nom, marque)

    else:
        print("Choix invalide.")
        return

    equipement.activer()
    topologie.ajouter_equipement(equipement)
    print(f"{nom} ajouté avec succès.")


def afficher_infos_equipement(topologie):
    nom = input("Nom de l'équipement : ")
    equipement = topologie.trouver_equipement_par_nom(nom)

    if equipement is None:
        print("Équipement introuvable.")
        return

    print("\n===== INFORMATIONS =====")
    equipement.afficher_infos()


def connecter_equipements(topologie):
    afficher_liste_equipements(topologie)

    nom1 = input("\nNom du premier équipement : ")
    nom2 = input("Nom du second équipement : ")

    succes = topologie.connecter(nom1, nom2)

    if succes:
        print("Connexion réussie.")
    else:
        print("Connexion impossible. Vérifiez les noms ou les interfaces disponibles.")


def supprimer_equipement(topologie):
    nom = input("Nom de l'équipement à supprimer : ")

    if topologie.supprimer_equipement(nom):
        print("Équipement supprimé avec succès.")
    else:
        print("Équipement introuvable.")


def gestion_equipements(topologie):
    while True:
        menu_equipement()
        choix = input("Choix : ")

        if choix == "1":
            ajouter_equipement(topologie)
        elif choix == "2":
            afficher_infos_equipement(topologie)
        elif choix == "3":
            connecter_equipements(topologie)
        elif choix == "4":
            supprimer_equipement(topologie)
        elif choix == "5":
            afficher_liste_equipements(topologie)
        elif choix == "0":
            break
        else:
            print("Choix invalide.")

        pause()


# ==============================
# GESTION DU RÉSEAU
# ==============================

def afficher_topologie(topologie):
    print("\n===== TOPOLOGIE RÉSEAU =====")
    afficher_liste_equipements(topologie)
    afficher_liste_liens(topologie)


def envoyer_paquet(topologie, moniteur):
    print("\n===== ENVOI D'UN PAQUET =====")

    source = input("Adresse IP source : ")
    destination = input("Adresse IP destination : ")

    print("\nService à simuler :")
    print("1. web")
    print("2. https")
    print("3. ping")
    print("4. dns")
    print("5. fichier")

    choix_service = input("Choix : ")

    services = {
        "1": "web",
        "2": "https",
        "3": "ping",
        "4": "dns",
        "5": "fichier"
    }

    service = services.get(choix_service, "web")

    paquet = Paquet(
        adresse_source=source,
        adresse_destination=destination,
        service=service
    )

    resultat = topologie.envoyer_paquet(paquet)
    enregistrer_resultat_moniteur(moniteur, paquet, resultat)

    print("\n===== RÉSULTAT =====")
    print(resultat["message"])

    if resultat["chemin"]:
        chemin = " -> ".join(equipement.nom for equipement in resultat["chemin"])
        print(f"Chemin : {chemin}")

    print(f"Latence totale : {resultat['latence']} ms")
    print(f"Débit du chemin : {resultat['debit']} Mbps")


def desactiver_equipement(topologie):
    nom = input("Nom de l'équipement à désactiver : ")
    equipement = topologie.trouver_equipement_par_nom(nom)

    if equipement:
        equipement.desactiver()
    else:
        print("Équipement introuvable.")


def activer_equipement(topologie):
    nom = input("Nom de l'équipement à activer : ")
    equipement = topologie.trouver_equipement_par_nom(nom)

    if equipement:
        equipement.activer()
    else:
        print("Équipement introuvable.")


def supprimer_route(topologie):
    nom = input("Nom du routeur : ")
    routeur = topologie.trouver_equipement_par_nom(nom)

    if routeur is None:
        print("Routeur introuvable.")
        return

    if not hasattr(routeur, "supprimer_route"):
        print("Cet équipement ne gère pas de table de routage.")
        return

    destination = input("Destination à supprimer de la table de routage : ")
    routeur.supprimer_route(destination)


def ajouter_interface(topologie):
    nom = input("Nom de l'équipement : ")
    equipement = topologie.trouver_equipement_par_nom(nom)

    if equipement is None:
        print("Équipement introuvable.")
        return

    if not hasattr(equipement, "ajouter_interface"):
        print("Cet équipement ne possède pas de méthode ajouter_interface().")
        return

    interface = input("Nom de l'interface : ")
    equipement.ajouter_interface(interface)


def ajouter_vlan(topologie):
    nom = input("Nom du switch : ")
    switch = topologie.trouver_equipement_par_nom(nom)

    if switch is None:
        print("Switch introuvable.")
        return

    if not hasattr(switch, "ajouter_vlan"):
        print("Cet équipement ne gère pas les VLANs.")
        return

    vlan_id = saisir_entier("ID du VLAN : ")
    nom_vlan = input("Nom du VLAN : ")

    switch.ajouter_vlan(vlan_id, nom_vlan)


def supprimer_vlan(topologie):
    nom = input("Nom du switch : ")
    switch = topologie.trouver_equipement_par_nom(nom)

    if switch is None:
        print("Switch introuvable.")
        return

    if not hasattr(switch, "supprimer_vlan"):
        print("Cet équipement ne gère pas les VLANs.")
        return

    vlan_id = saisir_entier("ID du VLAN à supprimer : ")
    switch.supprimer_vlan(vlan_id)


def ajouter_service(topologie):
    nom = input("Nom du serveur : ")
    serveur = topologie.trouver_equipement_par_nom(nom)

    if serveur is None:
        print("Serveur introuvable.")
        return

    if not hasattr(serveur, "ajouter_service"):
        print("Cet équipement ne gère pas les services.")
        return

    service = input("Nom du service : ")
    serveur.ajouter_service(service)


def supprimer_service(topologie):
    nom = input("Nom du serveur : ")
    serveur = topologie.trouver_equipement_par_nom(nom)

    if serveur is None:
        print("Serveur introuvable.")
        return

    if not hasattr(serveur, "supprimer_service"):
        print("Cet équipement ne gère pas les services.")
        return

    service = input("Nom du service à supprimer : ")
    serveur.supprimer_service(service)


def gestion_reseau(topologie, moniteur):
    while True:
        menu_reseau()
        choix = input("Choix : ")

        if choix == "1":
            afficher_topologie(topologie)
        elif choix == "2":
            envoyer_paquet(topologie, moniteur)
        elif choix == "3":
            desactiver_equipement(topologie)
        elif choix == "4":
            activer_equipement(topologie)
        elif choix == "5":
            supprimer_route(topologie)
        elif choix == "6":
            ajouter_interface(topologie)
        elif choix == "7":
            ajouter_vlan(topologie)
        elif choix == "8":
            supprimer_vlan(topologie)
        elif choix == "9":
            ajouter_service(topologie)
        elif choix == "10":
            supprimer_service(topologie)
        elif choix == "0":
            break
        else:
            print("Choix invalide.")

        pause()


# ==============================
# MONITORING
# ==============================

def gestion_monitoring(moniteur):
    while True:
        menu_monitoring()
        choix = input("Choix : ")

        if choix == "1":
            moniteur.afficher_statistiques()
        elif choix == "2":
            moniteur.afficher_historique()
        elif choix == "3":
            moniteur.generer_rapport()
        elif choix == "0":
            break
        else:
            print("Choix invalide.")

        pause()


# ==============================
# SÉCURITÉ
# ==============================

def ajouter_regle_firewall(firewall):
    print("\n===== AJOUT D'UNE RÈGLE FIREWALL =====")

    ip_source = input("IP source ou début de plage à filtrer (laisser vide pour toutes) : ")
    if ip_source.strip() == "":
        ip_source = None

    protocole = choisir_protocole()

    port_texte = input("Port destination (laisser vide pour tous) : ")
    if port_texte.strip() == "":
        port_destination = None
    else:
        try:
            port_destination = int(port_texte)
        except ValueError:
            print("Port invalide. Le port sera ignoré.")
            port_destination = None

    action = choisir_action()

    login = input("Login administrateur : ")
    password = input("Mot de passe : ")

    regle = RegleFiltrage(
        ip_source=ip_source,
        protocole=protocole,
        port_destination=port_destination,
        action=action
    )

    if firewall.ajouter_regle(regle, login, password):
        print("Règle ajoutée avec succès.")
    else:
        print("Échec : authentification incorrecte.")


def afficher_journal_firewall(firewall):
    print("\n===== JOURNAL FIREWALL =====")
    print(firewall.journal.afficher())


def afficher_regles_firewall(firewall):
    print("\n===== RÈGLES FIREWALL =====")

    if not firewall.regles:
        print("Aucune règle configurée.")
        return

    for index, regle in enumerate(firewall.regles, start=1):
        print(f"{index}. {regle}")


def gestion_securite(firewall):
    while True:
        menu_securite()
        choix = input("Choix : ")

        if choix == "1":
            ajouter_regle_firewall(firewall)
        elif choix == "2":
            afficher_journal_firewall(firewall)
        elif choix == "3":
            afficher_regles_firewall(firewall)
        elif choix == "0":
            break
        else:
            print("Choix invalide.")

        pause()


# ==============================
# INITIALISATION DÉMO
# ==============================

def initialiser_reseau_demo(topologie):
    """
    Crée une petite topologie de démonstration pour tester rapidement le projet.
    """
    client = Terminal("Client-1", "192.168.1.10", "Dell", "PC", "Utilisateur")
    switch = Switch("SW-1", "192.168.1.2", "Cisco", 24)
    serveur = Serveur("SRV-1", "192.168.1.20", "HP")
    firewall = FirewallPrincipal("192.168.1.254", "FW-1", "Cisco")

    client.activer()
    switch.activer()
    serveur.activer()
    firewall.activer()

    topologie.ajouter_equipement(client)
    topologie.ajouter_equipement(switch)
    topologie.ajouter_equipement(firewall)
    topologie.ajouter_equipement(serveur)

    topologie.connecter("Client-1", "SW-1")
    topologie.connecter("SW-1", "FW-1")
    topologie.connecter("FW-1", "SRV-1")

    return firewall


# ==============================
# PROGRAMME PRINCIPAL
# ==============================

def main():
    topologie = Topologie()
    moniteur = MoniteurReseau()

    firewall_principal = initialiser_reseau_demo(topologie)

    print("SIMNet initialisé avec une topologie de démonstration.")
    print("Client-1 -> SW-1 -> FW-1 -> SRV-1")

    while True:
        menu_principal()
        choix = input("Choix : ")

        if choix == "1":
            gestion_equipements(topologie)
        elif choix == "2":
            gestion_reseau(topologie, moniteur)
        elif choix == "3":
            gestion_monitoring(moniteur)
        elif choix == "4":
            gestion_securite(firewall_principal)
        elif choix == "5":
            print("Fermeture du simulateur SIMNet.")
            break
        else:
            print("Choix invalide.")

        pause()


if __name__ == "__main__":
    main()