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
    cat, _ = Category.objects.get_or_create(name="Électronique", defaults={"description": "Appareils électroniques"})
    
    # Exemple de produits à ajouter
    products = [
        {
            "name": "Smartphone X100",
            "description": "Un smartphone performant avec écran OLED.",
            "sku": "X100-001",
            "price": 499.99,
            "cost": 350.00,
            "unit": "pièce",
            "barcode": "1234567890123",
            "weight": 0.18,
            "dimensions": {"longueur": 15, "largeur": 7, "hauteur": 0.8},
            "is_active": True,
            "images": [
                {"url": "https://via.placeholder.com/300x300?text=Smartphone", "is_primary": True}
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
            "images": [
                {"url": "https://via.placeholder.com/300x300?text=Casque", "is_primary": True}
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
            "images": [
                {"url": "https://via.placeholder.com/300x300?text=Montre", "is_primary": True}
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
            "images": [
                {"url": "https://via.placeholder.com/300x300?text=Laptop", "is_primary": True}
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
            "images": [
                {"url": "https://via.placeholder.com/300x300?text=Enceinte", "is_primary": True}
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
            "images": [
                {"url": "https://via.placeholder.com/300x300?text=Tablette", "is_primary": True}
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
            "images": [
                {"url": "https://via.placeholder.com/300x300?text=Chargeur", "is_primary": True}
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
            "images": [
                {"url": "https://via.placeholder.com/300x300?text=Souris", "is_primary": True}
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
            "images": [
                {"url": "https://via.placeholder.com/300x300?text=Clavier", "is_primary": True}
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
            "images": [
                {"url": "https://via.placeholder.com/300x300?text=Webcam", "is_primary": True}
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
            "images": [
                {"url": "https://via.placeholder.com/300x300?text=SSD", "is_primary": True}
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
            "images": [
                {"url": "https://via.placeholder.com/300x300?text=SD+Card", "is_primary": True}
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
            "images": [
                {"url": "https://via.placeholder.com/300x300?text=Ecouteurs", "is_primary": True}
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
            "images": [
                {"url": "https://via.placeholder.com/300x300?text=Powerbank", "is_primary": True}
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
            "images": [
                {"url": "https://via.placeholder.com/300x300?text=Projecteur", "is_primary": True}
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
            "images": [
                {"url": "https://via.placeholder.com/300x300?text=Camera", "is_primary": True}
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
            "images": [
                {"url": "https://via.placeholder.com/300x300?text=Routeur", "is_primary": True}
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
            "images": [
                {"url": "https://via.placeholder.com/300x300?text=Lampe", "is_primary": True}
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
            "images": [
                {"url": "https://via.placeholder.com/300x300?text=Robot", "is_primary": True}
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
            "images": [
                {"url": "https://via.placeholder.com/300x300?text=Imprimante", "is_primary": True}
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
            "images": [
                {"url": "https://via.placeholder.com/300x300?text=Tapis", "is_primary": True}
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
            "images": [
                {"url": "https://via.placeholder.com/300x300?text=Station", "is_primary": True}
            ]
        }
    ]

    for prod in products:
        p, _ = Product.objects.get_or_create(
            sku=prod["sku"],
            defaults={
                "name": prod["name"],
                "description": prod["description"],
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
        for img in prod["images"]:
            ProductImage.objects.get_or_create(product=p, url=img["url"], is_primary=img["is_primary"])
    print("Produits ajoutés avec succès.")

if __name__ == "__main__":
    run()
