# SIMNet — Simulateur de Réseau Intelligent en Python

#groupe_1

---

## Description

SIMNet est un simulateur de réseau d'entreprise entièrement orienté objet, développé en Python 3.
Il permet de modéliser une infrastructure réseau, d'y faire circuler des données, d'en assurer
la sécurité via un firewall configurable, et d'en superviser le fonctionnement en temps réel.

---

## Fonctionnalités implémentées

- **Module 1 — Modélisation du réseau** : représentation des équipements réseau (routeurs, switches,
  serveurs, firewalls, points d'accès Wi-Fi, terminaux) avec héritage depuis une classe abstraite `Equipement`.

- **Module 2 — Simulation de trafic** : circulation de paquets entre équipements avec calcul de chemin
  par algorithme BFS (Breadth-First Search), transmission saut par saut, détection des destinations
  inatteignables et comptabilisation des statistiques.

- **Module 3 — Sécurité et filtrage** : firewall avec règles de filtrage (IP source, protocole, port),
  journalisation horodatée de chaque décision, et accès protégé par authentification login/mot de passe.

- **Module 4 — Surveillance et rapports** : moniteur réseau collectant les statistiques par équipement
  et par lien, historique des 10 derniers paquets, génération du fichier `rapport_simnet.txt`.

- **Module 5 — Interface console interactive** : menu interactif en boucle permettant d'ajouter/supprimer
  des équipements et des liens, d'envoyer des paquets, de consulter les logs et de générer des rapports.

---

## Structure du projet

```
project_isj_ing3_oop/
│
├── src/
│   ├── equipements.py   # Classes des équipements réseau (Routeur, Switch, Serveur...)
│   ├── topologie.py     # Topologie du réseau et classe Lien
│   ├── paquets.py       # Classe Paquet et simulation de trafic
│   ├── securite.py      # Firewall, règles de filtrage, journal
│   ├── moniteur.py      # Moniteur réseau et génération de rapport
│   └── main.py          # Point d'entrée — menu interactif
│
├── rapport.pdf          # Rapport technique du groupe
└── README.md            # Ce fichier
```

---

## Lancement du projet

### Prérequis

- Python 3.x installé sur votre machine
- Aucune bibliothèque tierce requise (stdlib uniquement)

### Commande de lancement

```bash
python src/main.py
```

---

## Membres du groupe

 Nom & Prénom         Rôle                   Module principal                         
---------------------------------------------------------------------------------------
 Bitoukoua Ousmane  |   Topologie, routage & trafic                |    topologie.py, paquets.py
 Macheu Talla       |   Architecture POO & équipements réseaux     |    equipements.py, README.md
 Tsafac Belvira     |   Sécurité & firewall                             securite.py, rapport.pdf |
 Onguene Anne       |   Monitoring, interface & intégration        |    moniteur.py,main.py 

---

## Choix techniques notables

- **Algorithme de routage** : BFS (Breadth-First Search) — simple, efficace, garantit le chemin
  le plus court en nombre de sauts.
- **Classe abstraite** : `Equipement` utilise le module `abc` pour forcer l'implémentation de
  `afficher_infos()` dans chaque sous-classe.
- **Encapsulation** : tous les attributs sont privés (préfixe `_`) et accessibles via des méthodes.
- **Journalisation** : chaque décision du firewall est horodatée avec le module `datetime`.

