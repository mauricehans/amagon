import subprocess
import time
import signal
import sys
import os
from typing import Dict, List
import threading
import queue
import atexit

class ServiceManager:
    def __init__(self):
        self.services: Dict[str, subprocess.Popen] = {}
        self.log_queue = queue.Queue()
        self.should_run = True
        
        # Define services with their commands and working directories
        self.service_configs = {
            "API Gateway": {
                "cmd": ["python", "manage.py", "runserver", "8000"],
                "cwd": "api-gateway",
                "ready_message": "Starting development server at http://127.0.0.1:8000/",
            },
            "Auth Service": {
                "cmd": ["python", "manage.py", "runserver", "8001"],
                "cwd": "microservices/auth-service",
                "ready_message": "Starting development server at http://127.0.0.1:8001/",
            },
            "Product Service": {
                "cmd": ["python", "manage.py", "runserver", "8002"],
                "cwd": "microservices/product-service",
                "ready_message": "Starting development server at http://127.0.0.1:8002/",
            },
            "Order Service": {
                "cmd": ["python", "manage.py", "runserver", "8003"],
                "cwd": "microservices/order-service",
                "ready_message": "Starting development server at http://127.0.0.1:8003/",
            },
            "Inventory Service": {
                "cmd": ["python", "manage.py", "runserver", "8004"],
                "cwd": "microservices/inventory-service",
                "ready_message": "Starting development server at http://127.0.0.1:8004/",
            },
            "Seller Service": {
                "cmd": ["python", "manage.py", "runserver", "8005"],
                "cwd": "microservices/seller-service",
                "ready_message": "Starting development server at http://127.0.0.1:8005/",
            },
            "Store Service": {
                "cmd": ["python", "manage.py", "runserver", "8006"],
                "cwd": "microservices/store-service",
                "ready_message": "Starting development server at http://127.0.0.1:8006/",
            },
            "Frontend": {
                "cmd": ["npm", "run", "dev"],
                "cwd": ".",
                "ready_message": "Local:",
            }
        }

    def log_reader(self, process: subprocess.Popen, service_name: str):
        """Read logs from a process and put them in the queue"""
        while self.should_run:
            if process.poll() is not None:
                break
            
            line = process.stdout.readline()
            if line:
                self.log_queue.put((service_name, line.decode().strip()))

    def log_printer(self):
        """Print logs from the queue"""
        while self.should_run:
            try:
                service_name, message = self.log_queue.get(timeout=1)
                print(f"[{service_name}] {message}")
            except queue.Empty:
                continue

    def start_service(self, service_name: str, config: dict) -> subprocess.Popen:
        """Start a service and return its process"""
        try:
            process = subprocess.Popen(
                config["cmd"],
                cwd=config["cwd"],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                bufsize=1,
                universal_newlines=False
            )
            
            # Start log reader thread for this process
            thread = threading.Thread(
                target=self.log_reader,
                args=(process, service_name),
                daemon=True
            )
            thread.start()
            
            return process
        except Exception as e:
            print(f"Failed to start {service_name}: {str(e)}")
            return None

    def check_service_ready(self, service_name: str, process: subprocess.Popen, ready_message: str) -> bool:
        """Check if a service is ready by looking for its ready message"""
        start_time = time.time()
        while time.time() - start_time < 30:  # 30 seconds timeout
            if process.poll() is not None:
                return False
            
            try:
                line = self.log_queue.get_nowait()
                if ready_message in line[1]:
                    return True
            except queue.Empty:
                time.sleep(0.1)
                continue
        
        return False

    def start_all_services(self):
        """Start all services in the correct order"""
        # Start log printer thread
        log_printer_thread = threading.Thread(target=self.log_printer, daemon=True)
        log_printer_thread.start()

        # Start backend services first
        backend_services = [name for name in self.service_configs.keys() if name != "Frontend"]
        for service_name in backend_services:
            config = self.service_configs[service_name]
            print(f"Starting {service_name}...")
            
            process = self.start_service(service_name, config)
            if process is None:
                print(f"Failed to start {service_name}")
                self.cleanup()
                sys.exit(1)
            
            self.services[service_name] = process
            
            # Wait for service to be ready
            if not self.check_service_ready(service_name, process, config["ready_message"]):
                print(f"Timeout waiting for {service_name} to be ready")
                self.cleanup()
                sys.exit(1)
            
            print(f"{service_name} is ready")

        # Start frontend last
        frontend_config = self.service_configs["Frontend"]
        print("Starting Frontend...")
        frontend_process = self.start_service("Frontend", frontend_config)
        if frontend_process is None:
            print("Failed to start Frontend")
            self.cleanup()
            sys.exit(1)
        
        self.services["Frontend"] = frontend_process
        print("Frontend is starting...")

    def monitor_services(self):
        """Monitor services and restart them if they crash"""
        while self.should_run:
            for service_name, process in list(self.services.items()):
                if process.poll() is not None:
                    print(f"{service_name} has crashed, restarting...")
                    config = self.service_configs[service_name]
                    new_process = self.start_service(service_name, config)
                    if new_process is not None:
                        self.services[service_name] = new_process
                    else:
                        print(f"Failed to restart {service_name}")
            
            time.sleep(1)

    def cleanup(self):
        """Clean up all services"""
        self.should_run = False
        print("\nShutting down services...")
        
        for service_name, process in self.services.items():
            print(f"Stopping {service_name}...")
            try:
                process.terminate()
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                process.kill()
            except Exception as e:
                print(f"Error stopping {service_name}: {str(e)}")

def signal_handler(signum, frame):
    """Handle shutdown signals"""
    print("\nReceived shutdown signal")
    manager.cleanup()
    sys.exit(0)

if __name__ == "__main__":
    # Register signal handlers
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    # Register cleanup handler
    manager = ServiceManager()
    atexit.register(manager.cleanup)

    try:
        # Start all services
        manager.start_all_services()
        
        # Monitor services
        manager.monitor_services()
    except KeyboardInterrupt:
        print("\nShutting down...")
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
    finally:
        manager.cleanup()