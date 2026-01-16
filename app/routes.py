from flask import send_file
from app.utils import generate_invoice_pdf

from flask import Blueprint, request, jsonify
from app.models import Customer, InvoiceItem
from flask_login import login_required

from app.models import Item, Invoice, Customer
import datetime
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
            address=data.get("address", ""),
        )
    elif request.method == "GET":
        customers = Customer.select()
        data = [{"id": c.id, "name": c.name, "email": c.email} for c in customers]
        return jsonify(data), 200



# @api.route("/customers", methods=["GET"])
# @login_required
# def get_customers():
#     customers = Customer.select()
#     data = [{"id": c.id, "name": c.name, "email": c.email} for c in customers]
#     return jsonify(data), 200


# for item product



@api.route("/items/:id", methods=["GET"])
@login_required
def get_items(id):
    if id:
       
        return items.select(id = id)
         
        
    else:
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
    invoice = Invoice.create(customer=customer, date=datetime.date.today())

    total = 0
    item_list = []

    for entry in data["items"]:
        item = Item.get_by_id(entry["item_id"])
        qty = entry["quantity"]
        line_total = item.price * qty

        InvoiceItem.create(
                invoice=invoice,
                item_name=item.name,   
                item_price=item.price,
                quantity=qty,
                line_total=line_total
            )
        
        total += line_total
        item_list.append(
            {
                "name": item.name,
                "qty": qty,
                "price": str(item.price),
                "line_total": str(line_total),
            }
        )

    invoice.total_amount = total
    invoice.save()

    return (
        jsonify(
            {
                "invoice_id": invoice.id,
                "customer": customer.name,
                "items": item_list,
                "total_amount": str(total),
                "message": "Invoice created successfully",
            }
        ),
        201,
    )


# pdf


@api.route("/invoices/<int:id>/pdf", methods=["GET"])
# @login_required
def download_invoice_pdf(id):

    invoice = Invoice.get_by_id(id)
    pdf_output = generate_invoice_pdf(invoice)

    return send_file(
        pdf_output,
        mimetype="application/pdf",
        as_attachment=True,
        download_name=f"invoice_{id}.pdf",
    )
