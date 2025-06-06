# Amagon - E-commerce Platform

A modern e-commerce platform built with React frontend and Django microservices backend, inspired by Amazon's design and functionality.

## 🏗️ Architecture

This project follows a microservices architecture with:

- **Frontend**: React with TypeScript, Tailwind CSS
- **API Gateway**: Django REST Framework (Port 8000)
- **Microservices**:
  - Auth Service (Port 8001)
  - Product Service (Port 8002)
  - Order Service (Port 8003)
  - Inventory Service (Port 8004)
  - Seller Service (Port 8005)
  - Store Service (Port 8006)

## 🗄️ Database

All services use **SQLite** databases for simplicity and portability:
- `gateway_db.sqlite3` - API Gateway
- `auth_db.sqlite3` - Authentication
- `product_db.sqlite3` - Products and categories
- `order_db.sqlite3` - Orders and order items
- `inventory_db.sqlite3` - Inventory management
- `seller_db.sqlite3` - Seller information
- `store_db.sqlite3` - Store management

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Node.js 16+
- npm or yarn

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd amagon
   ```

2. **Install frontend dependencies**
   ```bash
   npm install
   ```

3. **Install Python dependencies for all services**
   ```bash
   # API Gateway
   cd api-gateway
   pip install -r requirements.txt
   cd ..

   # Auth Service
   cd microservices/auth-service
   pip install -r requirements.txt
   cd ../..

   # Product Service
   cd microservices/product-service
   pip install -r requirements.txt
   cd ../..

   # Order Service
   cd microservices/order-service
   pip install -r requirements.txt
   cd ../..

   # Inventory Service
   cd microservices/inventory-service
   pip install -r requirements.txt
   cd ../..

   # Seller Service
   cd microservices/seller-service
   pip install -r requirements.txt
   cd ../..

   # Store Service
   cd microservices/store-service
   pip install -r requirements.txt
   cd ../..
   ```

4. **Setup all databases**
   ```bash
   python setup_databases.py
   ```

5. **Start all services**
   ```bash
   node start.cjs
   ```

The application will be available at:
- Frontend: http://localhost:5173
- API Gateway: http://localhost:8000

## 📁 Project Structure

```
amagon/
├── src/                          # React frontend
│   ├── components/              # Reusable components
│   ├── pages/                   # Page components
│   ├── context/                 # React contexts
│   └── data/                    # Mock data
├── api-gateway/                 # API Gateway service
├── microservices/               # Backend microservices
│   ├── auth-service/           # Authentication
│   ├── product-service/        # Product management
│   ├── order-service/          # Order processing
│   ├── inventory-service/      # Inventory management
│   ├── seller-service/         # Seller management
│   └── store-service/          # Store management
├── setup_databases.py          # Database setup script
└── start.cjs                   # Service orchestration
```

## 🔧 Development

### Running Individual Services

You can run services individually for development:

```bash
# Frontend only
npm run dev

# API Gateway only
cd api-gateway
python manage.py runserver 8000

# Specific microservice
cd microservices/auth-service
python manage.py runserver 8001
```

### Database Management

To reset a specific database:
```bash
cd <service-directory>
rm *.sqlite3
python manage.py makemigrations
python manage.py migrate
```

To reset all databases:
```bash
python setup_databases.py
```

## 🎨 Features

- **Modern UI**: Amazon-inspired design with Tailwind CSS
- **Responsive Design**: Mobile-first approach
- **Product Catalog**: Browse products by categories
- **Shopping Cart**: Add/remove items, quantity management
- **User Authentication**: Login/register functionality
- **Order Management**: Checkout process and order history
- **Microservices**: Scalable backend architecture
- **SQLite**: Simple, file-based database system

## 🛠️ Technologies

### Frontend
- React 18
- TypeScript
- Tailwind CSS
- React Router
- Zustand (State Management)
- Axios (HTTP Client)

### Backend
- Django 5.0
- Django REST Framework
- SQLite
- JWT Authentication

## 📝 API Documentation

The API Gateway routes requests to appropriate microservices:

- `/api/auth/` → Auth Service
- `/api/products/` → Product Service
- `/api/orders/` → Order Service
- `/api/inventory/` → Inventory Service
- `/api/sellers/` → Seller Service
- `/api/stores/` → Store Service

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests
5. Submit a pull request

## 📄 License

This project is for educational purposes only and is not affiliated with Amazon.