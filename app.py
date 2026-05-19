"""
app.py - Flask-webbserver för Glassfabrikens ERP
Kör: python app.py
Öppna sedan webbläsaren på: http://localhost:5000
"""

from flask import Flask, render_template, request, jsonify
from erp import ERPSystem

app = Flask(__name__)

# ERP-systemet skapas EN gång när servern startar
erp = ERPSystem(
    customers_file="data/customers.csv",
    products_file="data/products.csv",
    orders_file="data/orders.json",
)


# ─────────────────────────────────────────────
#  Sidor
# ─────────────────────────────────────────────

@app.route("/")
def index():
    """Startsida – serverar index.html från templates/"""
    return render_template("index.html")


# ─────────────────────────────────────────────
#  API – Kunder
# ─────────────────────────────────────────────

@app.route("/api/customers", methods=["GET"])
def get_customers():
    """Returnera alla kunder som JSON."""
    return jsonify([c.to_dict() for c in erp.customers.values()])


@app.route("/api/customers", methods=["POST"])
def add_customer():
    """Lägg till en ny kund. Skicka JSON: {customer_id, name, address, discount_pct}"""
    data = request.get_json()
    ok, result = erp.add_customer(
        data.get("customer_id", "").strip(),
        data.get("name", "").strip(),
        data.get("address", "").strip(),
        data.get("discount_pct", 0),
    )
    if ok:
        return jsonify(result.to_dict()), 201
    return jsonify({"error": result}), 400


# ─────────────────────────────────────────────
#  API – Produkter
# ─────────────────────────────────────────────

@app.route("/api/products", methods=["GET"])
def get_products():
    """Returnera alla produkter som JSON."""
    return jsonify([p.to_dict() for p in erp.products.values()])


@app.route("/api/products", methods=["POST"])
def add_product():
    """Lägg till en ny produkt. Skicka JSON: {sku, name, stock, price}"""
    data = request.get_json()
    ok, result = erp.add_product(
        data.get("sku", "").strip(),
        data.get("name", "").strip(),
        data.get("stock", 0),
        data.get("price", 0),
    )
    if ok:
        return jsonify(result.to_dict()), 201
    return jsonify({"error": result}), 400


# ─────────────────────────────────────────────
#  API – Ordrar
# ─────────────────────────────────────────────

@app.route("/api/orders", methods=["GET"])
def get_orders():
    """Returnera orderhistorik som JSON."""
    return jsonify(erp.get_order_history())


@app.route("/api/orders", methods=["POST"])
def place_order():
    """
    Lägg en ny order.
    Skicka JSON: {"customer": "C1001", "lines": [{"sku": "10001", "qty": 5}]}
    """
    data = request.get_json()
    order, error = erp.place_order(
        data.get("customer", ""),
        data.get("lines", []),
    )
    if error:
        return jsonify({"error": error}), 400
    return jsonify(order.to_dict()), 201


# ─────────────────────────────────────────────
#  API – Dashboard-statistik
# ─────────────────────────────────────────────

@app.route("/api/stats", methods=["GET"])
def get_stats():
    """Räkna ihop snabb statistik för dashboarden."""
    orders = erp.get_order_history()
    total_revenue = sum(o.get("total", 0) for o in orders)
    return jsonify({
        "num_customers": len(erp.customers),
        "num_products": len(erp.products),
        "num_orders": len(orders),
        "total_revenue": round(total_revenue, 2),
    })


if __name__ == "__main__":
    print("=" * 50)
    print("  Glassfabriken ERP startar...")
    print("  Öppna: http://localhost:5000")
    print("=" * 50)
    app.run(debug=True)
