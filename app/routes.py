from flask import Blueprint, request, jsonify
from app.models import Customer
from flask_login import login_required

api = Blueprint('api', __name__)

@api.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'ok', 'message': 'Invoice API is running'}), 200

@api.route('/customers', methods=['POST'])
@login_required
def create_customer():
    data = request.get_json()
    try:
        customer = Customer.create(
            name=data['name'],
            email=data['email'],
            phone=data['phone'],
            address=data.get('address', '')
        )
        return jsonify({'id': customer.id, 'message': 'Customer created'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@api.route('/customers', methods=['GET'])
@login_required
def get_customers():
    customers = Customer.select()
    data = [{'id': c.id, 'name': c.name, 'email': c.email} for c in customers]
    return jsonify(data), 200

# for item product

from app.models import Item, Invoice, Customer
import datetime

@api.route('/items', methods=['GET'])
@login_required
def get_items():
    items = Item.select()
    return jsonify([{'id': i.id, 'name': i.name, 'price': str(i.price)} for i in items]), 200

@api.route('/items', methods=['POST'])
@login_required
def create_item():
    data = request.get_json()
    if not data.get('name') or not data.get('price'):
        return jsonify({'error': 'Name and Price are required'}), 400
    
    item = Item.create(name=data['name'], price=data['price'])
    return jsonify({'id': item.id, 'message': 'Item created'}), 201

@api.route('/invoices', methods=['POST'])
@login_required
def create_invoice():
    data = request.get_json()

    try:
        customer = Customer.get_by_id(data['customer_id'])
        
        invoice = Invoice.create(customer=customer, date=datetime.date.today())
                
        total = 0
        item_list = []
        
        for entry in data['items']:
            item = Item.get_by_id(entry['item_id'])
            qty = entry['quantity']
            line_total = item.price * qty
            total += line_total
            item_list.append({
                'name': item.name,
                'qty': qty,
                'price': str(item.price),
                'line_total': str(line_total)
            })

        invoice.total_amount = total
        invoice.save()

        return jsonify({
            'invoice_id': invoice.id,
            'customer': customer.name,
            'items': item_list,
            'total_amount': str(total),
            'message': 'Invoice created successfully'
        }), 201

    except Customer.DoesNotExist:
        return jsonify({'error': 'Customer not found'}), 404
    except Item.DoesNotExist:
        return jsonify({'error': 'One of the items does not exist'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500