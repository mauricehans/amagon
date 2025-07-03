#!/bin/bash

# Script to launch all microservices and the API gateway

echo "Starting API Gateway..."
cd api-gateway
python manage.py runserver 0.0.0.0:8000 &
cd ..
echo "API Gateway started on port 8000."
echo "------------------------------------"

echo "Starting Auth Service..."
cd microservices/auth-service
python manage.py runserver 0.0.0.0:8001 &
cd ../..
echo "Auth Service started on port 8001."
echo "------------------------------------"

echo "Starting Product Service..."
cd microservices/product-service
python manage.py runserver 0.0.0.0:8002 &
cd ../..
echo "Product Service started on port 8002."
echo "------------------------------------"

echo "Starting Inventory Service..."
cd microservices/inventory-service
python manage.py runserver 0.0.0.0:8003 &
cd ../..
echo "Inventory Service started on port 8003."
echo "------------------------------------"

# Assuming Notification Service exists and follows the same pattern
if [ -d "microservices/notification-service" ]; then
    echo "Starting Notification Service..."
    cd microservices/notification-service
    python manage.py runserver 0.0.0.0:8004 &
    cd ../..
    echo "Notification Service started on port 8004."
    echo "------------------------------------"
else
    echo "Notification Service directory not found, skipping."
    echo "------------------------------------"
fi

echo "Starting Seller Service..."
cd microservices/seller-service
python manage.py runserver 0.0.0.0:8005 &
cd ../..
echo "Seller Service started on port 8005."
echo "------------------------------------"

echo "Starting Store Service..."
cd microservices/store-service
python manage.py runserver 0.0.0.0:8006 &
cd ../..
echo "Store Service started on port 8006."
echo "------------------------------------"

echo "Starting Order Service..."
cd microservices/order-service
python manage.py runserver 0.0.0.0:8007 &
cd ../..
echo "Order Service started on port 8007."
echo "------------------------------------"

echo "Starting Admin Service..."
cd microservices/admin-service
python manage.py runserver 0.0.0.0:8008 &
cd ../..
echo "Admin Service started on port 8008."
echo "------------------------------------"

echo "All services launched."
echo "Press Ctrl+C to stop all background services (this might require multiple Ctrl+C presses or manual termination)."
echo "Alternatively, use 'killall python' or identify PIDs to stop them."

# Keep the script running to easily stop all with Ctrl+C, or use trap
# trap "echo 'Stopping all services...'; killall python; exit" SIGINT SIGTERM # This can be aggressive

wait # Wait for all background jobs to complete (which they won't, they are servers)
# This means Ctrl+C in the terminal where this script is run should propagate to children.
