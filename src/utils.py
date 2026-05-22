from ipaddress import IPv4Address


def valider_adresse_ip(adresse_ip):
    """
    Vérifie qu'une adresse IP est une adresse IPv4 valide.

    Exemple valide : 192.168.1.10
    Exemple invalide : 300.400.500.600
    """
    try:
        return str(IPv4Address(adresse_ip.strip()))
    except ValueError:
        raise ValueError(f"Adresse IP invalide : {adresse_ip}")