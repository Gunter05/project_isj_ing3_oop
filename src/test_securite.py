# Importation de tes classes du module securite
from securite import Firewall, RegleFiltrage, Protocole, Action

# 1. Création d'une structure de paquet simplifiée pour le test
class PaquetTest:
    def __init__(self, adresse_source, adresse_destination, protocole, port_destination):
        self.adresse_source = adresse_source
        self.adresse_destination = adresse_destination
        self.protocole = protocole
        self.port_destination = port_destination

# 2. Initialisation de ton Firewall
print("=== Initialisation du Firewall ===")
mon_firewall = Firewall(adresse_ip="192.168.100.1", nom="FW_Principal", marque="Cisco_SIMNet")
print(f"Firewall créé : {mon_firewall.nom} ({mon_firewall.adresse_ip})")

# 3. Ajout des règles de filtrage (avec authentification)
print("\n=== Configuration des Règles de Sécurité ===")
# Règle 1 : Bloquer tout ce qui vient du réseau suspect 10.0.0.x
regle_suspect = RegleFiltrage(ip_source="10.0.0.", action=Action.BLOQUER)
# Règle 2 : Autoriser spécifiquement le trafic HTTPS (Port 443)
regle_https = RegleFiltrage(protocole=Protocole.HTTPS, port_destination=443, action=Action.AUTORISER)

# Tentative d'ajout des règles
if mon_firewall.ajouter_regle(regle_suspect, "admin", "admin123"):
    print("-> Règle 1 (Bloquer 10.0.0.x) : Ajoutée avec succès !")
else:
    print("-> Échec d'ajout de la règle 1 (Erreur d'authentification)")

if mon_firewall.ajouter_regle(regle_https, "admin", "admin123"):
    print("-> Règle 2 (Autoriser HTTPS 443) : Ajoutée avec succès !")


# 4. Simulation du trafic réseau (Test du filtrage)
print("\n=== Simulation du Trafic Réseau ===")

# Paquet A : Vient d'une IP normale, va sur le port 443 (HTTPS)
paquet_A = PaquetTest("192.168.1.50", "8.8.8.8", Protocole.HTTPS, 443)
print(f"\nInspection Paquet A...")
if mon_firewall.filtrer(paquet_A):
    print("Résultat : [PASS] Le paquet A a bien été AUTORISÉ.")
else:
    print("Résultat : [FAIL] Le paquet A a été bloqué à tort.")

# Paquet B : Vient de la plage bloquée (10.0.0.99)
paquet_B = PaquetTest("10.0.0.99", "192.168.1.1", Protocole.TCP, 80)
print(f"\nInspection Paquet B...")
if not mon_firewall.filtrer(paquet_B):
    print("Résultat : [PASS] Le paquet B provenant d'une IP suspecte a bien été BLOQUÉ.")
else:
    print("Résultat : [FAIL] Sécurité défaillante : Le paquet B est passé !")


# 5. Affichage du journal d'audit (Logs)
print("\n=== Affichage du Journal d'Audit du Firewall ===")
print(mon_firewall.journal.afficher())