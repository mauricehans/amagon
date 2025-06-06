#!/usr/bin/env python3
"""
Script Python pour lancer automatiquement tout le projet Amagon
Gère l'installation des dépendances, la configuration des bases de données et le démarrage des services
"""

import os
import subprocess
import sys
import time
import threading
import signal
from pathlib import Path
from typing import Dict, List, Optional

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
        
        # Configuration des services
        self.services = {
            "API Gateway": {
                "path": "api-gateway",
                "port": 8000,
                "cmd": ["python", "manage.py", "runserver", "8000"],
                "ready_message": "Starting development server at http://127.0.0.1:8000/",
                "requirements": "requirements.txt"
            },
            "Auth Service": {
                "path": "microservices/auth-service",
                "port": 8001,
                "cmd": ["python", "manage.py", "runserver", "8001"],
                "ready_message": "Starting development server at http://127.0.0.1:8001/",
                "requirements": "requirements.txt"
            },
            "Product Service": {
                "path": "microservices/product-service",
                "port": 8002,
                "cmd": ["python", "manage.py", "runserver", "8002"],
                "ready_message": "Starting development server at http://127.0.0.1:8002/",
                "requirements": "requirements.txt"
            },
            "Order Service": {
                "path": "microservices/order-service",
                "port": 8003,
                "cmd": ["python", "manage.py", "runserver", "8003"],
                "ready_message": "Starting development server at http://127.0.0.1:8003/",
                "requirements": "requirements.txt"
            },
            "Inventory Service": {
                "path": "microservices/inventory-service",
                "port": 8004,
                "cmd": ["python", "manage.py", "runserver", "8004"],
                "ready_message": "Starting development server at http://127.0.0.1:8004/",
                "requirements": "requirements.txt"
            },
            "Seller Service": {
                "path": "microservices/seller-service",
                "port": 8005,
                "cmd": ["python", "manage.py", "runserver", "8005"],
                "ready_message": "Starting development server at http://127.0.0.1:8005/",
                "requirements": "requirements.txt"
            },
            "Store Service": {
                "path": "microservices/store-service",
                "port": 8006,
                "cmd": ["python", "manage.py", "runserver", "8006"],
                "ready_message": "Starting development server at http://127.0.0.1:8006/",
                "requirements": "requirements.txt"
            },
            "Frontend": {
                "path": ".",
                "port": 5173,
                "cmd": ["npm", "run", "dev"],
                "ready_message": "Local:",
                "requirements": "package.json"
            }
        }

    def print_colored(self, message: str, color: str = Colors.ENDC):
        """Affiche un message avec une couleur"""
        print(f"{color}{message}{Colors.ENDC}")

    def print_header(self, message: str):
        """Affiche un en-tête"""
        self.print_colored(f"\n{'='*60}", Colors.HEADER)
        self.print_colored(f"  {message}", Colors.HEADER + Colors.BOLD)
        self.print_colored(f"{'='*60}", Colors.HEADER)

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
                if not self.run_command(f"pip install -r {config['requirements']}", cwd=service_path):
                    self.print_colored(f"⚠️  Échec de l'installation pour {service_name}", Colors.WARNING)
                else:
                    self.print_colored(f"✅ Dépendances installées pour {service_name}", Colors.OKGREEN)
            else:
                self.print_colored(f"⚠️  Fichier requirements.txt non trouvé pour {service_name}", Colors.WARNING)

        return True

    def setup_databases(self) -> bool:
        """Configure toutes les bases de données"""
        self.print_header("Configuration des bases de données")
        
        for service_name, config in self.services.items():
            if service_name == "Frontend":
                continue
                
            service_path = self.root_dir / config["path"]
            manage_py = service_path / "manage.py"
            
            if not manage_py.exists():
                self.print_colored(f"⚠️  manage.py non trouvé pour {service_name}", Colors.WARNING)
                continue
            
            self.print_colored(f"🔧 Configuration de la base de données pour {service_name}...", Colors.OKBLUE)
            
            # Makemigrations
            if not self.run_command("python manage.py makemigrations", cwd=service_path):
                self.print_colored(f"⚠️  Échec de makemigrations pour {service_name}", Colors.WARNING)
                continue
            
            # Migrate
            if not self.run_command("python manage.py migrate", cwd=service_path):
                self.print_colored(f"❌ Échec de migrate pour {service_name}", Colors.FAIL)
                return False
            
            self.print_colored(f"✅ Base de données configurée pour {service_name}", Colors.OKGREEN)

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
                            print(f"[{service_name}] {line.strip()}")
                            if config["ready_message"] in line:
                                self.print_colored(f"✅ {service_name} est prêt sur le port {config['port']}", Colors.OKGREEN)
                    except:
                        break
            
            # Démarrer le monitoring dans un thread séparé
            monitor_thread = threading.Thread(target=monitor_output, daemon=True)
            monitor_thread.start()
            
            return True
            
        except Exception as e:
            self.print_colored(f"❌ Erreur lors du démarrage de {service_name}: {e}", Colors.FAIL)
            return False

    def start_all_services(self) -> bool:
        """Démarre tous les services"""
        self.print_header("Démarrage des services")
        
        # Démarrer les services backend d'abord
        backend_services = {k: v for k, v in self.services.items() if k != "Frontend"}
        
        for service_name, config in backend_services.items():
            if not self.start_service(service_name, config):
                return False
            time.sleep(2)  # Attendre un peu entre chaque service
        
        # Attendre que les services backend soient prêts
        self.print_colored("⏳ Attente que les services backend soient prêts...", Colors.WARNING)
        time.sleep(5)
        
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
                    self.print_colored(f"✅ {service_name} - En cours d'exécution sur le port {config['port']}", Colors.OKGREEN)
                else:
                    self.print_colored(f"❌ {service_name} - Arrêté", Colors.FAIL)
            else:
                self.print_colored(f"⚪ {service_name} - Non démarré", Colors.WARNING)
        
        self.print_colored(f"\n🌐 Application disponible sur:", Colors.OKBLUE)
        self.print_colored(f"   Frontend: http://localhost:5173", Colors.OKCYAN)
        self.print_colored(f"   API Gateway: http://localhost:8000", Colors.OKCYAN)

    def cleanup(self):
        """Arrête tous les services"""
        self.should_run = False
        self.print_colored("\n🛑 Arrêt des services...", Colors.WARNING)
        
        for service_name, process in self.processes.items():
            try:
                self.print_colored(f"   Arrêt de {service_name}...", Colors.WARNING)
                process.terminate()
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.print_colored(f"   Forçage de l'arrêt de {service_name}...", Colors.WARNING)
                process.kill()
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
║                  Lanceur automatique                         ║
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
            
            # Configurer les bases de données
            if not self.setup_databases():
                self.print_colored("❌ Échec de la configuration des bases de données", Colors.FAIL)
                return False
            
            # Démarrer tous les services
            if not self.start_all_services():
                self.print_colored("❌ Échec du démarrage des services", Colors.FAIL)
                return False
            
            # Afficher le statut
            time.sleep(3)
            self.show_status()
            
            # Attendre l'interruption
            self.print_colored(f"\n{Colors.OKGREEN}🎉 Projet lancé avec succès!{Colors.ENDC}")
            self.print_colored(f"{Colors.WARNING}Appuyez sur Ctrl+C pour arrêter tous les services{Colors.ENDC}")
            
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