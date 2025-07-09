import hashlib
import os

def generate_salt():
    """Génère un salt aléatoire de 8 octets."""
    return os.urandom(8).hex()

def hash_password(salt, password):
    """Hache un mot de passe avec MD5 et un salt."""
    return hashlib.md5((salt + password).encode()).hexdigest()

def check_password(salt, password, hashed_password):
    """Vérifie un mot de passe haché."""
    return hash_password(salt, password) == hashed_password

def generate_token():
    """Génère un token aléatoire de 32 octets."""
    return os.urandom(32).hex()
