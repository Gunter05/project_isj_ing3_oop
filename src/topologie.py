from collections import deque

class Lien:
    """
    Représente un lien physique entre deux équipements réseau dans la topologie.

    Ce lien relie deux équipements et définit les caractéristiques physiques
    du canal de transmission comme la latence et la bande passante.

    Attributs:
        equipement1 (Equipement): Le premier équipement connecté.
        equipement2 (Equipement): Le second équipement connecté.
        latence (int): La latence de transmission sur ce lien en millisecondes (ms).
        bande_passante (int): La bande passante disponible sur ce lien en Mbps.
        actif (bool): Indique si le lien physique est opérationnel.
    """

    def __init__(self, equipement1, equipement2, bande_passante=100, latence=5):
        """
        Initialise un nouveau lien physique entre deux équipements.

        Entrées:
            equipement1 (Equipement): Le premier équipement du lien.
            equipement2 (Equipement): Le second équipement du lien.
            bande_passante (int, optionnel): La bande passante en Mbps. Par défaut 100.
            latence (int, optionnel): La latence en millisecondes. Par défaut 5.

        Sortie:
            None.
        """
        self.equipement1 = equipement1
        self.equipement2 = equipement2
        self.latence = latence # en ms
        self.bande_passante = bande_passante # en Mbps
        self.actif = True

    def connecte(self, equipement):
        """
        Vérifie si un équipement donné est connecté à ce lien.

        Entrée:
            equipement (Equipement): L'équipement à tester.

        Sortie:
            bool: True si l'équipement fait partie du lien, False sinon.
        """
        return self.equipement1 == equipement or self.equipement2 == equipement

    def autre_extremite(self, equipement):
        """
        Retourne l'autre équipement connecté à ce lien à partir de l'un des deux.

        Entrée:
            equipement (Equipement): L'un des équipements du lien.

        Sortie:
            Equipement: L'autre équipement si l'équipement donné fait partie du lien, None sinon.
        """
        if self.equipement1 == equipement:
            return self.equipement2
        elif self.equipement2 == equipement:
            return self.equipement1
        else:
            return None

    def __str__(self):
        """
        Retourne une représentation sous forme de chaîne du lien physique.

        Entrée:
            Aucune.

        Sortie:
            str: Représentation textuelle au format "Equipement1 <--> Equipement2".
        """
        return f"{self.equipement1.nom} <--> {self.equipement2.nom}"

class Topologie:
    """
    Gère l'ensemble des équipements et des liens physiques d'un réseau SIMNet.

    Cette classe permet de construire le réseau, de trouver des chemins d'acheminement,
    d'envoyer des paquets et de simuler les transmissions réseau.

    Attributs:
        equipements (list): Liste de tous les équipements réseau de la topologie.
        liens (list): Liste de tous les liens physiques actifs/inactifs de la topologie.
    """

    def __init__(self):
        """
        Initialise une topologie vide.

        Entrée:
            Aucune.

        Sortie:
            None.
        """
        self.equipements = []
        self.liens = []

    def ajouter_equipement(self, equipement):
        """
        Ajoute un nouvel équipement au réseau.

        Entrée:
            equipement (Equipement): L'équipement à ajouter.

        Sortie:
            None.
        """
        if self.trouver_equipement_par_ip(equipement.adresse_ip) is not None:
            print(f"Erreur : l'adresse IP {equipement.adresse_ip} est déjà utilisée.")
            return False

        self.equipements.append(equipement)
        return True

    def supprimer_equipement(self, nom):
        """
        Supprime un équipement du réseau par son nom, ainsi que tous les liens qui y sont connectés.

        Entrée:
            nom (str): Nom de l'équipement à supprimer.

        Sortie:
            bool: True si l'équipement a été trouvé et supprimé, False sinon.
        """
        equipement = self.trouver_equipement_par_nom(nom)

        if equipement is None:
            return False

        liens_a_supprimer = [
            lien for lien in self.liens
            if lien.equipement1 == equipement or lien.equipement2 == equipement
        ]

        for lien in liens_a_supprimer:
            autre = lien.autre_extremite(equipement)
            if autre:
                autre.liberer_interface()

        self.equipements.remove(equipement)
        self.liens = [
            lien for lien in self.liens
            if lien not in liens_a_supprimer
        ]

        return True

    def trouver_equipement_par_nom(self, nom):
        """
        Recherche un équipement dans le réseau par son nom.

        Entrée:
            nom (str): Nom de l'équipement à rechercher.

        Sortie:
            Equipement: L'équipement correspondant s'il est trouvé, None sinon.
        """
        for equipement in self.equipements:
            if equipement.nom == nom:
                return equipement
        return None

    def trouver_equipement_par_ip(self, ip):
        """
        Recherche un équipement dans le réseau par son adresse IP.

        Entrée:
            ip (str): Adresse IP de l'équipement à rechercher.

        Sortie:
            Equipement: L'équipement correspondant s'il est trouvé, None sinon.
        """
        for equipement in self.equipements:
            if equipement.adresse_ip == ip:
                return equipement
        return None

    def connecter(self, nom1, nom2, bande_passante=None, latence=None):
        """
        Crée un lien physique entre deux équipements identifiés par leurs noms.

        Si la bande passante ou la latence n'est pas fournie, elle sera automatiquement
        déterminée en fonction des types des deux équipements reliés.

        Entrées:
            nom1 (str): Nom du premier équipement.
            nom2 (str): Nom du second équipement.
            bande_passante (int, optionnel): Bande passante du lien en Mbps. Par défaut None.
            latence (int, optionnel): Latence du lien en millisecondes (ms). Par défaut None.

        Sortie:
            bool: True si la connexion a été créée avec succès, False si l'un des équipements n'existe pas.
        """
        equipement1 = self.trouver_equipement_par_nom(nom1)
        equipement2 = self.trouver_equipement_par_nom(nom2)

        if equipement1 is None or equipement2 is None:
            return False

        if not equipement1.interface_disponible():
            print(f"Aucune interface disponible sur {equipement1.nom}.")
            return False

        if not equipement2.interface_disponible():
            print(f"Aucune interface disponible sur {equipement2.nom}.")
            return False

        if bande_passante is None or latence is None:
            bande_passante, latence = self.determiner_caracteristiques_lien(
                equipement1,
                equipement2
            )

        lien = Lien(equipement1, equipement2, bande_passante, latence)
        self.liens.append(lien)

        equipement1.reserver_interface()
        equipement2.reserver_interface()

        return True

    def determiner_caracteristiques_lien(self, equipement1, equipement2):
        """
        Détermine la bande passante et la latence typiques entre deux équipements selon leurs types.

        Entrées:
            equipement1 (Equipement): Le premier équipement.
            equipement2 (Equipement): Le second équipement.

        Sortie:
            tuple: (bande_passante: int, latence: int) représentant les valeurs physiques par défaut.
        """
        noms_classes = {
            equipement1.__class__.__name__,
            equipement2.__class__.__name__
        }

        if "PointAccesWifi" in noms_classes:
            return 54, 15

        if "Switch" in noms_classes and "Serveur" in noms_classes:
            return 1000, 2

        if "Switch" in noms_classes and "Routeur" in noms_classes:
            return 1000, 5

        if "Routeur" in noms_classes:
            return 100, 10

        return 100, 5

    def obtenir_voisins(self, equipement):
        """
        Récupère tous les équipements voisins d'un équipement donné via des liens actifs et opérationnels.

        Entrée:
            equipement (Equipement): L'équipement dont on cherche les voisins.

        Sortie:
            list: Liste des équipements voisins actifs et fonctionnels.
        """
        voisins = []

        for lien in self.liens:
            if lien.actif and lien.connecte(equipement):
                voisin = lien.autre_extremite(equipement)
                if voisin is not None and voisin.statut:
                    voisins.append(voisin)

        return voisins

    def trouver_chemin(self, source, destination):
        """
        Recherche le chemin le plus court (en nombre de sauts) entre deux équipements via un parcours en largeur (BFS).

        Entrées:
            source (Equipement): L'équipement de départ.
            destination (Equipement): L'équipement d'arrivée.

        Sortie:
            list: Liste ordonnée des équipements formant le chemin de source à destination, ou None s'il n'y a pas de chemin.
        """
        file = deque()
        visites = set()

        file.append((source, [source]))
        visites.add(source)

        while file:
            equipement_actuel, chemin = file.popleft()

            if equipement_actuel == destination:
                return chemin

            for voisin in self.obtenir_voisins(equipement_actuel):
                if voisin not in visites:
                    visites.add(voisin)
                    file.append((voisin, chemin + [voisin]))

        return None

    def envoyer_paquet(self, paquet):
        """
        Simule l'envoi d'un paquet à travers le réseau en déterminant le chemin et en appliquant les règles de filtrage.

        Le paquet parcourt le chemin trouvé. Si un équipement possède une méthode de filtrage (ex: Firewall),
        celle-ci est appliquée. En cas d'échec ou de blocage, le paquet est marqué perdu.

        Entrée:
            paquet (Paquet): Le paquet réseau à transmettre.

        Sortie:
            dict: Un dictionnaire contenant les résultats de la simulation :
                - succes (bool): Indique si le paquet est arrivé à destination.
                - message (str): Message descriptif du résultat (succès, blocage, etc.).
                - chemin (list): Liste des équipements traversés (trajet).
                - latence (int): Latence totale accumulée sur le trajet en ms.
                - debit (int): Débit du chemin (le goulot d'étranglement ou débit minimum rencontré) en Mbps.
        """
        source = self.trouver_equipement_par_ip(paquet.adresse_source)
        destination = self.trouver_equipement_par_ip(paquet.adresse_destination)

        if source is None:
            paquet.marquer_perdu()
            return {
                "succes": False,
                "message": "Source introuvable",
                "chemin": [],
                "latence": 0,
                "debit": 0
            }

        if destination is None:
            paquet.marquer_perdu()
            return {
                "succes": False,
                "message": "Destination introuvable",
                "chemin": [],
                "latence": 0,
                "debit": 0
            }

        chemin = self.trouver_chemin(source, destination)

        if chemin is None:
            paquet.marquer_perdu()
            return {
                "succes": False,
                "message": "Destination inatteignable",
                "chemin": [],
                "latence": 0,
                "debit": 0
            }

        for equipement in chemin:
            paquet.ajouter_saut(equipement)

            if hasattr(equipement, "filtrer"):
                autorise = equipement.filtrer(paquet)
                if not autorise:
                    paquet.marquer_perdu()
                    return {
                        "succes": False,
                        "message": "Paquet bloqué par le firewall",
                        "chemin": paquet.trajet,
                        "latence": self.calculer_latence_chemin(paquet.trajet),
                        "debit": self.calculer_debit_chemin(paquet.trajet)
                    }

        return {
            "succes": True,
            "message": "Paquet transmis avec succès",
            "chemin": paquet.trajet,
            "latence": self.calculer_latence_chemin(chemin),
            "debit": self.calculer_debit_chemin(chemin)
        }

    def obtenir_lien(self, equipement1, equipement2):
        """
        Recherche le lien physique connectant directement deux équipements.

        Entrées:
            equipement1 (Equipement): Le premier équipement.
            equipement2 (Equipement): Le second équipement.

        Sortie:
            Lien: L'objet Lien physique reliant les deux équipements, ou None s'ils ne sont pas directement connectés.
        """
        for lien in self.liens:
            if (
                lien.equipement1 == equipement1 and lien.equipement2 == equipement2
            ) or (
                lien.equipement1 == equipement2 and lien.equipement2 == equipement1
            ):
                return lien

        return None

    def calculer_latence_chemin(self, chemin):
        """
        Calcule la latence cumulée tout au long d'un chemin donné.

        Entrée:
            chemin (list): Liste d'équipements constituant le chemin.

        Sortie:
            int: Somme des latences des liens reliant successivement les équipements du chemin en ms.
        """
        latence_totale = 0

        for i in range(len(chemin) - 1):
            lien = self.obtenir_lien(chemin[i], chemin[i+1])
            if lien:
                latence_totale += lien.latence

        return latence_totale

    def calculer_debit_chemin(self, chemin):
        """
        Calcule le débit de transmission sur un chemin (loi du goulot d'étranglement).

        Le débit d'un chemin correspond à la bande passante minimale parmi tous les liens physiques du chemin.

        Entrée:
            chemin (list): Liste d'équipements constituant le chemin.

        Sortie:
            int: Débit minimal en Mbps trouvé sur le chemin, ou 0 s'il n'y a pas de liens.
        """
        debits = []

        for i in range(len(chemin) - 1):
            lien = self.obtenir_lien(chemin[i], chemin[i+1])
            if lien:
                debits.append(lien.bande_passante)

        if not debits:
            return 0

        return min(debits)

    def supprimer_lien(self, nom1, nom2):
        equipement1 = self.trouver_equipement_par_nom(nom1)
        equipement2 = self.trouver_equipement_par_nom(nom2)

        if equipement1 is None or equipement2 is None:
            return False

        lien = self.obtenir_lien(equipement1, equipement2)

        if lien is None:
            return False

        self.liens.remove(lien)
        equipement1.liberer_interface()
        equipement2.liberer_interface()

        return True