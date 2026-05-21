try:
    from securite import Protocole
except ImportError:
    from enum import Enum

    class Protocole(Enum):
        TCP = "TCP"
        UDP = "UDP"
        ICMP = "ICMP"


class Paquet:
    """
    Représente un paquet réseau circulant dans SIMNet.

    Le protocole, la taille et le port peuvent être générés automatiquement
    à partir du type de service demandé.
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
        self.trajet.append(equipement)

    def marquer_perdu(self):
        self.est_perdu = True

    def __str__(self):
        protocole = self.protocole.value if isinstance(self.protocole, Enum) else self.protocole

        return (
            f"Paquet {protocole} "
            f"{self.adresse_source} -> {self.adresse_destination} "
            f"| service={self.service}, taille={self.taille} octets, "
            f"priorité={self.priorite}, port={self.port_destination}"
        )