#!/usr/bin/env python3
"""
Script amélioré pour initialiser toutes les bases de données SQLite des microservices
Gère l'installation des dépendances, la création des migrations et l'initialisation des données
"""

import os
import subprocess
import sys
from pathlib import Path
import time

class Colors:
    """Couleurs pour l'affichage dans le terminal"""
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class DatabaseSetup:
    def __init__(self):
        self.root_dir = Path(__file__).parent
        self.services = {
            "API Gateway": {
                "path": "api-gateway",
                "app_name": "gateway",
                "db_file": "gateway_db.sqlite3"
            },
            "Auth Service": {
                "path": "microservices/auth-service",
                "app_name": "auth_app",
                "db_file": "auth_db.sqlite3"
            },
            "Product Service": {
                "path": "microservices/product-service",
                "app_name": "product_app",
                "db_file": "product_db.sqlite3"
            },
            "Order Service": {
                "path": "microservices/order-service",
                "app_name": "order_app",
                "db_file": "order_db.sqlite3"
            },
            "Inventory Service": {
                "path": "microservices/inventory-service",
                "app_name": "inventory_app",
                "db_file": "inventory_db.sqlite3"
            },
            "Seller Service": {
                "path": "microservices/seller-service",
                "app_name": "seller_app",
                "db_file": "seller_db.sqlite3"
            },
            "Store Service": {
                "path": "microservices/store-service",
                "app_name": "store_app",
                "db_file": "store_db.sqlite3"
            }
        }

    def print_colored(self, message: str, color: str = Colors.ENDC):
        """Affiche un message avec une couleur"""
        print(f"{color}{message}{Colors.ENDC}")

    def print_header(self, message: str):
        """Affiche un en-tête"""
        self.print_colored(f"\n{'='*70}", Colors.HEADER)
        self.print_colored(f"  {message}", Colors.HEADER + Colors.BOLD)
        self.print_colored(f"{'='*70}", Colors.HEADER)

    def run_command(self, command: str, cwd: str = None, capture_output: bool = True) -> bool:
        """Exécute une commande shell et retourne True si succès"""
        try:
            if isinstance(command, str):
                command = command.split()
            
            result = subprocess.run(
                command,
                cwd=cwd,
                capture_output=capture_output,
                text=True,
                check=True
            )
            
            if not capture_output:
                return True
                
            if result.stdout:
                self.print_colored(f"   Output: {result.stdout.strip()}", Colors.OKCYAN)
            
            return True
            
        except subprocess.CalledProcessError as e:
            self.print_colored(f"❌ Erreur lors de l'exécution de '{' '.join(command)}'", Colors.FAIL)
            if e.stderr:
                self.print_colored(f"   Erreur: {e.stderr.strip()}", Colors.FAIL)
            if e.stdout:
                self.print_colored(f"   Output: {e.stdout.strip()}", Colors.WARNING)
            return False
        except FileNotFoundError:
            self.print_colored(f"❌ Commande non trouvée: {command[0]}", Colors.FAIL)
            return False

    def check_dependencies(self) -> bool:
        """Vérifie que Python et pip sont installés"""
        self.print_header("Vérification des dépendances système")
        
        # Vérifier Python
        try:
            result = subprocess.run([sys.executable, "--version"], capture_output=True, text=True)
            python_version = result.stdout.strip()
            self.print_colored(f"✅ {python_version} trouvé", Colors.OKGREEN)
        except:
            self.print_colored("❌ Python non trouvé", Colors.FAIL)
            return False

        # Vérifier pip
        try:
            result = subprocess.run([sys.executable, "-m", "pip", "--version"], capture_output=True, text=True)
            pip_version = result.stdout.strip().split('\n')[0]
            self.print_colored(f"✅ {pip_version} trouvé", Colors.OKGREEN)
        except:
            self.print_colored("❌ pip non trouvé", Colors.FAIL)
            return False

        return True

    def install_dependencies(self) -> bool:
        """Installe les dépendances Python pour tous les services"""
        self.print_header("Installation des dépendances Python")
        
        success_count = 0
        total_services = len(self.services)
        
        for service_name, config in self.services.items():
            service_path = self.root_dir / config["path"]
            requirements_file = service_path / "requirements.txt"
            
            if not service_path.exists():
                self.print_colored(f"⚠️  Répertoire non trouvé: {service_path}", Colors.WARNING)
                continue
                
            if not requirements_file.exists():
                self.print_colored(f"⚠️  requirements.txt non trouvé pour {service_name}", Colors.WARNING)
                continue
            
            self.print_colored(f"📦 Installation des dépendances pour {service_name}...", Colors.OKBLUE)
            
            if self.run_command(f"{sys.executable} -m pip install -r requirements.txt", cwd=service_path):
                self.print_colored(f"✅ Dépendances installées pour {service_name}", Colors.OKGREEN)
                success_count += 1
            else:
                self.print_colored(f"❌ Échec de l'installation pour {service_name}", Colors.FAIL)

        self.print_colored(f"\n📊 Installation terminée: {success_count}/{total_services} services", Colors.OKBLUE)
        return success_count > 0

    def clean_old_databases(self):
        """Supprime les anciennes bases de données"""
        self.print_header("Nettoyage des anciennes bases de données")
        
        for service_name, config in self.services.items():
            service_path = self.root_dir / config["path"]
            db_file = service_path / config["db_file"]
            
            if db_file.exists():
                try:
                    db_file.unlink()
                    self.print_colored(f"🗑️  Suppression de {config['db_file']} pour {service_name}", Colors.WARNING)
                except Exception as e:
                    self.print_colored(f"⚠️  Impossible de supprimer {config['db_file']}: {e}", Colors.WARNING)

    def setup_service_database(self, service_name: str, config: dict) -> bool:
        """Configure la base de données pour un service spécifique"""
        service_path = self.root_dir / config["path"]
        manage_py = service_path / "manage.py"
        
        if not service_path.exists():
            self.print_colored(f"❌ Répertoire non trouvé: {service_path}", Colors.FAIL)
            return False
            
        if not manage_py.exists():
            self.print_colored(f"❌ manage.py non trouvé dans {service_path}", Colors.FAIL)
            return False
        
        self.print_colored(f"🔧 Configuration de la base de données pour {service_name}...", Colors.OKBLUE)
        
        # Supprimer les anciennes migrations
        migrations_dir = service_path / config["app_name"] / "migrations"
        if migrations_dir.exists():
            for migration_file in migrations_dir.glob("*.py"):
                if migration_file.name != "__init__.py":
                    try:
                        migration_file.unlink()
                        self.print_colored(f"   Suppression de {migration_file.name}", Colors.WARNING)
                    except Exception as e:
                        self.print_colored(f"   Impossible de supprimer {migration_file.name}: {e}", Colors.WARNING)
        
        # Créer le répertoire migrations s'il n'existe pas
        migrations_dir.mkdir(exist_ok=True)
        init_file = migrations_dir / "__init__.py"
        if not init_file.exists():
            init_file.touch()
        
        # Makemigrations
        self.print_colored(f"   Création des migrations pour {service_name}...", Colors.OKBLUE)
        if not self.run_command(f"{sys.executable} manage.py makemigrations", cwd=service_path):
            self.print_colored(f"❌ Échec de makemigrations pour {service_name}", Colors.FAIL)
            return False
        
        # Migrate
        self.print_colored(f"   Application des migrations pour {service_name}...", Colors.OKBLUE)
        if not self.run_command(f"{sys.executable} manage.py migrate", cwd=service_path):
            self.print_colored(f"❌ Échec de migrate pour {service_name}", Colors.FAIL)
            return False
        
        # Vérifier que la base de données a été créée
        db_file = service_path / config["db_file"]
        if db_file.exists():
            db_size = db_file.stat().st_size
            self.print_colored(f"✅ Base de données créée pour {service_name} ({db_size} bytes)", Colors.OKGREEN)
        else:
            self.print_colored(f"⚠️  Fichier de base de données non trouvé pour {service_name}", Colors.WARNING)
        
        return True

    def create_superuser_for_auth_service(self):
        """Crée un superutilisateur pour le service d'authentification"""
        self.print_header("Création d'un superutilisateur pour le service d'authentification")
        
        auth_service_path = self.root_dir / "microservices/auth-service"
        
        if not auth_service_path.exists():
            self.print_colored("⚠️  Service d'authentification non trouvé", Colors.WARNING)
            return
        
        self.print_colored("👤 Création d'un superutilisateur par défaut...", Colors.OKBLUE)
        
        # Créer un script Python pour créer le superutilisateur
        create_superuser_script = """
import os
import django
from django.contrib.auth import get_user_model

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'auth_app.settings')
django.setup()

User = get_user_model()

if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser(
        username='admin',
        email='admin@amagon.com',
        password='admin123'
    )
    print('Superutilisateur créé: admin / admin123')
else:
    print('Superutilisateur existe déjà')
"""
        
        script_file = auth_service_path / "create_superuser.py"
        try:
            with open(script_file, 'w') as f:
                f.write(create_superuser_script)
            
            if self.run_command(f"{sys.executable} create_superuser.py", cwd=auth_service_path):
                self.print_colored("✅ Superutilisateur créé (admin / admin123)", Colors.OKGREEN)
            
            # Nettoyer le script temporaire
            script_file.unlink()
            
        except Exception as e:
            self.print_colored(f"❌ Erreur lors de la création du superutilisateur: {e}", Colors.FAIL)

    def setup_all_databases(self) -> bool:
        """Configure toutes les bases de données"""
        self.print_header("Configuration des bases de données SQLite")
        
        success_count = 0
        total_services = len(self.services)
        
        for service_name, config in self.services.items():
            if self.setup_service_database(service_name, config):
                success_count += 1
            time.sleep(1)  # Petite pause entre chaque service
        
        self.print_colored(f"\n📊 Configuration terminée: {success_count}/{total_services} bases de données", Colors.OKBLUE)
        return success_count == total_services

    def run(self) -> bool:
        """Lance la configuration complète"""
        try:
            self.print_colored(f"""
{Colors.HEADER}{Colors.BOLD}
╔══════════════════════════════════════════════════════════════╗
║                🗄️  AMAGON DATABASE SETUP                    ║
║              Configuration des bases SQLite                  ║
╚══════════════════════════════════════════════════════════════╝
{Colors.ENDC}""")
            
            # Vérifier les dépendances
            if not self.check_dependencies():
                return False
            
            # Installer les dépendances
            if not self.install_dependencies():
                self.print_colored("⚠️  Certaines dépendances n'ont pas pu être installées", Colors.WARNING)
            
            # Nettoyer les anciennes bases
            self.clean_old_databases()
            
            # Configurer toutes les bases de données
            if not self.setup_all_databases():
                return False
            
            # Créer un superutilisateur pour l'auth service
            self.create_superuser_for_auth_service()
            
            self.print_colored(f"\n{Colors.OKGREEN}🎉 Configuration des bases de données terminée avec succès!{Colors.ENDC}")
            self.print_colored(f"{Colors.OKBLUE}Vous pouvez maintenant lancer le projet avec: python run_project.py{Colors.ENDC}")
            
            return True
            
        except Exception as e:
            self.print_colored(f"❌ Erreur inattendue: {e}", Colors.FAIL)
            return False

def main():
    """Fonction principale"""
    setup = DatabaseSetup()
    success = setup.run()
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()