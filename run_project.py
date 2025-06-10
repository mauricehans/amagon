#!/usr/bin/env python3
"""
Script Python amélioré pour lancer automatiquement tout le projet Amagon
Gère l'installation des dépendances, la configuration des bases de données et le démarrage des services
"""

import os
import subprocess
import sys
import time
import threading
import signal
import json
from pathlib import Path
from typing import Dict, List, Optional, Tuple

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

class ProjectLauncher:
    def __init__(self):
        self.processes: Dict[str, subprocess.Popen] = {}
        self.should_run = True
        self.root_dir = Path(__file__).parent
        self.ready_services = set()
        
        # Configuration des services
        self.services = {
            "API Gateway": {
                "path": "api-gateway",
                "port": 8000,
                "cmd": [sys.executable, "manage.py", "runserver", "8000"],
                "ready_message": "Starting development server at http://127.0.0.1:8000/",
                "requirements": "requirements.txt",
                "health_check": "http://localhost:8000/admin/"
            },
            "Auth Service": {
                "path": "microservices/auth-service",
                "port": 8001,
                "cmd": [sys.executable, "manage.py", "runserver", "8001"],
                "ready_message": "Starting development server at http://127.0.0.1:8001/",
                "requirements": "requirements.txt",
                "health_check": "http://localhost:8001/admin/"
            },
            "Product Service": {
                "path": "microservices/product-service",
                "port": 8002,
                "cmd": [sys.executable, "manage.py", "runserver", "8002"],
                "ready_message": "Starting development server at http://127.0.0.1:8002/",
                "requirements": "requirements.txt",
                "health_check": "http://localhost:8002/admin/"
            },
            "Order Service": {
                "path": "microservices/order-service",
                "port": 8003,
                "cmd": [sys.executable, "manage.py", "runserver", "8003"],
                "ready_message": "Starting development server at http://127.0.0.1:8003/",
                "requirements": "requirements.txt",
                "health_check": "http://localhost:8003/admin/"
            },
            "Inventory Service": {
                "path": "microservices/inventory-service",
                "port": 8004,
                "cmd": [sys.executable, "manage.py", "runserver", "8004"],
                "ready_message": "Starting development server at http://127.0.0.1:8004/",
                "requirements": "requirements.txt",
                "health_check": "http://localhost:8004/admin/"
            },
            "Seller Service": {
                "path": "microservices/seller-service",
                "port": 8005,
                "cmd": [sys.executable, "manage.py", "runserver", "8005"],
                "ready_message": "Starting development server at http://127.0.0.1:8005/",
                "requirements": "requirements.txt",
                "health_check": "http://localhost:8005/admin/"
            },
            "Store Service": {
                "path": "microservices/store-service",
                "port": 8006,
                "cmd": [sys.executable, "manage.py", "runserver", "8006"],
                "ready_message": "Starting development server at http://127.0.0.1:8006/",
                "requirements": "requirements.txt",
                "health_check": "http://localhost:8006/admin/"
            },
            "Frontend": {
                "path": ".",
                "port": 5173,
                "cmd": ["npm", "run", "dev"],
                "ready_message": "Local:",
                "requirements": "package.json",
                "health_check": "http://localhost:5173"
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

    def run_command(self, command: str, cwd: Optional[str] = None, capture_output: bool = True) -> Optional[str]:
        """Exécute une commande shell"""
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
            return result.stdout if capture_output else None
        except subprocess.CalledProcessError as e:
            self.print_colored(f"❌ Erreur lors de l'exécution de '{' '.join(command)}': {e}", Colors.FAIL)
            if capture_output and e.stderr:
                self.print_colored(f"Détails: {e.stderr}", Colors.FAIL)
            return None
        except FileNotFoundError:
            self.print_colored(f"❌ Commande non trouvée: {command[0]}", Colors.FAIL)
            return None

    def check_dependencies(self) -> bool:
        """Vérifie que Python et Node.js sont installés"""
        self.print_header("Vérification des dépendances système")
        
        # Vérifier Python
        try:
            result = subprocess.run([sys.executable, "--version"], capture_output=True, text=True)
            python_version = result.stdout.strip()
            self.print_colored(f"✅ {python_version} trouvé", Colors.OKGREEN)
        except:
            self.print_colored("❌ Python non trouvé", Colors.FAIL)
            return False

        # Vérifier Node.js
        try:
            result = subprocess.run(["node", "--version"], capture_output=True, text=True)
            node_version = result.stdout.strip()
            self.print_colored(f"✅ Node.js {node_version} trouvé", Colors.OKGREEN)
        except:
            self.print_colored("❌ Node.js non trouvé", Colors.FAIL)
            return False

        # Vérifier npm
        try:
            result = subprocess.run(["npm", "--version"], capture_output=True, text=True)
            npm_version = result.stdout.strip()
            self.print_colored(f"✅ npm {npm_version} trouvé", Colors.OKGREEN)
        except:
            self.print_colored("❌ npm non trouvé", Colors.FAIL)
            return False

        return True

    def install_dependencies(self) -> bool:
        """Installe toutes les dépendances"""
        self.print_header("Installation des dépendances")
        
        # Installer les dépendances frontend
        self.print_colored("📦 Installation des dépendances frontend...", Colors.OKBLUE)
        if not self.run_command("npm install", cwd=self.root_dir):
            self.print_colored("❌ Échec de l'installation des dépendances frontend", Colors.FAIL)
            return False
        self.print_colored("✅ Dépendances frontend installées", Colors.OKGREEN)

        # Installer les dépendances Python pour chaque service
        for service_name, config in self.services.items():
            if service_name == "Frontend":
                continue
                
            service_path = self.root_dir / config["path"]
            requirements_file = service_path / config["requirements"]
            
            if requirements_file.exists():
                self.print_colored(f"📦 Installation des dépendances pour {service_name}...", Colors.OKBLUE)
                if not self.run_command(f"{sys.executable} -m pip install -r {config['requirements']}", cwd=service_path):
                    self.print_colored(f"⚠️  Échec de l'installation pour {service_name}", Colors.WARNING)
                else:
                    self.print_colored(f"✅ Dépendances installées pour {service_name}", Colors.OKGREEN)
            else:
                self.print_colored(f"⚠️  Fichier requirements.txt non trouvé pour {service_name}", Colors.WARNING)

        return True

    def check_databases(self) -> bool:
        """Vérifie si les bases de données existent"""
        self.print_header("Vérification des bases de données")
        
        db_files = {
            "API Gateway": "api-gateway/gateway_db.sqlite3",
            "Auth Service": "microservices/auth-service/auth_db.sqlite3",
            "Product Service": "microservices/product-service/product_db.sqlite3",
            "Order Service": "microservices/order-service/order_db.sqlite3",
            "Inventory Service": "microservices/inventory-service/inventory_db.sqlite3",
            "Seller Service": "microservices/seller-service/seller_db.sqlite3",
            "Store Service": "microservices/store-service/store_db.sqlite3",
        }
        
        missing_dbs = []
        for service_name, db_path in db_files.items():
            db_file = self.root_dir / db_path
            if db_file.exists():
                db_size = db_file.stat().st_size
                self.print_colored(f"✅ {service_name}: {db_path} ({db_size} bytes)", Colors.OKGREEN)
            else:
                self.print_colored(f"❌ {service_name}: {db_path} manquant", Colors.FAIL)
                missing_dbs.append(service_name)
        
        if missing_dbs:
            self.print_colored(f"\n⚠️  Bases de données manquantes détectées!", Colors.WARNING)
            self.print_colored(f"Services concernés: {', '.join(missing_dbs)}", Colors.WARNING)
            self.print_colored(f"Exécution de setup_databases.py...", Colors.OKBLUE)
            
            if not self.run_command(f"{sys.executable} setup_databases.py", cwd=self.root_dir, capture_output=False):
                self.print_colored("❌ Échec de la configuration des bases de données", Colors.FAIL)
                return False
            
            self.print_colored("✅ Bases de données configurées", Colors.OKGREEN)
        
        return True

    def start_service(self, service_name: str, config: Dict) -> bool:
        """Démarre un service spécifique"""
        service_path = self.root_dir / config["path"]
        
        if not service_path.exists():
            self.print_colored(f"❌ Répertoire non trouvé: {service_path}", Colors.FAIL)
            return False

        self.print_colored(f"🚀 Démarrage de {service_name}...", Colors.OKBLUE)
        
        try:
            process = subprocess.Popen(
                config["cmd"],
                cwd=service_path,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1,
                universal_newlines=True
            )
            
            self.processes[service_name] = process
            
            # Surveiller la sortie du processus
            def monitor_output():
                while self.should_run and process.poll() is None:
                    try:
                        line = process.stdout.readline()
                        if line:
                            line = line.strip()
                            print(f"[{service_name}] {line}")
                            
                            if config["ready_message"] in line:
                                self.ready_services.add(service_name)
                                self.print_colored(f"✅ {service_name} est prêt sur le port {config['port']}", Colors.OKGREEN)
                    except:
                        break
                        
                # Surveiller stderr
                while self.should_run and process.poll() is None:
                    try:
                        line = process.stderr.readline()
                        if line:
                            line = line.strip()
                            if line and not line.startswith("Watching for file changes"):
                                print(f"[{service_name}] {line}")
                    except:
                        break
            
            # Démarrer le monitoring dans un thread séparé
            monitor_thread = threading.Thread(target=monitor_output, daemon=True)
            monitor_thread.start()
            
            return True
            
        except Exception as e:
            self.print_colored(f"❌ Erreur lors du démarrage de {service_name}: {e}", Colors.FAIL)
            return False

    def wait_for_services(self, services: List[str], timeout: int = 60) -> bool:
        """Attend que les services soient prêts"""
        self.print_colored(f"⏳ Attente que les services soient prêts...", Colors.WARNING)
        
        start_time = time.time()
        while time.time() - start_time < timeout:
            ready_count = len([s for s in services if s in self.ready_services])
            if ready_count == len(services):
                return True
            
            self.print_colored(f"   Services prêts: {ready_count}/{len(services)}", Colors.OKCYAN)
            time.sleep(2)
        
        return False

    def start_all_services(self) -> bool:
        """Démarre tous les services"""
        self.print_header("Démarrage des services")
        
        # Démarrer les services backend d'abord
        backend_services = [name for name in self.services.keys() if name != "Frontend"]
        
        for service_name in backend_services:
            config = self.services[service_name]
            if not self.start_service(service_name, config):
                return False
            time.sleep(1)  # Attendre un peu entre chaque service
        
        # Attendre que les services backend soient prêts
        if not self.wait_for_services(backend_services, timeout=30):
            self.print_colored("⚠️  Certains services backend ne sont pas prêts", Colors.WARNING)
        
        # Démarrer le frontend
        if not self.start_service("Frontend", self.services["Frontend"]):
            return False
        
        return True

    def show_status(self):
        """Affiche le statut des services"""
        self.print_header("Statut des services")
        
        for service_name, config in self.services.items():
            if service_name in self.processes:
                process = self.processes[service_name]
                if process.poll() is None:
                    status = "🟢 En cours" if service_name in self.ready_services else "🟡 Démarrage"
                    self.print_colored(f"{status} {service_name} - Port {config['port']}", Colors.OKGREEN if service_name in self.ready_services else Colors.WARNING)
                else:
                    self.print_colored(f"🔴 {service_name} - Arrêté", Colors.FAIL)
            else:
                self.print_colored(f"⚪ {service_name} - Non démarré", Colors.WARNING)
        
        self.print_colored(f"\n🌐 URLs d'accès:", Colors.OKBLUE)
        self.print_colored(f"   Frontend: http://localhost:5173", Colors.OKCYAN)
        self.print_colored(f"   API Gateway: http://localhost:8000", Colors.OKCYAN)
        self.print_colored(f"   Admin Auth: http://localhost:8001/admin/ (admin/admin123)", Colors.OKCYAN)

    def show_project_info(self):
        """Affiche les informations du projet"""
        self.print_colored(f"""
{Colors.OKGREEN}🎉 Projet Amagon lancé avec succès!{Colors.ENDC}

{Colors.OKBLUE}📋 Informations importantes:{Colors.ENDC}
• Frontend React: http://localhost:5173
• API Gateway: http://localhost:8000
• Interface Admin: http://localhost:8001/admin/
• Compte admin: admin / admin123

{Colors.OKBLUE}🗄️ Bases de données SQLite:{Colors.ENDC}
• Toutes les données sont stockées localement
• Pas besoin de PostgreSQL ou MySQL
• Fichiers .sqlite3 dans chaque service

{Colors.WARNING}⚠️  Pour arrêter tous les services: Ctrl+C{Colors.ENDC}
""")

    def cleanup(self):
        """Arrête tous les services"""
        self.should_run = False
        self.print_colored("\n🛑 Arrêt des services...", Colors.WARNING)
        
        for service_name, process in self.processes.items():
            try:
                self.print_colored(f"   Arrêt de {service_name}...", Colors.WARNING)
                process.terminate()
                
                # Attendre un peu pour l'arrêt gracieux
                try:
                    process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    self.print_colored(f"   Forçage de l'arrêt de {service_name}...", Colors.WARNING)
                    process.kill()
                    process.wait()
                    
            except Exception as e:
                self.print_colored(f"   Erreur lors de l'arrêt de {service_name}: {e}", Colors.FAIL)
        
        self.print_colored("✅ Tous les services ont été arrêtés", Colors.OKGREEN)

    def run(self):
        """Lance le projet complet"""
        try:
            self.print_colored(f"""
{Colors.HEADER}{Colors.BOLD}
╔══════════════════════════════════════════════════════════════╗
║                     🛒 AMAGON PROJECT                        ║
║                  Lanceur automatique v2.0                   ║
╚══════════════════════════════════════════════════════════════╝
{Colors.ENDC}""")
            
            # Vérifier les dépendances système
            if not self.check_dependencies():
                self.print_colored("❌ Dépendances système manquantes", Colors.FAIL)
                return False
            
            # Installer les dépendances
            if not self.install_dependencies():
                self.print_colored("❌ Échec de l'installation des dépendances", Colors.FAIL)
                return False
            
            # Vérifier et configurer les bases de données
            if not self.check_databases():
                self.print_colored("❌ Échec de la configuration des bases de données", Colors.FAIL)
                return False
            
            # Démarrer tous les services
            if not self.start_all_services():
                self.print_colored("❌ Échec du démarrage des services", Colors.FAIL)
                return False
            
            # Attendre un peu pour que tout se stabilise
            time.sleep(3)
            
            # Afficher le statut
            self.show_status()
            self.show_project_info()
            
            # Attendre l'interruption
            try:
                while self.should_run:
                    time.sleep(1)
            except KeyboardInterrupt:
                pass
            
            return True
            
        except Exception as e:
            self.print_colored(f"❌ Erreur inattendue: {e}", Colors.FAIL)
            return False
        finally:
            self.cleanup()

def signal_handler(signum, frame):
    """Gestionnaire de signal pour arrêt propre"""
    print("\n🛑 Signal d'arrêt reçu...")
    if hasattr(signal_handler, 'launcher'):
        signal_handler.launcher.cleanup()
    sys.exit(0)

def main():
    """Fonction principale"""
    # Configurer le gestionnaire de signal
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # Créer et lancer le projet
    launcher = ProjectLauncher()
    signal_handler.launcher = launcher
    
    success = launcher.run()
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()