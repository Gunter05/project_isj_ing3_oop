from abc import ABC, abstractmethod
class Equipement(ABC):
    """Classe abstraite représentant un équipement réseau"""
    def __init__(self, nom, adresse_ip, marque):
        self._nom = nom
        self._adresse_ip = adresse_ip
        self._marque = marque
        self._statut = False

    @property
    def nom(self):
        return self._nom

    @property
    def adresse_ip(self):
        return self._adresse_ip

    @property
    def marque(self):
        return self._marque

    @property
    def statut(self):
        return self._statut

    def activer(self):
        """Active l'équipement"""
        self._statut = True
        print(f"{self._nom} est maintenant actif.")

    def desactiver(self):
        """Désactive l'équipement"""        
        self._statut = False
        print(f"{self._nom} est maintenant inctif.")

    @abstractmethod
    def afficher_infos(self):
        """Affiche les informations de l'équipement"""
        print(f"Nom : {self._nom}")
        print(f"IP : {self._adresse_ip}")
        print(f"Marque : {self._marque}")
        statut = "actif" if self._statut else "inactif"
        print(f"Statut : {statut}")
    
    def __str__(self):
        statut = "actif" if self._statut else "inactif"
        return f"{self._nom} ({self._marque}) - IP: {self._adresse_ip} - Statut: {statut}"


class Routeur(Equipement):
    """Classe représentant un routeur réseau"""
    def __init__(self, nom, adresse_ip, marque, nombre_ports):
        super().__init__(nom, adresse_ip, marque)
        self._nombre_ports = nombre_ports
        self._table_routage = {}
        self._interfaces = []
        
    def afficher_infos(self):
        """Affiche les informations du routeur""" 
        super().afficher_infos()
        print(f"Nombre de ports : {self._nombre_ports}")
        print(f"Table de routage : {self._table_routage}")  
        print(f"Interfaces : {self._interfaces}")

    def ajouter_route(self, destination, prochain_saut): 
        """Ajoute une route à la table de routage"""
        self._table_routage[destination] = prochain_saut
        print(f"Route ajoutée : {destination} -> {prochain_saut}")

    def supprimer_route(self, destination):
        """Supprime une route de la table de routage"""
        if destination in self._table_routage:
            del self._table_routage[destination]
            print(f"Route {destination}  supprimée.")
        else:
            print(f"Route{destination} introuvable")    


    def get_prochain_saut(self, destination):
        """Retourne le prochain saut pour une destination donnée"""
        return self._table_routage.get(destination, None)

    def ajouter_interface(self, interface):
        """Ajoute une interface au routeur"""
        if len(self._interfaces) < self._nombre_ports:
            self._interfaces.append(interface)
            print(f"Interface {interface} ajoutée au routeur {self._nom}.")
        else:
            print(f"Nombre maximum de ports atteint pour le routeur {self._nom}.")              


class Switch(Equipement):
    """Classe représentant un switch réseau"""
    def __init__(self, nom, adresse_ip, marque, nombre_ports):
        super().__init__(nom, adresse_ip, marque)
        self._nombre_ports = nombre_ports
        self._vlans = []
        
    def afficher_infos(self):
        """Affiche les informations du switch""" 
        super().afficher_infos()
        print(f"Nombre de ports : {self._nombre_ports}")
        print(f"VLANs : {self._vlans}")


    def ajouter_vlan(self, vlan_id, nom_vlan):
        """Ajoute un VLAN au switch"""
        vlan = {"id":vlan_id, "nom": nom_vlan}
        self._vlans.append(vlan)
        print(f"VLAN {vlan_id} - {nom_vlan} ajouté au switch {self._nom}.")
    

    def supprimer_vlan(self, vlan_id):
        """Supprime un VLAN du switch"""
        
        for vlan in self._vlans:
            if vlan["id"] == vlan_id:
                self._vlans.remove(vlan)
                print(f"VLAN {vlan_id} supprimé du switch {self._nom}.")
                return
        print(f"VLAN {vlan_id} introuvable sur le switch {self._nom}.")
        


class Serveur(Equipement):
    """Classe représentant un serveur réseau"""
    def __init__(self, nom, adresse_ip, marque):
        super().__init__(nom, adresse_ip, marque)
        self._services = []
        
    def afficher_infos(self):
        """Affiche les informations du serveur""" 
        super().afficher_infos()
        print(f"Services : {self._services}")    


    def ajouter_service(self, service):
        """Ajoute un service au serveur"""
        self._services.append(service)
        print(f"Service {service} ajouté au serveur {self._nom}.")


    def supprimer_service(self, service):
        """Supprime un service du serveur"""
        if service in self._services:
            self._services.remove(service)
            print(f"Service {service} supprimé du serveur {self._nom}.")
        else:
            print(f"Service {service} introuvable sur le serveur {self._nom}.")    



class Firewall(Equipement):
    """Classe représentant un firewall réseau"""
    def __init__(self, nom, adresse_ip, marque, login, password):
        super().__init__(nom, adresse_ip, marque)
        self._regles = []
        self._journal = []
        self._login = login
        self._password = password

    def afficher_infos(self):
        """Affiche les informations du firewall""" 
        super().afficher_infos()
        print(f"Nombres de règles : {len(self._regles)}")    
        print(f"Nombre d'entrées dans le journal : {len(self._journal)}")


    def authentifier(self, login, password):
        """Authentifie l'utilisateur pour accéder au firewall"""
        if login == self._login and password == self._password:
            print(f"Authentification réussie pour {self._nom}.")
            return True
        else:
            print(f"Authentification échouée pour {self._nom}.")
            return False
    
    
    def ajouter_regle(self, regle):
        """Ajoute une règle au firewall"""
        self._regles.append(regle)
        print(f"Règle {regle} ajoutée au firewall {self._nom}.")


    def supprimer_regle(self, regle):
        """Supprime une règle du firewall"""
        if regle in self._regles:
            self._regles.remove(regle)
            print(f"Règle {regle} supprimée du firewall {self._nom}.")
        else:
            print(f"Règle {regle} introuvable sur le firewall {self._nom}.")     


    def filtrer(self, paquet):
        """Filtre un paquet en fonction des règles du firewall"""
        for regle in self._regles:
            if regle.appliquer(paquet):
                self._journal.append(f"Paquet {paquet} bloqué par la règle {regle}.")
                print(f"Paquet {paquet} bloqué par la règle {regle}.")
                return False
        self._journal.append(f"Paquet {paquet} autorisé.")
        print(f"Paquet {paquet} autorisé.")
        return True
    


class PointAccesWifi(Equipement):
    """Classe représentant un point d'accès Wi-Fi"""
    def __init__(self, nom, adresse_ip, marque, ssid, frequence):
        super().__init__(nom, adresse_ip, marque)
        self._ssid = ssid
        self._clients_connectes = []
        self._frequence = frequence 
    def afficher_infos(self):
        """Affiche les informations du point d'accès Wi-Fi""" 
        super().afficher_infos()
        print(f"SSID : {self._ssid}")
        print(f"Clients connectés : {self._clients_connectes}")
        print(f"Fréquence : {self._frequence} GHz")


    def connecter_client(self, client):
        """Connecte un client au point d'accès Wi-Fi"""
        self._clients_connectes.append(client)
        print(f"Client {client} connecté au point d'accès {self._ssid}.")    


    def deconnecter_client(self, client):
        """Déconnecte un client du point d'accès Wi-Fi"""
        if client in self._clients_connectes:
            self._clients_connectes.remove(client)
            print(f"Client {client} déconnecté du point d'accès {self._ssid}.")
        else:
            print(f"Client {client} introuvable sur le point d'accès {self._ssid}.")    



class Terminal(Equipement):
    """Classe représentant un terminal client"""
    def __init__(self, nom, adresse_ip, marque, type_terminal, utilisateur):
        super().__init__(nom, adresse_ip, marque)
        self._type_terminal = type_terminal
        self._utilisateur = utilisateur
        
    def afficher_infos(self):
        """Affiche les informations du terminal""" 
        super().afficher_infos()
        print(f"Type de terminal : {self._type_terminal}")
        print(f"Utilisateur : {self._utilisateur}")   


    def envoyer(self, paquet):
        """Envoie un paquet depuis le terminal."""
        if self._statut:
            print(f"{self._nom} envoie un paquet vers {paquet._adresse_ip_dest}.")
            return True
        print(f"{self._nom} est inactif, impossible d'envoyer.")
        return False

    def recevoir(self, paquet):
        """Reçoit un paquet sur le terminal."""
        if self._statut:
            print(f"{self._nom} a reçu un paquet de {paquet._adresse_ip_src}.")
            return True
        print(f"{self._nom} est inactif, impossible de recevoir.")
        return False