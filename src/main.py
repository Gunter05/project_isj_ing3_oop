#importations
from equipements import *  
from topologie import * 
from paquets import * 
from securite import * 
from moniteur import * 

#Affichage du menu
def afficher_menu():
    print("\n===== SIMNET =====")
    print("1. Ajouter un routeur")
    print("2. Connecter deux équipements")
    print("3. Afficher la topologie")
    print("4. Envoyer un paquet")
    print("5. Voir statistiques réseau")
    print("6. Voir historique réseau")
    print("7. Générer rapport")
    print("8. Quitter")

def main():
    #création de la topologie réseau
    topologie = Topologie()

    #création du système de monitoring
    moniteur = MoniteurReseau()

    #Création du firewall principal
    firewall = Firewall(
        "192.168.1.254",
        "FW-1",
        "Cisco"
    )

    #Activation du firewall
    #firewall.activer()

    while True :
        afficher_menu()
        choix= input("Choix : ")
        if choix == "1":
            nom = input("Nom du routeur : ")
            adresse_ip = input("Adresse IP : ")
            nombre_ports = int(input("Nombre de ports : "))
            routeur = Routeur(
                nom,
                adresse_ip,
                "Cisco",
                nombre_ports
            )
            routeur.activer()
            topologie.ajouter_equipement(routeur)
            print("Routeur ajouté avec succès.")
        elif choix == "2":
            nom1 = input("Premier équipement : ")
            nom2 = input("Second équipement : ")
            bande_passante = int(input("Bande passante : "))
            








