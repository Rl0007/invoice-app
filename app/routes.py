from flask import Blueprint, request, jsonify, send_file
from flask_login import login_required
import datetime
from decimal import Decimal 
from app.utils import generate_invoice_pdf
from app.models import Customer, InvoiceItem, Item, Invoice
from app.einvoice import get_arn 

api = Blueprint("api", __name__)

@api.route("/health", methods=["GET"])
def health_check():
    return jsonify({"status": "ok", "message": "Invoice API is running"}), 200

@api.route("/customers", methods=["POST","GET"])
@login_required
def create_customer():
    if request.method == "POST":
        data = request.get_json()
        customer = Customer.create(
            name=data["name"],
            email=data["email"],
            phone=data["phone"],
            address=data.get("address", " "),
        )
        return jsonify({"message": "Customer created", "id": customer.id}), 201
    elif request.method == "GET":
        customers = Customer.select()
        data = [{"id": c.id, "name": c.name, "email": c.email} for c in customers]
        return jsonify(data), 200

@api.route("/items", methods=["GET"])
@login_required
def get_items():
    items = Item.select()
    return (
        jsonify([{"id": i.id, "name": i.name, "price": str(i.price)} for i in items]),
        200,
    )

@api.route("/items", methods=["POST"])
@login_required
def create_item():
    data = request.get_json()
    if not data.get("name") or not data.get("price"):
        return jsonify({"error": "Name and Price are required"}), 400

    item = Item.create(name=data["name"], price=data["price"])
    return jsonify({"id": item.id, "message": "Item created"}), 201


@api.route("/invoices", methods=["POST"])
@login_required
def create_invoice():
    data = request.get_json()
    customer = Customer.get_by_id(data["customer_id"])
    
    tax_type = data.get("tax_type", "GST")
    tax_rate = Decimal(str(data.get("tax_rate", 0)))

    invoice = Invoice.create(
        customer=customer, 
        date=datetime.date.today(),
        tax_type=tax_type,
        tax_rate=tax_rate,
        total_amount=0 
    )

    subtotal = Decimal(0) 

    for entry in data["items"]:
        item = Item.get_by_id(entry["item_id"])
        qty = int(entry["quantity"])
        
        line_total = item.price * qty

        InvoiceItem.create(
            invoice=invoice,
            item_name=item.name,    
            item_price=item.price,
            quantity=qty,
            line_total=line_total
        )
        subtotal += line_total

    tax_amount = subtotal * (tax_rate / Decimal(100))
    grand_total = subtotal + tax_amount
    
    invoice.total_amount = grand_total
    invoice.save() 
    
    new_arn = get_arn(invoice.id, "Admin")
    
    if new_arn:
        invoice.arn = new_arn
        invoice.save()

    return jsonify({
        "invoice_id": invoice.id,
        "message": "Invoice created successfully",
        "total": str(grand_total),
        "arn": invoice.arn
    }), 201


@api.route("/invoices/<int:id>/pdf", methods=["GET"])
@login_required
def download_invoice_pdf(id):
    invoice = Invoice.get_by_id(id)
    pdf_output = generate_invoice_pdf(invoice)

    return send_file(
        pdf_output,
        mimetype="application/pdf",
        as_attachment=True,
        download_name=f"invoice_{id}.pdf",
    )