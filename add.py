import os

BASE_DIR = os.path.join(os.path.dirname(__file__), "src", "pages", "seller")
os.makedirs(BASE_DIR, exist_ok=True)

pages = [
    "SellerProfilePage",
    "SellerProductsPage",
    "SellerProductCreatePage",
    "SellerProductDetailPage",
    "SellerProductUpdatePage",
    "SellerOrdersPage",
    "SellerAnalyticsPage",
]

# Use double braces for curly braces, and replace {name} and {title} only
template = (
    "import React from 'react';\n\n"
    "const {name}: React.FC = () => {{\n"
    "  return (\n"
    "    <div className=\"container-custom py-8\">\n"
    "      <h1 className=\"text-2xl font-bold mb-4\">{title}</h1>\n"
    "      {/* TODO: Implement {name} */}\n"
    "    </div>\n"
    "  );\n"
    "}};\n\n"
    "export default {name};\n"
)

for page in pages:
    filename = os.path.join(BASE_DIR, f"{page}.tsx")
    if not os.path.exists(filename):
        content = template.replace("{name}", page).replace("{title}", page.replace("Seller", "Seller "))
        with open(filename, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Created {filename}")
    else:
        print(f"Skipped {filename} (already exists)")
