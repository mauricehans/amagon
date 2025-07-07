import os
import sys
import django

# Ajout du dossier parent au sys.path pour que 'product_app' soit trouvable
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'product_app.settings')
django.setup()

from product_app.models import Category, Product, ProductImage

def run():
    # Créez une catégorie si elle n'existe pas
    categories_to_create = [
        {"name": "Electronics", "description": "Electronic devices"},
        {"name": "Books", "description": "Books and literature"},
        {"name": "Home & Kitchen", "description": "Home and kitchen appliances"},
        {"name": "Fashion", "description": "Clothing and accessories"},
        {"name": "Toys & Games", "description": "Toys and games for all ages"},
    ]

    for cat_data in categories_to_create:
        Category.objects.get_or_create(name=cat_data["name"], defaults={"description": cat_data["description"]})
    
    # Utilisez la catégorie 'Electronics' pour les produits existants si elle est créée
    electronics_cat = Category.objects.get(name="Electronics")

    # Exemple de produits à ajouter
    products = [
        {
            "name": "Smartphone X100",
            "description": "Smartphone tres tactile et facile a utiliser ",
            "sku": "X100-001",
            "price": 18,
            "cost": 45,
            "unit": "pièce",
            "barcode": "1234567890123",
            "weight": 0.18,
            "dimensions": {"longueur": 15, "largeur": 7, "hauteur": 0.8},
            "is_active": True,
            "category_name": "Electronics", # Assign to Electronics
            "images": [
               
                {"url": "https://m.media-amazon.com/images/I/71NKGnsIkvL.jpg", "is_primary": True}
            ]
        },
        {
            "name": "Casque Bluetooth",
            "description": "Casque sans fil avec réduction de bruit.",
            "sku": "BT-HEAD-002",
            "price": 89.99,
            "cost": 50.00,
            "unit": "pièce",
            "barcode": "9876543210987",
            "weight": 0.25,
            "dimensions": {"longueur": 18, "largeur": 15, "hauteur": 7},
            "is_active": True,
            "category_name": "Electronics", # Assign to Electronics
            "images": [
                {"url": "https://resize-europe1.lanmedia.fr/img/var/europe1/storage/images/media/images/02_beats-studio3/58239346-1-fre-FR/02_Beats-Studio3.jpg", "is_primary": True}
            ]
        },
        {
            "name": "Montre Connectée Pro",
            "description": "Montre intelligente avec suivi de santé et notifications.",
            "sku": "WATCH-PRO-003",
            "price": 129.99,
            "cost": 80.00,
            "unit": "pièce",
            "barcode": "1111111111111",
            "weight": 0.05,
            "dimensions": {"longueur": 4, "largeur": 4, "hauteur": 1},
            "is_active": True,
            "category_name": "Electronics", # Assign to Electronics
            "images": [
                {"url": "https://m.media-amazon.com/images/I/617psPDxTLL._AC_SX679_.jpg", "is_primary": True}
            ]
        },
        {
            "name": "Ordinateur Portable Slim",
            "description": "Laptop léger et puissant pour le travail et les loisirs.",
            "sku": "LAPTOP-SLIM-004",
            "price": 899.99,
            "cost": 650.00,
            "unit": "pièce",
            "barcode": "2222222222222",
            "weight": 1.3,
            "dimensions": {"longueur": 32, "largeur": 22, "hauteur": 1.8},
            "is_active": True,
            "category_name": "Electronics", # Assign to Electronics
            "images": [
                {"url": "https://www.cdiscount.com/pdt2/7/f/r/1/700x700/82xj0047fr/rw/pc-portable-chromebook-lenovo-ideapad-slim-3-14m86.jpg", "is_primary": True}
            ]
        },
        {
            "name": "Enceinte Bluetooth",
            "description": "Enceinte portable avec son stéréo et autonomie 12h.",
            "sku": "SPEAKER-BT-005",
            "price": 49.99,
            "cost": 25.00,
            "unit": "pièce",
            "barcode": "3333333333333",
            "weight": 0.4,
            "dimensions": {"longueur": 16, "largeur": 7, "hauteur": 7},
            "is_active": True,
            "category_name": "Electronics", # Assign to Electronics
            "images": [
                {"url": "https://mmkdo.fr/11356-large_default/enceinte-led-bluetooth-15-w.jpg", "is_primary": True}
            ]
        },
        {
            "name": "Tablette 10 pouces",
            "description": "Tablette tactile HD, idéale pour la lecture et le streaming.",
            "sku": "TABLET-10-006",
            "price": 199.99,
            "cost": 120.00,
            "unit": "pièce",
            "barcode": "4444444444444",
            "weight": 0.5,
            "dimensions": {"longueur": 24, "largeur": 16, "hauteur": 0.9},
            "is_active": True,
            "category_name": "Electronics", # Assign to Electronics
            "images": [
                {"url": "https://image.darty.com/darty?type=image&source=/market/2023/06/05/22062658_3723_1.jpg&width=497&height=330&quality=95&effects=Pad(CC,FFFFFF)", "is_primary": True}
            ]
        },
        {
            "name": "Chargeur Rapide USB-C",
            "description": "Chargeur mural 30W compatible smartphones et tablettes.",
            "sku": "CHARGER-USB-C-007",
            "price": 19.99,
            "cost": 8.00,
            "unit": "pièce",
            "barcode": "5555555555555",
            "weight": 0.08,
            "dimensions": {"longueur": 6, "largeur": 4, "hauteur": 2.5},
            "is_active": True,
            "category_name": "Electronics", # Assign to Electronics
            "images": [
                {"url": "https://www.cdiscount.com/pdt2/0/6/9/1/700x700/efc3665329311069/rw/pack-chargeur-rapide-25w-blanc-type-c-cable-type.jpg", "is_primary": True}
            ]
        },
        {
            "name": "Souris Sans Fil",
            "description": "Souris ergonomique avec connexion Bluetooth.",
            "sku": "MOUSE-BT-008",
            "price": 24.99,
            "cost": 10.00,
            "unit": "pièce",
            "barcode": "6666666666666",
            "weight": 0.09,
            "dimensions": {"longueur": 11, "largeur": 6, "hauteur": 3.5},
            "is_active": True,
            "category_name": "Electronics", # Assign to Electronics
            "images": [
                {"url": "https://m.media-amazon.com/images/I/51YZVx82mlL._AC_SX679_.jpg", "is_primary": True}
            ]
        },
        {
            "name": "Clavier Mécanique RGB",
            "description": "Clavier rétroéclairé pour gamers.",
            "sku": "KEYBOARD-RGB-009",
            "price": 69.99,
            "cost": 35.00,
            "unit": "pièce",
            "barcode": "7777777777777",
            "weight": 0.7,
            "dimensions": {"longueur": 44, "largeur": 13, "hauteur": 3.5},
            "is_active": True,
            "category_name": "Electronics", # Assign to Electronics
            "images": [
                {"url": "https://media.ldlc.com/r705/ld/products/00/05/96/67/LD0005966749.jpg", "is_primary": True}
            ]
        },
        {
            "name": "Webcam Full HD",
            "description": "Webcam 1080p avec micro intégré.",
            "sku": "WEBCAM-HD-010",
            "price": 39.99,
            "cost": 18.00,
            "unit": "pièce",
            "barcode": "8888888888888",
            "weight": 0.12,
            "dimensions": {"longueur": 8, "largeur": 3, "hauteur": 3},
            "is_active": True,
            "category_name": "Electronics", # Assign to Electronics
            "images": [
                {"url": "https://img-1.kwcdn.com/product/fancy/c08b3b4d-dc92-4d0e-932e-803b9ff76429.jpg?imageView2/2/w/264/q/70/format/webp", "is_primary": True}
            ]
        },
        {
            "name": "Disque SSD 1To",
            "description": "Stockage rapide pour PC et Mac.",
            "sku": "SSD-1TB-011",
            "price": 109.99,
            "cost": 70.00,
            "unit": "pièce",
            "barcode": "9999999999999",
            "weight": 0.06,
            "dimensions": {"longueur": 10, "largeur": 7, "hauteur": 0.7},
            "is_active": True,
            "category_name": "Electronics", # Assign to Electronics
            "images": [
                {"url": "https://m.media-amazon.com/images/I/51Yif3RXFVL._AC_SL1080_.jpg", "is_primary": True}
            ]
        },
        {
            "name": "Carte Mémoire 128Go",
            "description": "Carte microSD rapide pour smartphones et caméras.",
            "sku": "SDCARD-128-012",
            "price": 29.99,
            "cost": 12.00,
            "unit": "pièce",
            "barcode": "1010101010101",
            "weight": 0.01,
            "dimensions": {"longueur": 1.5, "largeur": 1.1, "hauteur": 0.1},
            "is_active": True,
            "category_name": "Electronics", # Assign to Electronics
            "images": [
                {"url": "https://www.prophot.com/455239-superlarge_default/sandisk-carte-memoire-sdxc-uhs-i-extreme-pro-128gb-170mo-s-c10-u3-v30.jpg", "is_primary": True}
            ]
        },
        {
            "name": "Écouteurs Intra-auriculaires",
            "description": "Écouteurs filaires avec micro.",
            "sku": "EARPHONES-013",
            "price": 14.99,
            "cost": 5.00,
            "unit": "pièce",
            "barcode": "1212121212121",
            "weight": 0.02,
            "dimensions": {"longueur": 8, "largeur": 2, "hauteur": 2},
            "is_active": True,
            "category_name": "Electronics", # Assign to Electronics
            "images": [
                {"url": "https://static.fnac-static.com/multimedia/Images/F9/8F/48/10/17074425-3-1520-2/tsp20250409112252/Ecouteurs-intra-auriculaire-Sony-WF-C500-Bluetooth-Noir.jpg", "is_primary": True}
            ]
        },
        {
            "name": "Batterie Externe 10000mAh",
            "description": "Batterie portable pour recharger vos appareils.",
            "sku": "POWERBANK-014",
            "price": 34.99,
            "cost": 15.00,
            "unit": "pièce",
            "barcode": "1313131313131",
            "weight": 0.22,
            "dimensions": {"longueur": 14, "largeur": 7, "hauteur": 1.5},
            "is_active": True,
            "category_name": "Electronics", # Assign to Electronics
            "images": [
                {"url": "https://zenkaa.fr/16056-large_default/batterie-externe-noire-10000-mah-powerhub10-black-de-vortex.jpg", "is_primary": True}
            ]
        },
        {
            "name": "Projecteur LED Portable",
            "description": "Mini projecteur pour films et présentations.",
            "sku": "PROJECTOR-015",
            "price": 159.99,
            "cost": 90.00,
            "unit": "pièce",
            "barcode": "1414141414141",
            "weight": 0.9,
            "dimensions": {"longueur": 18, "largeur": 13, "hauteur": 6},
            "is_active": True,
            "category_name": "Electronics", # Assign to Electronics
            "images": [
                {"url": "https://bati-solution.fr/1180-large_default/theard-projecteur-led-portable-rechargeable-20w.jpg", "is_primary": True}
            ]
        },
        {
            "name": "Caméra de Surveillance WiFi",
            "description": "Caméra connectée pour la sécurité de votre maison.",
            "sku": "CAMERA-WIFI-016",
            "price": 59.99,
            "cost": 28.00,
            "unit": "pièce",
            "barcode": "1515151515151",
            "weight": 0.15,
            "dimensions": {"longueur": 7, "largeur": 7, "hauteur": 10},
            "is_active": True,
            "category_name": "Electronics", # Assign to Electronics
            "images": [
                {"url": "https://www.video-surveillance-direct.com/1088-large_default/camera-ip-wifi-antivandale-dvr-sans-fil.jpg", "is_primary": True}
            ]
        },
        {
            "name": "Routeur WiFi 6",
            "description": "Routeur haut débit pour toute la maison.",
            "sku": "ROUTER-WIFI6-017",
            "price": 89.99,
            "cost": 45.00,
            "unit": "pièce",
            "barcode": "1616161616161",
            "weight": 0.35,
            "dimensions": {"longueur": 20, "largeur": 13, "hauteur": 3},
            "is_active": True,
            "category_name": "Electronics", # Assign to Electronics
            "images": [
                {"url": "https://www.busiboutique.com/medias/boutique/319566/586eaf12-0738-4981-9628-87e2525c8024.jpg", "is_primary": True}
            ]
        },
        {
            "name": "Lampe LED Connectée",
            "description": "Lampe intelligente contrôlable via smartphone.",
            "sku": "LAMP-LED-018",
            "price": 24.99,
            "cost": 9.00,
            "unit": "pièce",
            "barcode": "1717171717171",
            "weight": 0.18,
            "dimensions": {"longueur": 12, "largeur": 12, "hauteur": 18},
            "is_active": True,
            "category_name": "Electronics", # Assign to Electronics
            "images": [
                {"url": "https://www.silamp.fr/cdn/shop/products/SY-A60S-WF-RGBCW-9W-zoom.jpg?v=1691765887", "is_primary": True}
            ]
        },
        {
            "name": "Aspirateur Robot",
            "description": "Robot aspirateur autonome avec navigation intelligente.",
            "sku": "ROBOT-VAC-019",
            "price": 249.99,
            "cost": 160.00,
            "unit": "pièce",
            "barcode": "1818181818181",
            "weight": 2.8,
            "dimensions": {"longueur": 34, "largeur": 34, "hauteur": 9},
            "is_active": True,
            "category_name": "Electronics", # Assign to Electronics
            "images": [
                {"url": "https://media.carrefour.fr/medias/e1ed996468004f30aca4b828e7b678b7/p_1500x1500/5060944996666_0.jpg", "is_primary": True}
            ]
        },
        {
            "name": "Imprimante Jet d'Encre",
            "description": "Imprimante couleur multifonction WiFi.",
            "sku": "PRINTER-INK-020",
            "price": 79.99,
            "cost": 40.00,
            "unit": "pièce",
            "barcode": "1919191919191",
            "weight": 3.2,
            "dimensions": {"longueur": 42, "largeur": 30, "hauteur": 15},
            "is_active": True,
            "category_name": "Electronics", # Assign to Electronics
            "images": [
                {"url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRZxNilI4WMjEiOBWGSo_T0CMeStkKBPXB9LA&s", "is_primary": True}
            ]
        },
        {
            "name": "Tapis de Souris XXL",
            "description": "Tapis de souris grande taille pour bureau.",
            "sku": "MOUSEPAD-XXL-021",
            "price": 15.99,
            "cost": 4.00,
            "unit": "pièce",
            "barcode": "2020202020202",
            "weight": 0.3,
            "dimensions": {"longueur": 90, "largeur": 40, "hauteur": 0.3},
            "is_active": True,
            "category_name": "Electronics", # Assign to Electronics
            "images": [
                {"url": "https://www.grosbill.com/images_produits/4ce8346d-3612-4289-afb0-b8cebdc2ecf9.png", "is_primary": True}
            ]
        },
        {
            "name": "Station de Charge Sans Fil",
            "description": "Chargeur sans fil pour smartphone et écouteurs.",
            "sku": "WIRELESS-CHARGE-022",
            "price": 29.99,
            "cost": 13.00,
            "unit": "pièce",
            "barcode": "2121212121212",
            "weight": 0.11,
            "dimensions": {"longueur": 10, "largeur": 10, "hauteur": 1.2},
            "is_active": True,
            "category_name": "Electronics", # Assign to Electronics
            "images": [
                {"url": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRmEdDnbJF6twsnznkn68to9LCx4JOnXESkMA&s", "is_primary": True}
            ]
        },
        {
            "name": "The Great Novel",
            "description": "A captivating story of adventure and discovery.",
            "sku": "BOOK-GN-001",
            "price": 15.99,
            "cost": 8.00,
            "unit": "piece",
            "barcode": "1000000000001",
            "weight": 0.5,
            "dimensions": {"longueur": 20, "largeur": 14, "hauteur": 2},
            "is_active": True,
            "category_name": "Books",
            "images": [
                {"url": "https://m.media-amazon.com/images/I/71g2+0hC+7L._AC_UF1000,1000_QL80_.jpg", "is_primary": True}
            ]
        },
        {
            "name": "Cookbook for Beginners",
            "description": "Easy recipes for aspiring chefs.",
            "sku": "BOOK-CB-002",
            "price": 22.50,
            "cost": 10.00,
            "unit": "piece",
            "barcode": "1000000000002",
            "weight": 0.8,
            "dimensions": {"longueur": 25, "largeur": 18, "hauteur": 3},
            "is_active": True,
            "category_name": "Books",
            "images": [
                {"url": "https://m.media-amazon.com/images/I/71xG-e-4-eL._AC_UF1000,1000_QL80_.jpg", "is_primary": True}
            ]
        },
        {
            "name": "Science Fiction Anthology",
            "description": "Collection of thrilling sci-fi short stories.",
            "sku": "BOOK-SF-003",
            "price": 19.99,
            "cost": 9.50,
            "unit": "piece",
            "barcode": "1000000000003",
            "weight": 0.6,
            "dimensions": {"longueur": 22, "largeur": 15, "hauteur": 2.5},
            "is_active": True,
            "category_name": "Books",
            "images": [
                {"url": "https://m.media-amazon.com/images/I/81+x4+x+x+xL._AC_UF1000,1000_QL80_.jpg", "is_primary": True}
            ]
        },
        {
            "name": "Coffee Maker",
            "description": "Automatic drip coffee maker with timer.",
            "sku": "HK-CM-001",
            "price": 49.99,
            "cost": 25.00,
            "unit": "piece",
            "barcode": "2000000000001",
            "weight": 2.0,
            "dimensions": {"longueur": 25, "largeur": 20, "hauteur": 30},
            "is_active": True,
            "category_name": "Home & Kitchen",
            "images": [
                {"url": "https://m.media-amazon.com/images/I/71-0-0-0-0L._AC_UF1000,1000_QL80_.jpg", "is_primary": True}
            ]
        },
        {
            "name": "Blender",
            "description": "High-speed blender for smoothies and shakes.",
            "sku": "HK-BL-002",
            "price": 79.99,
            "cost": 40.00,
            "unit": "piece",
            "barcode": "2000000000002",
            "weight": 3.5,
            "dimensions": {"longueur": 18, "largeur": 18, "hauteur": 40},
            "is_active": True,
            "category_name": "Home & Kitchen",
            "images": [
                {"url": "https://m.media-amazon.com/images/I/71-0-0-0-0L._AC_UF1000,1000_QL80_.jpg", "is_primary": True}
            ]
        },
        {
            "name": "Smart Light Bulb",
            "description": "Wi-Fi enabled LED bulb, color changing.",
            "sku": "HK-LB-003",
            "price": 19.99,
            "cost": 9.00,
            "unit": "piece",
            "barcode": "2000000000003",
            "weight": 0.1,
            "dimensions": {"longueur": 6, "largeur": 6, "hauteur": 12},
            "is_active": True,
            "category_name": "Home & Kitchen",
            "images": [
                {"url": "https://m.media-amazon.com/images/I/71-0-0-0-0L._AC_UF1000,1000_QL80_.jpg", "is_primary": True}
            ]
        },
        {
            "name": "Men's Casual T-Shirt",
            "description": "Comfortable cotton t-shirt for everyday wear.",
            "sku": "FASH-MT-001",
            "price": 25.00,
            "cost": 10.00,
            "unit": "piece",
            "barcode": "3000000000001",
            "weight": 0.2,
            "dimensions": {"longueur": 30, "largeur": 25, "hauteur": 2},
            "is_active": True,
            "category_name": "Fashion",
            "images": [
                {"url": "https://m.media-amazon.com/images/I/71-0-0-0-0L._AC_UF1000,1000_QL80_.jpg", "is_primary": True}
            ]
        },
        {
            "name": "Women's Slim Fit Jeans",
            "description": "Stylish and comfortable denim jeans.",
            "sku": "FASH-WJ-002",
            "price": 55.00,
            "cost": 25.00,
            "unit": "piece",
            "barcode": "3000000000002",
            "weight": 0.6,
            "dimensions": {"longueur": 35, "largeur": 28, "hauteur": 3},
            "is_active": True,
            "category_name": "Fashion",
            "images": [
                {"url": "https://m.media-amazon.com/images/I/71-0-0-0-0L._AC_UF1000,1000_QL80_.jpg", "is_primary": True}
            ]
        },
        {
            "name": "Unisex Running Sneakers",
            "description": "Lightweight and breathable athletic shoes.",
            "sku": "FASH-SN-003",
            "price": 75.00,
            "cost": 35.00,
            "unit": "pair",
            "barcode": "3000000000003",
            "weight": 0.8,
            "dimensions": {"longueur": 30, "largeur": 15, "hauteur": 10},
            "is_active": True,
            "category_name": "Fashion",
            "images": [
                {"url": "https://m.media-amazon.com/images/I/71-0-0-0-0L._AC_UF1000,1000_QL80_.jpg", "is_primary": True}
            ]
        },
        {
            "name": "Building Blocks Set",
            "description": "Creative building set for kids, 500 pieces.",
            "sku": "TG-BB-001",
            "price": 30.00,
            "cost": 15.00,
            "unit": "set",
            "barcode": "4000000000001",
            "weight": 1.2,
            "dimensions": {"longueur": 25, "largeur": 20, "hauteur": 10},
            "is_active": True,
            "category_name": "Toys & Games",
            "images": [
                {"url": "https://m.media-amazon.com/images/I/71-0-0-0-0L._AC_UF1000,1000_QL80_.jpg", "is_primary": True}
            ]
        },
        {
            "name": "Family Board Game",
            "description": "Fun strategy game for 2-6 players.",
            "sku": "TG-BG-002",
            "price": 28.00,
            "cost": 12.00,
            "unit": "piece",
            "barcode": "4000000000002",
            "weight": 0.9,
            "dimensions": {"longueur": 28, "largeur": 28, "hauteur": 7},
            "is_active": True,
            "category_name": "Toys & Games",
            "images": [
                {"url": "https://m.media-amazon.com/images/I/71-0-0-0-0L._AC_UF1000,1000_QL80_.jpg", "is_primary": True}
            ]
        },
        {
            "name": "Remote Control Car",
            "description": "High-speed RC car, perfect for outdoor fun.",
            "sku": "TG-RC-003",
            "price": 45.00,
            "cost": 20.00,
            "unit": "piece",
            "barcode": "4000000000003",
            "weight": 0.7,
            "dimensions": {"longueur": 30, "largeur": 15, "hauteur": 10},
            "is_active": True,
            "category_name": "Toys & Games",
            "images": [
                {"url": "https://m.media-amazon.com/images/I/71-0-0-0-0L._AC_UF1000,1000_QL80_.jpg", "is_primary": True}
            ]
        }
        
    ]

    for prod in products:
        # Récupérer la catégorie par son nom
        cat = Category.objects.get(name=prod["category_name"])
        p, created = Product.objects.get_or_create(
            sku=prod["sku"],
            defaults={
                "name": prod["name"],
                "description": prod.get("description", ""),
                "category": cat,
                "price": prod["price"],
                "cost": prod["cost"],
                "unit": prod["unit"],
                "barcode": prod["barcode"],
                "weight": prod["weight"],
                "dimensions": prod["dimensions"],
                "is_active": prod["is_active"],
            }
        )
        if not created:
            # Met à jour les champs et sauvegarde
            p.name = prod["name"]
            p.description = prod.get("description", "")
            p.category = cat
            p.price = prod["price"]
            p.cost = prod["cost"]
            p.unit = prod["unit"]
            p.barcode = prod["barcode"]
            p.weight = prod["weight"]
            p.dimensions = prod["dimensions"]
            p.is_active = True  # <-- Force l'activation du produit
            p.save()
            # Supprime les anciennes images pour ce produit
            ProductImage.objects.filter(product=p).delete()
        # Ajoute les images
        for img in prod["images"]:
            ProductImage.objects.get_or_create(product=p, url=img["url"], is_primary=img["is_primary"])