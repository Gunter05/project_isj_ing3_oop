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
#option 2           
        elif choix == "2":
            nom1 = input("Premier équipement : ")
            nom2 = input("Second équipement : ")
            #Vérification de la présence des équipements
            if(topologie.trouver_equipement_par_nom(nom1)== None or topologie.trouver_equipement_par_nom(nom2) == None):
                print("Ces équipements n'appartiennent pas au réseau\n")
            #création du lien
            succes = topologie.connecter(nom1, nom2)
            if succes:
                print("connexion réussie\n")
            else:
                print("connexion impossible\n")
#option 3
        elif choix == "3":
            if len(topologie.equipements) == 0:
                print("Aucun équipement dans la topologie.")
            else:
                print("\n===== TOPOLOGIE =====")

            for equipement in topologie.equipements:
                print(equipement)
#option 4
        elif choix == "4":
            source = input("Adresse IP source : ")
            destination = input("Adresse IP destination : ")
            











