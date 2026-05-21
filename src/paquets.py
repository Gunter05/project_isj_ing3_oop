try:
    from securite import Protocole
except ImportError:
    from enum import Enum

    class Protocole(Enum):
        """
        Représente les protocoles réseau pris en charge par SIMNet.

        Attributs:
            TCP (str): Protocole de contrôle de transmission (orienté connexion).
            UDP (str): Protocole de datagramme utilisateur (non orienté connexion).
            ICMP (str): Protocole de message de contrôle Internet (utilisé pour ping).
        """
        TCP = "TCP"
        UDP = "UDP"
        ICMP = "ICMP"


class Paquet:
    """
    Représente un paquet réseau circulant dans SIMNet.

    Le protocole, la taille et le port peuvent être générés automatiquement
    à partir du type de service demandé.

    Attributs:
        adresse_source (str): L'adresse IP de l'équipement émetteur.
        adresse_destination (str): L'adresse IP de l'équipement récepteur.
        service (str): Le service associé au paquet (ex. 'web', 'https', 'ping', 'dns', 'fichier').
        protocole (Protocole/str): Le protocole de transport utilisé.
        taille (int): La taille du paquet en octets.
        priorite (int): La priorité du paquet (de 1 à 5).
        port_destination (int): Le port réseau de destination.
        trajet (list): Liste des équipements traversés par le paquet.
        est_perdu (bool): Indique si le paquet a été perdu en cours de route.
    """

    SERVICES = {
        "web": {
            "protocole": Protocole.TCP,
            "port_destination": 80,
            "taille": 512,
            "priorite": 3
        },
        "https": {
            "protocole": Protocole.TCP,
            "port_destination": 443,
            "taille": 768,
            "priorite": 3
        },
        "ping": {
            "protocole": Protocole.ICMP,
            "port_destination": None,
            "taille": 64,
            "priorite": 5
        },
        "dns": {
            "protocole": Protocole.UDP,
            "port_destination": 53,
            "taille": 128,
            "priorite": 4
        },
        "fichier": {
            "protocole": Protocole.TCP,
            "port_destination": 21,
            "taille": 1500,
            "priorite": 2
        }
    }

    def __init__(
        self,
        adresse_source,
        adresse_destination,
        service="web",
        protocole=None,
        taille=None,
        priorite=None,
        port_destination=None
    ):
        """
        Initialise un nouveau paquet réseau avec ses caractéristiques.

        Si des paramètres spécifiques (protocole, taille, priorite, port_destination)
        ne sont pas fournis, ils seront déduits du type de service indiqué.

        Entrées:
            adresse_source (str): Adresse IP de l'expéditeur.
            adresse_destination (str): Adresse IP du destinataire.
            service (str, optionnel): Type de service réseau (ex: "web", "https", "ping", "dns", "fichier"). Par défaut "web".
            protocole (Protocole, optionnel): Protocole de transport (TCP, UDP, ICMP). Par défaut None (déduit du service).
            taille (int, optionnel): Taille du paquet en octets. Par défaut None (déduite du service).
            priorite (int, optionnel): Priorité du paquet de 1 (faible) à 5 (haute). Par défaut None (déduite du service).
            port_destination (int, optionnel): Port de destination. Par défaut None (déduit du service).

        Sortie:
            None (Initialise l'instance).

        Exceptions:
            ValueError: Si la priorité finale n'est pas comprise entre 1 et 5.
        """
        self.adresse_source = adresse_source
        self.adresse_destination = adresse_destination
        self.service = service.lower()

        caracteristiques = self.SERVICES.get(self.service, self.SERVICES["web"])

        self.protocole = protocole if protocole is not None else caracteristiques["protocole"]
        self.taille = taille if taille is not None else caracteristiques["taille"]
        self.priorite = priorite if priorite is not None else caracteristiques["priorite"]
        self.port_destination = (
            port_destination
            if port_destination is not None
            else caracteristiques["port_destination"]
        )

        if self.priorite < 1 or self.priorite > 5:
            raise ValueError("La priorité doit être comprise entre 1 et 5.")

        self.trajet = []
        self.est_perdu = False

    def ajouter_saut(self, equipement):
        """
        Ajoute un équipement réseau au trajet parcouru par le paquet.

        Entrée:
            equipement (Equipement): L'équipement réseau actuellement traversé.

        Sortie:
            None.
        """
        self.trajet.append(equipement)

    def marquer_perdu(self):
        """
        Marque le paquet comme étant perdu ou bloqué lors de son acheminement.

        Entrée:
            Aucune.

        Sortie:
            None.
        """
        self.est_perdu = True

    def __str__(self):
        """
        Retourne une représentation textuelle détaillée du paquet pour le débogage.

        Entrée:
            Aucune.

        Sortie:
            str: Description textuelle contenant le protocole, source, destination, service, taille, priorité et port.
        """
        protocole = self.protocole.value if isinstance(self.protocole, Enum) else self.protocole

        return (
            f"Paquet {protocole} "
            f"{self.adresse_source} -> {self.adresse_destination} "
            f"| service={self.service}, taille={self.taille} octets, "
            f"priorité={self.priorite}, port={self.port_destination}"
        )