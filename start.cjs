const { spawn } = require('child_process');
const path = require('path');

class ServiceManager {
    constructor() {
        this.services = new Map();
        this.shouldRun = true;
        
        this.serviceConfigs = {
            "API Gateway": {
                cmd: ['python', 'manage.py', 'runserver', '8000'],
                cwd: 'api-gateway',
                readyMessage: 'Starting development server at http://127.0.0.1:8000/',
            },
            "Auth Service": {
                cmd: ['python', 'manage.py', 'runserver', '8001'],
                cwd: 'microservices/auth-service',
                readyMessage: 'Starting development server at http://127.0.0.1:8001/',
            },
            "Product Service": {
                cmd: ['python', 'manage.py', 'runserver', '8002'],
                cwd: 'microservices/product-service',
                readyMessage: 'Starting development server at http://127.0.0.1:8002/',
            },
            "Order Service": {
                cmd: ['python', 'manage.py', 'runserver', '8003'],
                cwd: 'microservices/order-service',
                readyMessage: 'Starting development server at http://127.0.0.1:8003/',
            },
            "Inventory Service": {
                cmd: ['python', 'manage.py', 'runserver', '8004'],
                cwd: 'microservices/inventory-service',
                readyMessage: 'Starting development server at http://127.0.0.1:8004/',
            },
            "Seller Service": {
                cmd: ['python', 'manage.py', 'runserver', '8005'],
                cwd: 'microservices/seller-service',
                readyMessage: 'Starting development server at http://127.0.0.1:8005/',
            },
            "Store Service": {
                cmd: ['python', 'manage.py', 'runserver', '8006'],
                cwd: 'microservices/store-service',
                readyMessage: 'Starting development server at http://127.0.0.1:8006/',
            },
            "Frontend": {
                cmd: ['npm', 'run', 'dev'],
                cwd: '.',
                readyMessage: 'Local:',
            }
        };
    }

    startService(serviceName, config) {
        return new Promise((resolve, reject) => {
            try {
                const process = spawn(config.cmd[0], config.cmd.slice(1), {
                    cwd: path.resolve(process.cwd(), config.cwd),
                    stdio: ['ignore', 'pipe', 'pipe']
                });

                process.stdout.on('data', (data) => {
                    const message = data.toString().trim();
                    console.log(`[${serviceName}] ${message}`);
                    
                    if (message.includes(config.readyMessage)) {
                        resolve(process);
                    }
                });

                process.stderr.on('data', (data) => {
                    console.error(`[${serviceName}] ${data.toString().trim()}`);
                });

                process.on('error', (err) => {
                    console.error(`Failed to start ${serviceName}:`, err);
                    reject(err);
                });

                process.on('exit', (code) => {
                    if (code !== null && this.shouldRun) {
                        console.log(`${serviceName} exited with code ${code}, restarting...`);
                        this.startService(serviceName, config)
                            .then(newProcess => {
                                this.services.set(serviceName, newProcess);
                            })
                            .catch(err => {
                                console.error(`Failed to restart ${serviceName}:`, err);
                            });
                    }
                });

                this.services.set(serviceName, process);

                // Set a timeout for service startup
                setTimeout(() => {
                    reject(new Error(`Timeout waiting for ${serviceName} to be ready`));
                }, 30000);

            } catch (err) {
                reject(err);
            }
        });
    }

    async startAllServices() {
        try {
            // Start backend services first
            const backendServices = Object.entries(this.serviceConfigs)
                .filter(([name]) => name !== "Frontend");

            for (const [serviceName, config] of backendServices) {
                console.log(`Starting ${serviceName}...`);
                await this.startService(serviceName, config);
                console.log(`${serviceName} is ready`);
            }

            // Start frontend last
            console.log("Starting Frontend...");
            await this.startService("Frontend", this.serviceConfigs["Frontend"]);
            console.log("Frontend is starting...");

        } catch (err) {
            console.error("Error starting services:", err);
            this.cleanup();
            process.exit(1);
        }
    }

    cleanup() {
        this.shouldRun = false;
        console.log("\nShutting down services...");
        
        for (const [serviceName, process] of this.services.entries()) {
            console.log(`Stopping ${serviceName}...`);
            try {
                process.kill();
            } catch (err) {
                console.error(`Error stopping ${serviceName}:`, err);
            }
        }
    }
}

// Handle process termination
process.on('SIGINT', () => {
    console.log("\nShutting down...");
    if (global.manager) {
        global.manager.cleanup();
    }
    process.exit(0);
});

// Start the service manager
try {
    global.manager = new ServiceManager();
    global.manager.startAllServices();
} catch (err) {
    console.error("Unexpected error:", err);
    if (global.manager) {
        global.manager.cleanup();
    }
    process.exit(1);
}