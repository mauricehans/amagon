#!/usr/bin/env python3
"""
Script d'installation automatique des dépendances pour le projet Amagon
Installe les dépendances frontend (npm) et backend (pip) pour tous les services
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

class DependencyInstaller:
    def __init__(self):
        self.root_dir = Path(__file__).parent
        self.services = [
            {
                "name": "API Gateway",
                "path": "api-gateway",
                "requirements": "requirements.txt"
            },
            {
                "name": "Auth Service",
                "path": "microservices/auth-service",
                "requirements": "requirements.txt"
            },
            {
                "name": "Product Service",
                "path": "microservices/product-service",
                "requirements": "requirements.txt"
            },
            {
                "name": "Order Service",
                "path": "microservices/order-service",
                "requirements": "requirements.txt"
            },
            {
                "name": "Inventory Service",
                "path": "microservices/inventory-service",
                "requirements": "requirements.txt"
            },
            {
                "name": "Seller Service",
                "path": "microservices/seller-service",
                "requirements": "requirements.txt"
            },
            {
                "name": "Store Service",
                "path": "microservices/store-service",
                "requirements": "requirements.txt"
            }
        ]

    def print_colored(self, message: str, color: str = Colors.ENDC):
        """Affiche un message avec une couleur"""
        print(f"{color}{message}{Colors.ENDC}")

    def print_header(self, message: str):
        """Affiche un en-tête"""
        self.print_colored(f"\n{'='*70}", Colors.HEADER)
        self.print_colored(f"  {message}", Colors.HEADER + Colors.BOLD)
        self.print_colored(f"{'='*70}", Colors.HEADER)

    def run_command(self, command: str, cwd: str = None, capture_output: bool = True, shell: bool = False) -> bool:
        """Exécute une commande shell et retourne True si succès"""
        try:
            if isinstance(command, str) and not shell:
                command = command.split()
            
            self.print_colored(f"   Exécution: {command if shell else ' '.join(command)}", Colors.OKCYAN)
            
            result = subprocess.run(
                command,
                cwd=cwd,
                capture_output=capture_output,
                text=True,
                check=True,
                shell=shell
            )
            
            if capture_output and result.stdout:
                # Afficher seulement les dernières lignes importantes
                lines = result.stdout.strip().split('\n')
                if len(lines) > 5:
                    self.print_colored(f"   ... ({len(lines)} lignes)", Colors.OKCYAN)
                    for line in lines[-3:]:
                        if line.strip():
                            self.print_colored(f"   {line}", Colors.OKCYAN)
                else:
                    for line in lines:
                        if line.strip():
                            self.print_colored(f"   {line}", Colors.OKCYAN)
            
            return True
            
        except subprocess.CalledProcessError as e:
            self.print_colored(f"❌ Erreur lors de l'exécution de '{command if shell else ' '.join(command)}'", Colors.FAIL)
            if e.stderr:
                self.print_colored(f"   Erreur: {e.stderr.strip()}", Colors.FAIL)
            return False
        except FileNotFoundError:
            self.print_colored(f"❌ Commande non trouvée: {command[0] if not shell else command}", Colors.FAIL)
            return False

    def ask_user_confirmation(self, message: str) -> bool:
        """Demande une confirmation à l'utilisateur"""
        while True:
            self.print_colored(f"\n{message}", Colors.WARNING)
            response = input(f"{Colors.OKCYAN}Voulez-vous continuer ? (o/n): {Colors.ENDC}").lower().strip()
            
            if response in ['o', 'oui', 'y', 'yes']:
                return True
            elif response in ['n', 'non', 'no']:
                return False
            else:
                self.print_colored("Veuillez répondre par 'o' (oui) ou 'n' (non)", Colors.WARNING)

    def check_prerequisites(self) -> bool:
        """Vérifie que Node.js, npm et Python sont installés"""
        self.print_header("Vérification des prérequis")
        
        prerequisites_ok = True
        missing_prereqs = []
        
        # Vérifier Python
        try:
            result = subprocess.run([sys.executable, "--version"], capture_output=True, text=True)
            python_version = result.stdout.strip()
            self.print_colored(f"✅ {python_version} trouvé", Colors.OKGREEN)
        except:
            self.print_colored("❌ Python non trouvé", Colors.FAIL)
            prerequisites_ok = False
            missing_prereqs.append("Python")

        # Vérifier pip
        try:
            result = subprocess.run([sys.executable, "-m", "pip", "--version"], capture_output=True, text=True)
            pip_version = result.stdout.strip().split('\n')[0]
            self.print_colored(f"✅ {pip_version} trouvé", Colors.OKGREEN)
        except:
            self.print_colored("❌ pip non trouvé", Colors.FAIL)
            prerequisites_ok = False
            missing_prereqs.append("pip")

        # Vérifier Node.js
        try:
            result = subprocess.run(["node", "--version"], capture_output=True, text=True)
            node_version = result.stdout.strip()
            self.print_colored(f"✅ Node.js {node_version} trouvé", Colors.OKGREEN)
        except:
            self.print_colored("❌ Node.js non trouvé", Colors.FAIL)
            prerequisites_ok = False
            missing_prereqs.append("Node.js")

        # Vérifier npm avec différentes méthodes pour Windows
        npm_found = False
        try:
            # Essayer d'abord avec npm.cmd (Windows)
            result = subprocess.run(["npm.cmd", "--version"], capture_output=True, text=True, shell=True)
            if result.returncode == 0:
                npm_version = result.stdout.strip()
                self.print_colored(f"✅ npm {npm_version} trouvé", Colors.OKGREEN)
                npm_found = True
        except:
            pass
        
        if not npm_found:
            try:
                # Essayer avec npm
                result = subprocess.run(["npm", "--version"], capture_output=True, text=True, shell=True)
                if result.returncode == 0:
                    npm_version = result.stdout.strip()
                    self.print_colored(f"✅ npm {npm_version} trouvé", Colors.OKGREEN)
                    npm_found = True
            except:
                pass
        
        if not npm_found:
            self.print_colored("❌ npm non trouvé", Colors.FAIL)
            prerequisites_ok = False
            missing_prereqs.append("npm")

        # Si des prérequis manquent, demander confirmation
        if not prerequisites_ok:
            self.print_colored(f"\n⚠️  Prérequis manquants détectés:", Colors.WARNING)
            for prereq in missing_prereqs:
                self.print_colored(f"   • {prereq}", Colors.FAIL)
            
            self.print_colored(f"\n📋 Instructions d'installation:", Colors.OKBLUE)
            if "Python" in missing_prereqs:
                self.print_colored("   • Python: https://www.python.org/downloads/", Colors.OKCYAN)
            if "Node.js" in missing_prereqs or "npm" in missing_prereqs:
                self.print_colored("   • Node.js (inclut npm): https://nodejs.org/", Colors.OKCYAN)
            
            if not self.ask_user_confirmation("⚠️  Certains prérequis manquent. L'installation pourrait échouer."):
                self.print_colored("❌ Installation annulée par l'utilisateur", Colors.FAIL)
                return False
            else:
                self.print_colored("✅ Continuation forcée par l'utilisateur", Colors.WARNING)

        return True

    def install_frontend_dependencies(self) -> bool:
        """Installe les dépendances frontend avec npm"""
        self.print_header("Installation des dépendances frontend")
        
        package_json = self.root_dir / "package.json"
        if not package_json.exists():
            self.print_colored("❌ package.json non trouvé dans le répertoire racine", Colors.FAIL)
            return False
        
        self.print_colored("📦 Installation des dépendances npm...", Colors.OKBLUE)
        
        # Essayer différentes méthodes pour npm sur Windows
        npm_commands = ["npm install", "npm.cmd install"]
        
        for npm_cmd in npm_commands:
            if self.run_command(npm_cmd, cwd=self.root_dir, capture_output=True, shell=True):
                self.print_colored("✅ Dépendances frontend installées avec succès", Colors.OKGREEN)
                return True
        
        self.print_colored("❌ Échec de l'installation des dépendances frontend", Colors.FAIL)
        return False

    def install_python_dependencies(self) -> bool:
        """Installe les dépendances Python pour tous les services"""
        self.print_header("Installation des dépendances Python pour tous les services")
        
        success_count = 0
        total_services = len(self.services)
        
        for service in self.services:
            service_path = self.root_dir / service["path"]
            requirements_file = service_path / service["requirements"]
            
            self.print_colored(f"\n🔧 {service['name']}", Colors.OKBLUE)
            
            if not service_path.exists():
                self.print_colored(f"⚠️  Répertoire non trouvé: {service_path}", Colors.WARNING)
                continue
                
            if not requirements_file.exists():
                self.print_colored(f"⚠️  {service['requirements']} non trouvé", Colors.WARNING)
                continue
            
            self.print_colored(f"📦 Installation des dépendances pour {service['name']}...", Colors.OKBLUE)
            
            # Utiliser pip install avec le chemin complet vers Python
            command = f"{sys.executable} -m pip install -r {service['requirements']}"
            
            if self.run_command(command, cwd=service_path, capture_output=True):
                self.print_colored(f"✅ {service['name']} - Dépendances installées", Colors.OKGREEN)
                success_count += 1
            else:
                self.print_colored(f"❌ {service['name']} - Échec de l'installation", Colors.FAIL)
                
                # Demander si on continue malgré l'échec
                if not self.ask_user_confirmation(f"L'installation a échoué pour {service['name']}."):
                    self.print_colored("❌ Installation interrompue par l'utilisateur", Colors.FAIL)
                    return False
            
            # Petite pause entre les installations
            time.sleep(0.5)
        
        self.print_colored(f"\n📊 Résumé: {success_count}/{total_services} services configurés", Colors.OKBLUE)
        return success_count > 0

    def show_summary(self, frontend_success: bool, backend_success: bool):
        """Affiche un résumé de l'installation"""
        self.print_header("Résumé de l'installation")
        
        if frontend_success:
            self.print_colored("✅ Dépendances frontend (npm) installées", Colors.OKGREEN)
        else:
            self.print_colored("❌ Échec des dépendances frontend", Colors.FAIL)
        
        if backend_success:
            self.print_colored("✅ Dépendances Python installées pour tous les services", Colors.OKGREEN)
        else:
            self.print_colored("⚠️  Certaines dépendances Python ont échoué", Colors.WARNING)
        
        if frontend_success and backend_success:
            self.print_colored(f"\n🎉 Installation terminée avec succès!", Colors.OKGREEN)
            self.print_colored(f"Vous pouvez maintenant lancer le projet avec:", Colors.OKBLUE)
            self.print_colored(f"  python setup_databases.py", Colors.OKCYAN)
            self.print_colored(f"  python run_project.py", Colors.OKCYAN)
        else:
            self.print_colored(f"\n⚠️  Installation partiellement réussie", Colors.WARNING)
            self.print_colored(f"Vérifiez les erreurs ci-dessus et réessayez", Colors.WARNING)
            
            if not self.ask_user_confirmation("Voulez-vous continuer malgré les erreurs ?"):
                self.print_colored("❌ Processus interrompu par l'utilisateur", Colors.FAIL)
                return False

    def run(self) -> bool:
        """Lance l'installation complète"""
        try:
            self.print_colored(f"""
{Colors.HEADER}{Colors.BOLD}
╔══════════════════════════════════════════════════════════════╗
║                🔧 AMAGON DEPENDENCY INSTALLER                ║
║              Installation automatique v2.0                  ║
╚══════════════════════════════════════════════════════════════╝
{Colors.ENDC}""")
            
            # Vérifier les prérequis avec confirmation utilisateur
            if not self.check_prerequisites():
                return False
            
            # Installer les dépendances frontend
            frontend_success = self.install_frontend_dependencies()
            
            # Si le frontend échoue, demander confirmation
            if not frontend_success:
                if not self.ask_user_confirmation("L'installation frontend a échoué. Continuer avec le backend ?"):
                    self.print_colored("❌ Installation interrompue par l'utilisateur", Colors.FAIL)
                    return False
            
            # Installer les dépendances Python
            backend_success = self.install_python_dependencies()
            
            # Afficher le résumé
            self.show_summary(frontend_success, backend_success)
            
            return frontend_success or backend_success
            
        except KeyboardInterrupt:
            self.print_colored("\n❌ Installation interrompue par l'utilisateur (Ctrl+C)", Colors.FAIL)
            return False
        except Exception as e:
            self.print_colored(f"❌ Erreur inattendue: {e}", Colors.FAIL)
            return False

def main():
    """Fonction principale"""
    installer = DependencyInstaller()
    success = installer.run()
    
    if success:
        print(f"\n{Colors.OKGREEN}🎉 Installation terminée !{Colors.ENDC}")
    else:
        print(f"\n{Colors.FAIL}❌ Installation échouée ou interrompue{Colors.ENDC}")
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
