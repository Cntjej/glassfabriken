"""
erp.py - Affärslogik för Glassfabrikens ERP-system
Innehåller klasserna Customer, Product, Order och ERPSystem.
"""

import csv
import json
import os
from datetime import datetime


# ─────────────────────────────────────────────
#  Dataklasser
# ─────────────────────────────────────────────

class Customer:
    """Representerar en kund med rabatt."""

    def __init__(self, customer_id, name, address, discount_pct):
        self.customer_id = customer_id
        self.name = name
        self.address = address
        self.discount_pct = float(discount_pct)

    def to_dict(self):
        return {
            "customer_id": self.customer_id,
            "name": self.name,
            "address": self.address,
            "discount_pct": self.discount_pct,
        }

    def __str__(self):
        return f"{self.customer_id} – {self.name} ({self.address}) [{self.discount_pct}% rabatt]"


class Product:
    """Representerar en produkt i lagret."""

    def __init__(self, sku, name, stock, price):
        self.sku = sku
        self.name = name
        self.stock = int(stock)
        self.price = float(price)

    def to_dict(self):
        return {
            "sku": self.sku,
            "name": self.name,
            "stock": self.stock,
            "price": self.price,
        }

    def __str__(self):
        return f"{self.sku} – {self.name}  Lager: {self.stock}  Pris: {self.price} kr"


class Order:
    """Representerar en bekräftad beställning."""

    def __init__(self, order_id, customer, lines):
        self.order_id = order_id
        self.customer = customer
        # lines: [{"product": Product, "qty": int, "unit_price": float, "line_total": float}]
        self.lines = lines
        self.created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def subtotal(self):
        return sum(l["line_total"] for l in self.lines)

    def discount_amount(self):
        return self.subtotal() * (self.customer.discount_pct / 100)

    def total(self):
        return self.subtotal() - self.discount_amount()

    def to_dict(self):
        return {
            "order_id": self.order_id,
            "customer_id": self.customer.customer_id,
            "customer_name": self.customer.name,
            "customer_address": self.customer.address,
            "created_at": self.created_at,
            "lines": [
                {
                    "sku": l["product"].sku,
                    "name": l["product"].name,
                    "qty": l["qty"],
                    "unit_price": l["unit_price"],
                    "line_total": l["line_total"],
                }
                for l in self.lines
            ],
            "discount_pct": self.customer.discount_pct,
            "discount_amount": round(self.discount_amount(), 2),
            "total": round(self.total(), 2),
        }


# ─────────────────────────────────────────────
#  Huvudklass – hanterar all data och logik
# ─────────────────────────────────────────────

class ERPSystem:
    """
    Hjärtat i systemet.
    Läser in kunder/produkter vid start och erbjuder metoder
    för att lägga ordrar, lägga till kunder/produkter m.m.
    """

    def __init__(
        self,
        customers_file="data/customers.csv",
        products_file="data/products.csv",
        orders_file="data/orders.json",
    ):
        self.customers_file = customers_file
        self.products_file = products_file
        self.orders_file = orders_file

        self.customers: dict[str, Customer] = {}
        self.products: dict[str, Product] = {}

        # Ladda filer vid uppstart
        self.load_customers()
        self.load_products()

    # ── Inläsning ──────────────────────────────

    def load_customers(self):
        """Läs customers.csv och fyll self.customers."""
        self.customers = {}
        if not os.path.exists(self.customers_file):
            return
        with open(self.customers_file, newline="", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                c = Customer(row["customer_id"], row["name"], row["address"], row["discount_pct"])
                self.customers[c.customer_id] = c

    def load_products(self):
        """Läs products.csv och fyll self.products."""
        self.products = {}
        if not os.path.exists(self.products_file):
            return
        with open(self.products_file, newline="", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                p = Product(row["sku"], row["name"], row["antal_i_lager"], row["price_sek"])
                self.products[p.sku] = p

    # ── Sparning ───────────────────────────────

    def save_customers(self):
        """Skriv hela kundlistan till CSV."""
        os.makedirs(os.path.dirname(self.customers_file), exist_ok=True)
        with open(self.customers_file, "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(["customer_id", "name", "address", "discount_pct"])
            for c in self.customers.values():
                w.writerow([c.customer_id, c.name, c.address, c.discount_pct])

    def save_products(self):
        """Skriv hela produktlistan till CSV."""
        os.makedirs(os.path.dirname(self.products_file), exist_ok=True)
        with open(self.products_file, "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(["sku", "name", "antal_i_lager", "price_sek"])
            for p in self.products.values():
                w.writerow([p.sku, p.name, p.stock, p.price])

    def _append_order(self, order_dict):
        """Lägg till en order i orders.json."""
        os.makedirs(os.path.dirname(self.orders_file), exist_ok=True)
        try:
            with open(self.orders_file, encoding="utf-8") as f:
                data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            data = []
        data.append(order_dict)
        with open(self.orders_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    # ── Hjälpmetoder ──────────────────────────

    def find_customer(self, identifier: str):
        """Hitta kund via ID eller namn (skiftlägesokänsligt)."""
        if identifier in self.customers:
            return self.customers[identifier]
        lo = identifier.lower()
        for c in self.customers.values():
            if c.name.lower() == lo:
                return c
        return None

    def find_product(self, identifier: str):
        """Hitta produkt via SKU eller namn (skiftlägesokänsligt)."""
        if identifier in self.products:
            return self.products[identifier]
        lo = identifier.lower()
        for p in self.products.values():
            if p.name.lower() == lo:
                return p
        return None

    def generate_order_id(self) -> str:
        """Generera nästa order-ID, t.ex. O-2026-0003."""
        year = datetime.now().year
        prefix = f"O-{year}-"
        max_num = 0
        for o in self.get_order_history():
            oid = o.get("order_id", "")
            if oid.startswith(prefix):
                try:
                    max_num = max(max_num, int(oid[len(prefix):]))
                except ValueError:
                    pass
        return f"{prefix}{max_num + 1:04d}"

    # ── Beställning ───────────────────────────

    def place_order(self, customer_identifier: str, order_lines: list):
        """
        Lägg en beställning.

        order_lines: [{"sku": "10001", "qty": 5}, ...]

        Returnerar (Order, None) vid lyckat resultat
               eller (None, felmeddelande) vid fel.
        """
        # Validera kund
        customer = self.find_customer(customer_identifier)
        if not customer:
            return None, f"Kund '{customer_identifier}' hittades inte."

        resolved = []
        for line in order_lines:
            product = self.find_product(str(line["sku"]))
            if not product:
                return None, f"Produkt '{line['sku']}' hittades inte."

            qty = int(line["qty"])
            if qty <= 0:
                return None, f"Antal måste vara > 0 för produkt '{line['sku']}'."

            if product.stock < qty:
                return None, (
                    f"Otillräckligt lagersaldo för '{product.name}'. "
                    f"Begärt: {qty}, Finns: {product.stock}."
                )

            resolved.append({
                "product": product,
                "qty": qty,
                "unit_price": product.price,
                "line_total": product.price * qty,
            })

        # Allt validerat – dra av lagersaldo och skapa order
        order_id = self.generate_order_id()
        for line in resolved:
            line["product"].stock -= line["qty"]

        order = Order(order_id, customer, resolved)
        self.save_products()
        self._append_order(order.to_dict())
        return order, None

    # ── Lägga till kunder/produkter (VG) ──────

    def add_customer(self, customer_id, name, address, discount_pct):
        """Lägg till ny kund och spara till fil."""
        if customer_id in self.customers:
            return False, f"Kund-ID '{customer_id}' finns redan."
        c = Customer(customer_id, name, address, float(discount_pct))
        self.customers[customer_id] = c
        self.save_customers()
        return True, c

    def add_product(self, sku, name, stock, price):
        """Lägg till ny produkt och spara till fil."""
        if sku in self.products:
            return False, f"SKU '{sku}' finns redan."
        p = Product(sku, name, int(stock), float(price))
        self.products[sku] = p
        self.save_products()
        return True, p

    # ── Orderhistorik ─────────────────────────

    def get_order_history(self) -> list:
        """Returnera alla sparade ordrar som lista av dict."""
        try:
            with open(self.orders_file, encoding="utf-8") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    # ── Batch-beställning från fil ────────────

    def process_orders_from_file(self, filepath: str) -> list:
        """
        Bearbeta en JSON-fil med flera ordrar.
        Returnerar lista med resultat per order.
        """
        with open(filepath, encoding="utf-8") as f:
            entries = json.load(f)

        results = []
        for entry in entries:
            order, error = self.place_order(
                entry.get("customer_id", ""),
                entry.get("lines", []),
            )
            if error:
                results.append({"success": False, "error": error, "input": entry})
            else:
                results.append({
                    "success": True,
                    "order_id": order.order_id,
                    "total": order.total(),
                })
        return results
