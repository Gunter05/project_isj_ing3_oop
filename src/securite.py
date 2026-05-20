import datetime
from enum import Enum

class Action(Enum):
    """
    Énumération pour définir l'action d'une règle de filtrage.
    Permet de standardiser les décisions du firewall (AUTORISER ou BLOQUER).
    """
    AUTORISER = "AUTORISER"
    BLOQUER = "BLOQUER"

class RegleFiltrage:
    """classe qui représente une règle de filtrage unitaire pour le Firewall, elle permet de définir des critères basés sur l'IP source, le protocole, 
    le port de destination et l'action associée"""
    
    def __init__(self, ip_source=None, protocole=None, port_destination=None, action=Action.BLOQUER):
        """ Initialise une règle de filtrage[cite: 240].
        Les attributs qui sont None font office de joker (concernent toutes les valeurs).
        """
        self.ip_source = ip_source  
        self.protocole = protocole  
        self.port_destination = port_destination  
        self.action = action  

    def __str__(self):
        """C'est la surcharge de la méthode __str__ pour faciliter l'affichage des règles dans les logs et les interfaces de gestion."""
        return f"Règle [{self.action.value}] -> IP Src: {self.ip_source or 'Tout'}, Protocole: {self.protocole or 'Tout'}, Port Dest: {self.port_destination or 'Tout'}"


class JournalFirewall:
    """   Gère l'historique et la journalisation des décisions du Firewall, enregistre les détails de chaque paquet inspecté avec un horodatage précis """
    
    def __init__(self):
        """Initialise une liste vide pour stocker les entrées de log."""
        self.logs = []

    def ajouter_log(self, paquet, action, raison):
        """Crée et ajoute une entrée horodatée dans le journal """
        horodatage = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{horodatage}] Paquet [{paquet.adresse_source} -> {paquet.adresse_destination} | {paquet.protocole}] - Action: {action.value} ({raison})"
        self.logs.append(log_entry)

    def afficher(self):
        """
        Retourne l'ensemble des logs sous forme de chaîne de caractères pour l'affichage console. """
        if not self.logs:
            return "Le journal du firewall est vide."
        return "\n".join(self.logs)


class Authentification:
    """  Gère l'accès sécurisé à la configuration du Firewall. Vérifie les identifiants d'administration (login et mot de passe)"""
    
    def __init__(self, login_par_defaut="admin", password_par_defaut="admin123"):
        """Initialise les identifiants d'accès d'administration ."""
        self._login = login_par_defaut
        self._password = password_par_defaut
        self.est_authentifie = False

    def se_connecter(self, login, password):
        """ Vérifie les identifiants fournis et connecte l'utilisateur si valides. """
        if login == self._login and password == self._password:
            self.est_authentifie = True
            return True
        self.est_authentifie = False
        return False

    def se_deconnecter(self):
        """Déconnecte l'utilisateur et réinitialise l'état d'authentification."""
        self.est_authentifie = False


# Note d'intégration : On importe la classe mère Equipement rédigée par le Membre A.
# Si le fichier equipements.py est encore vide chez le Membre A, vous pouvez temporairement 
# créer une classe Equipement vide dans son fichier pour éviter les erreurs d'import.
from src.equipements import Equipement

class Firewall(Equipement):
    """ Équipement réseau de sécurité chargé de filtrer les paquets de données. Hérite de la classe Equipement et implémente les fonctionnalités de filtrage,
    d'authentification et de journalisation.  """
    
    def __init__(self, adresse_ip, nom, marque):
        """ Initialise le Firewall avec ses attributs d'équipement et ses modules de sécurité. """
        super().__init__(adresse_ip, nom, marque)
        self.regles = []  # Liste pour stocker les instances de RegleFiltrage, ce sont les regles du firewall
        self.journal = JournalFirewall()  # Module de logs pour enregistrer les décisions de filtrage et les événements importants
        self.auth = Authentification()  # Module de sécurité d'accès 

    def ajouter_regle(self, regle, login, password):        
        """ Permet d'ajouter une règle de filtrage si l'administrateur s'authentifie correctement. """
        if self.auth.se_connecter(login, password) or self.auth.est_authentifie:
            self.regles.append(regle)
            return True
        return False

    def filtrer(self, paquet):
        """Examine un paquet entrant et applique la politique de sécurité.  
        Compare le paquet aux règles existantes et journalise le résultat.
        Retourne True si le paquet est autorisé, False s'il est bloqué. """

        # Politique par défaut : Si aucune règle ne correspond, on autorise le paquet
        action_finale = Action.AUTORISER
        raison = "Aucune règle correspondante (Autorisation par défaut)"

        # Parcours des règles selon le principe "First Match" (première règle correspondante appliquée)
        for regle in self.regles:
            # Vérification de l'IP Source (gère l'adresse exacte ou le début d'une plage réseau) 
            match_ip = regle.ip_source is None or paquet.adresse_source.startswith(regle.ip_source)
            
            # Vérification du protocole 
            match_proto = regle.protocole is None or paquet.protocole.upper() == regle.protocole.upper()
            
            # Vérification sécurisée du port de destination (évite les crashs si l'attribut n'existe pas) 
            port_paquet = getattr(paquet, 'port_destination', None)
            match_port = regle.port_destination is None or port_paquet == regle.port_destination

            # Si le paquet correspond à tous les critères définis dans la règle
            if match_ip and match_proto and match_port:
                action_finale = regle.action
                raison = f"Correspondance avec la règle: {regle}"
                break  # Règle trouvée, on arrête l'analyse pour ce paquet


        # Enregistrement systématique de la décision dans le journal 
        self.journal.ajouter_log(paquet, action_finale, raison)
        
        return action_finale == Action.AUTORISER
    