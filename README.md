# SIMNet — Simulateur de Réseau Intelligent en Python

> Projet de groupe — Programmation Orientée Objet en Python
> ING3 SRT — Institut Saint Jean — Année académique 2025-2026

---

## Description

**SIMNet** est un simulateur de réseau d’entreprise développé en Python 3 selon les principes de la programmation orientée objet.

Il permet de modéliser une infrastructure réseau composée d’équipements tels que des routeurs, switches, serveurs, firewalls, points d’accès Wi-Fi et terminaux. Le simulateur permet également de créer des liens entre ces équipements, de faire circuler des paquets, d’appliquer des règles de sécurité via un firewall et de surveiller l’activité réseau à travers un module de monitoring.

---

## Objectif du projet

L’objectif principal de SIMNet est de simuler le fonctionnement d’un réseau informatique simple en mettant en pratique les concepts fondamentaux de la programmation orientée objet :

* classes et objets ;
* héritage ;
* abstraction ;
* encapsulation ;
* polymorphisme ;
* composition ;
* modularité ;
* surcharge de méthodes ;
* gestion des interactions entre objets.

---

## Fonctionnalités implémentées

### Module 1 — Modélisation du réseau

Le simulateur permet de représenter plusieurs types d’équipements réseau :

* routeur ;
* switch ;
* serveur ;
* firewall ;
* point d’accès Wi-Fi ;
* terminal client.

Tous ces équipements héritent d’une classe abstraite `Equipement`, qui regroupe les attributs et comportements communs.

---

### Module 2 — Topologie et liens réseau

Le module de topologie permet de :

* créer une topologie réseau ;
* ajouter des équipements ;
* supprimer des équipements ;
* connecter deux équipements ;
* représenter les liens entre équipements ;
* calculer automatiquement la bande passante et la latence d’un lien ;
* rechercher un chemin entre deux équipements.

Les équipements sont considérés comme des nœuds du réseau, tandis que les liens représentent les connexions entre eux.

---

### Module 3 — Simulation de trafic

Le simulateur permet d’envoyer des paquets entre deux adresses IP.

Chaque paquet contient notamment :

* une adresse source ;
* une adresse destination ;
* un service simulé ;
* un protocole ;
* une taille ;
* une priorité ;
* un port de destination ;
* le trajet parcouru.

Le chemin du paquet est déterminé à l’aide de l’algorithme **BFS** (*Breadth-First Search*), qui permet de trouver un chemin entre la source et la destination.

---

### Module 4 — Sécurité et firewall

Le module de sécurité permet de configurer un firewall capable de filtrer les paquets selon plusieurs critères :

* adresse IP source ;
* protocole ;
* port de destination ;
* action à appliquer : autoriser ou bloquer.

Le firewall dispose également :

* d’un système d’authentification ;
* d’un journal de sécurité ;
* d’une journalisation horodatée des décisions prises.

---

### Module 5 — Monitoring et rapports

Le moniteur réseau permet de suivre l’activité du simulateur.

Il permet notamment de :

* compter les paquets envoyés ;
* compter les paquets perdus ;
* suivre le débit cumulé ;
* conserver l’historique des derniers événements réseau ;
* générer un rapport dans un fichier texte.

Le rapport généré est nommé :

```bash
rapport_simnet.txt
```

---

### Module 6 — Interface console interactive

Le simulateur dispose d’une interface console permettant à l’utilisateur de naviguer dans plusieurs menus :

* gestion des équipements ;
* gestion du réseau ;
* monitoring ;
* sécurité ;
* fermeture du simulateur.

L’interface permet d’effectuer les principales actions sans modifier directement le code source.

---

## Structure du projet

```text
project_isj_ing3_oop/
│
├── src/
│   ├── equipements.py      # Classes des équipements réseau
│   ├── topologie.py        # Topologie du réseau et classe Lien
│   ├── paquets.py          # Classe Paquet et caractéristiques du trafic
│   ├── securite.py         # Firewall, règles de filtrage et journalisation
│   ├── moniteur.py         # Moniteur réseau et génération de rapport
│   ├── simulateur.py       # Classe principale SimulateurSIMNet
│   └── main.py             # Point d’entrée du programme
│
├── rapport.pdf             # Rapport technique du groupe
└── README.md               # Documentation du projet
```

---

## Lancement du projet

### Prérequis

* Python 3.x installé ;
* aucune bibliothèque externe requise ;
* exécution depuis la racine du projet.

### Commande de lancement

```bash
python src/main.py
```

---

## Scénario de démonstration

Au lancement, le simulateur peut initialiser une topologie de démonstration :

```text
Client-1 -> SW-1 -> FW-1 -> SRV-1
```

Cette topologie permet de tester rapidement :

* l’affichage des équipements ;
* l’affichage des liens ;
* l’envoi d’un paquet ;
* le calcul du chemin ;
* le passage par le firewall ;
* l’enregistrement dans le monitoring ;
* la génération du rapport réseau.

---

## Membres du groupe

| N° | Nom et prénom    | Rôle dans le groupe                       | Modules principaux                              |
| -: | ---------------- | ---------------------------------         | ----------------------------------------------  |
|  1 | Bitoukoa Ousmane | Topologie, routage, trafic                | topologie.py, paquets.py                        |
|  2 | Macheu Sandra    | Architecture POO et &quipements réseau    | equipements.py, README.md                       |
|  3 | Tsafac Belvira   | Sécurité et Firewall                      | securite.py, rapport.pdf                        |
|  4 | Anne Onguene     | Monitoring,interface et integration       | moniteur.py, main.py                            |


---

## Choix techniques

### Programmation orientée objet

Le projet repose sur une architecture orientée objet afin de représenter chaque élément réseau sous forme d’objet autonome.

Chaque classe possède ses propres attributs et méthodes, ce qui rend le code plus lisible, réutilisable et maintenable.

---

### Classe abstraite `Equipement`

La classe `Equipement` sert de base commune à tous les équipements réseau.

Elle permet de factoriser les propriétés communes :

* nom ;
* adresse IP ;
* marque ;
* statut.

Elle impose également certaines méthodes aux classes filles, notamment l’affichage des informations.

---

### Algorithme BFS

L’algorithme **BFS** est utilisé pour rechercher un chemin entre deux équipements.

Ce choix est adapté au projet car :

* il est simple à comprendre ;
* il fonctionne bien sur une topologie représentée sous forme de graphe ;
* il permet de trouver un chemin en nombre minimal de sauts ;
* il est facile à expliquer lors de la soutenance.

---

### Firewall configurable

Le firewall utilise des règles de filtrage permettant d’autoriser ou de bloquer un paquet selon :

* l’adresse IP source ;
* le protocole ;
* le port de destination.

Chaque décision est enregistrée dans un journal horodaté.

---

### Génération automatique des caractéristiques des paquets

L’utilisateur choisit un service à simuler, par exemple :

* web ;
* https ;
* ping ;
* dns ;
* fichier.

La classe `Paquet` déduit ensuite automatiquement certaines caractéristiques :

* protocole ;
* port ;
* taille ;
* priorité.

Cela simplifie l’utilisation du simulateur tout en gardant une logique réseau réaliste.

---

## Exemples de services simulés

| Service | Protocole utilisé |  Port | Taille simulée |
| ------- | ----------------- | ----: | -------------: |
| web     | TCP               |    80 |     512 octets |
| https   | TCP               |   443 |     768 octets |
| ping    | ICMP              | Aucun |      64 octets |
| dns     | UDP               |    53 |     128 octets |
| fichier | TCP               |    21 |    1500 octets |

---

## Exemple d’utilisation

1. Lancer le programme :

```bash
python src/main.py
```

2. Choisir un menu :

```text
1. Gestion des équipements
2. Gestion du réseau
3. Monitoring
4. Sécurité
5. Quitter
```

3. Ajouter ou afficher des équipements.

4. Connecter deux équipements.

5. Envoyer un paquet depuis une adresse IP source vers une adresse IP destination.

6. Consulter les statistiques et les journaux.

7. Générer un rapport réseau.

---

## Résultats attendus

Le simulateur doit permettre de :

* créer une topologie réseau simple ;
* connecter des équipements entre eux ;
* simuler l’envoi de paquets ;
* déterminer le chemin emprunté par un paquet ;
* bloquer ou autoriser un paquet via le firewall ;
* enregistrer l’activité réseau ;
* générer un rapport de supervision.

---

## Auteurs

Projet réalisé par le **Groupe 1** dans le cadre du cours de **Programmation Orientée Objet en Python**.


