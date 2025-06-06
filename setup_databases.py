#!/usr/bin/env python3
"""
Script to initialize all SQLite databases for the microservices
"""

import os
import subprocess
import sys
from pathlib import Path

def run_command(command, cwd=None):
    """Run a shell command and return the result"""
    try:
        result = subprocess.run(
            command, 
            shell=True, 
            cwd=cwd, 
            capture_output=True, 
            text=True,
            check=True
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Error running command '{command}': {e}")
        print(f"Error output: {e.stderr}")
        return None

def setup_service_database(service_path, service_name):
    """Setup database for a specific service"""
    print(f"\n🔧 Setting up {service_name} database...")
    
    # Check if manage.py exists
    manage_py = os.path.join(service_path, 'manage.py')
    if not os.path.exists(manage_py):
        print(f"❌ manage.py not found in {service_path}")
        return False
    
    # Run migrations
    print(f"   Running makemigrations for {service_name}...")
    result = run_command("python manage.py makemigrations", cwd=service_path)
    if result is None:
        print(f"❌ Failed to make migrations for {service_name}")
        return False
    
    print(f"   Running migrate for {service_name}...")
    result = run_command("python manage.py migrate", cwd=service_path)
    if result is None:
        print(f"❌ Failed to migrate {service_name}")
        return False
    
    print(f"✅ {service_name} database setup complete")
    return True

def main():
    """Main function to setup all databases"""
    print("🚀 Setting up SQLite databases for all microservices...")
    
    # Define all services and their paths
    services = {
        "API Gateway": "api-gateway",
        "Auth Service": "microservices/auth-service",
        "Product Service": "microservices/product-service",
        "Order Service": "microservices/order-service",
        "Inventory Service": "microservices/inventory-service",
        "Seller Service": "microservices/seller-service",
        "Store Service": "microservices/store-service",
    }
    
    success_count = 0
    total_services = len(services)
    
    for service_name, service_path in services.items():
        if os.path.exists(service_path):
            if setup_service_database(service_path, service_name):
                success_count += 1
        else:
            print(f"❌ Service directory not found: {service_path}")
    
    print(f"\n📊 Database setup complete: {success_count}/{total_services} services configured")
    
    if success_count == total_services:
        print("🎉 All databases are ready!")
        print("\nYou can now start the services using:")
        print("   node start.cjs")
    else:
        print("⚠️  Some databases failed to setup. Please check the errors above.")
        sys.exit(1)

if __name__ == "__main__":
    main()