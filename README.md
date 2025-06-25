# Amagon - E-commerce Platform

A modern e-commerce platform built with React frontend and Django microservices backend, inspired by Amazon's design and functionality.

## 🏗️ Architecture

This project follows a microservices architecture with:

- **Frontend**: React with TypeScript, Tailwind CSS
- **API Gateway**: Django REST Framework (Port 8000)
- **Microservices**:
  - Auth Service (Port 8001) - User authentication
  - Product Service (Port 8002) - Product management
  - Order Service (Port 8003) - Order processing
  - Inventory Service (Port 8004) - Stock management
  - Seller Service (Port 8005) - Seller dashboard
  - Store Service (Port 8006) - Store management

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

### 🎯 **Méthode Recommandée - Scripts Automatisés**

Le projet inclut 3 scripts Python à la racine pour une installation et un lancement automatiques :

#### **1. Installation des dépendances (optionnel)**
```bash
python install_dependencies.py
```
- Installe automatiquement toutes les dépendances Python et npm
- Vérifie les prérequis système
- Gestion intelligente des erreurs
- Compatible Windows/Mac/Linux

#### **2. Configuration des bases de données**
```bash
python setup_databases.py
```
- Configure automatiquement toutes les bases de données SQLite
- Crée les migrations Django
- Initialise les données de base
- Crée un superutilisateur (admin/admin123)

#### **3. Lancement du projet complet**
```bash
python run_project.py
```
- Lance automatiquement tous les services **backend (tous les microservices Python)** et le frontend React
- Gère les dépendances manquantes
- Surveille et redémarre les services en cas d'erreur
- Interface colorée avec statut en temps réel

### 🎉 **Lancement en Une Commande**

Pour une installation et un lancement complets :

```bash
# Installation complète (si première fois)
python install_dependencies.py

# Configuration des bases de données
python setup_databases.py

# Lancement du projet
python run_project.py
```

Ou directement :
```bash
python run_project.py
```
*(Le script gère automatiquement les dépendances et la configuration)*

### 📱 **Accès aux Services**

Une fois lancé, le projet sera accessible sur :
- **Frontend React** : http://localhost:5173
- **API Gateway** : http://localhost:8000
- **Interface Admin** : http://localhost:8001/admin/
  - Utilisateur : `admin`
  - Mot de passe : `admin123`

### 🛑 **Arrêt du Projet**

Pour arrêter tous les services :
- Appuyez sur `Ctrl+C` dans le terminal où `run_project.py` s'exécute
- Tous les services seront arrêtés automatiquement

## 📁 Project Structure

```
amagon/
├── 📄 install_dependencies.py    # Installation automatique des dépendances
├── 📄 setup_databases.py         # Configuration des bases de données
├── 📄 run_project.py             # Lancement automatique du projet
├── src/                          # React frontend
│   ├── components/              # Reusable components
│   ├── pages/                   # Page components
│   ├── context/                 # React contexts
│   └── data/                    # Mock data
├── api-gateway/                 # API Gateway service
└── microservices/               # Backend microservices
    ├── auth-service/           # Authentication
    ├── product-service/        # Product management
    ├── order-service/          # Order processing
    ├── inventory-service/      # Inventory management
    ├── seller-service/         # Seller management
    └── store-service/          # Store management
```

## 🔧 Development

### **Scripts de Développement Avancés**

Les scripts Python offrent des fonctionnalités avancées :

#### **🔍 Diagnostics Automatiques**
- Vérification des prérequis système
- Détection des dépendances manquantes
- Validation des configurations
- Rapports d'erreur détaillés

#### **🔄 Gestion Intelligente**
- Installation sélective des dépendances manquantes
- Redémarrage automatique des services en cas d'erreur
- Surveillance en temps réel
- Nettoyage automatique à l'arrêt

#### **🎨 Interface Utilisateur**
- Affichage coloré avec codes couleur
- Barres de progression
- Statut en temps réel de chaque service
- Messages d'aide contextuels

### **Lancement Manuel (Développement)**

Si vous préférez lancer les services individuellement :

```bash
# Frontend seulement
npm run dev

# API Gateway seulement
cd api-gateway
python manage.py runserver 8000

# Service spécifique
cd microservices/auth-service
python manage.py runserver 8001
```

### **Gestion des Bases de Données**

Pour réinitialiser une base de données spécifique :
```bash
cd <service-directory>
rm *.sqlite3
python manage.py makemigrations
python manage.py migrate
```

Pour réinitialiser toutes les bases de données :
```bash
python setup_databases.py
```

## 🎨 Features

- **Modern UI**: Amazon-inspired design with Tailwind CSS
- **Responsive Design**: Mobile-first approach
- **Product Catalog**: Browse products by categories
- **Shopping Cart**: Add/remove items, quantity management
- **User Authentication**: Login/register functionality
- **Seller Dashboard**: Complete seller management system
- **Order Management**: Checkout process and order history
- **Inventory System**: Multi-store stock management
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

- `/api/auth/` → Auth Service (Port 8001)
- `/api/products/` → Product Service (Port 8002)
- `/api/orders/` → Order Service (Port 8003)
- `/api/inventory/` → Inventory Service (Port 8004)
- `/api/sellers/` → Seller Service (Port 8005)
- `/api/stores/` → Store Service (Port 8006)

### **🔐 Authentication Endpoints**
- `POST /api/auth/register/` - User registration
- `POST /api/auth/login/` - User login
- `GET /api/auth/profile/` - User profile
- `POST /api/auth/verify-token/` - Token verification

### **🏪 Seller Endpoints**
- `POST /api/sellers/register/` - Seller registration
- `POST /api/sellers/login/` - Seller login
- `GET /api/sellers/dashboard/` - Seller dashboard
- `GET/POST /api/sellers/products/` - Product management

## 🚨 Troubleshooting

### **Problèmes Courants**

#### **Port déjà utilisé**
```bash
# Tuer les processus sur les ports utilisés
python run_project.py
# Le script gère automatiquement les conflits de ports
```

#### **Dépendances manquantes**
```bash
python install_dependencies.py
# Réinstalle toutes les dépendances manquantes
```

#### **Base de données corrompue**
```bash
python setup_databases.py
# Recrée toutes les bases de données
```

#### **Erreurs de permissions**
- Sur Windows : Exécuter en tant qu'administrateur
- Sur Mac/Linux : Utiliser `sudo` si nécessaire

#### **Page 404 ou redirection vers Amazon lors du clic sur un produit**
- Vérifiez que la route `/product/:id` (ou `/products/:id`) existe dans votre code React (`src/pages/ProductPage.tsx` ou similaire).
- Dans `src/App.tsx` (ou le fichier de routes), assurez-vous d’avoir une ligne comme :
  ```jsx
  <Route path="/product/:id" element={<ProductPage />} />
  ```
- Vérifiez que vos liens utilisent `react-router-dom` :
  ```jsx
  <Link to={`/product/${product.id}`}>Voir le produit</Link>
  ```
- Si vous voyez une page Amazon, c’est probablement un lien externe ou une mauvaise gestion du fallback 404.
- Vérifiez que le backend retourne bien les détails du produit pour l’ID demandé.

#### **Checklist de vérification pour la page produit**
1. **Route React pour la page produit**
   - Ouvrez `src/App.tsx` (ou le fichier de routes principal).
   - Vérifiez la présence de :
     ```jsx
     <Route path="/product/:id" element={<ProductPage />} />
     ```
   - Le composant `ProductPage` doit exister dans `src/pages/ProductPage.tsx` (ou similaire).

2. **Lien vers la page produit**
   - Dans la liste des produits (`src/components/ProductCard.tsx` ou équivalent), vérifiez que le lien utilise `react-router-dom` :
     ```jsx
     <Link to={`/product/${product.id}`}>Voir le produit</Link>
     ```
   - Il ne doit pas s’agir d’un lien externe (`<a href="...amazon.com...">`).

3. **Fallback 404**
   - Vérifiez que la route fallback (`*`) dans votre routeur affiche une page 404 personnalisée, pas une redirection externe :
     ```jsx
     <Route path="*" element={<NotFoundPage />} />
     ```

4. **Backend : Endpoint produit**
   - L’API `/api/products/<id>/` doit retourner les détails du produit demandé.
   - Testez avec :
     ```bash
     curl http://localhost:8002/api/products/1/
     ```
   - Vous devez recevoir un JSON avec les infos du produit, pas une erreur 404.

5. **Console et logs**
   - Ouvrez la console du navigateur et vérifiez l’absence d’erreurs lors du clic sur un produit.
   - Vérifiez les logs du backend pour toute erreur lors de la requête produit.

6. **Redémarrage**
   - Après toute modification, redémarrez le frontend (`npm run dev`) et le backend concerné.

### **Logs et Debugging**

Les scripts fournissent des logs détaillés :
- ✅ Messages de succès en vert
- ⚠️ Avertissements en jaune
- ❌ Erreurs en rouge
- 📋 Informations en bleu

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test with `python run_project.py`
5. Submit a pull request

## 📄 License

This project is for educational purposes only and is not affiliated with Amazon.

---

## 🎯 **Résumé des Commandes Essentielles**

```bash
# Installation complète (première fois)
python install_dependencies.py

# Configuration des bases de données
python setup_databases.py

# Lancement du projet
python run_project.py

# Arrêt : Ctrl+C
```

**Le projet sera accessible sur http://localhost:5173** 🚀