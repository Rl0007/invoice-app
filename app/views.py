from app.models import Customer, Invoice ,Item
from flask import Blueprint, render_template ,redirect
from flask_login import login_required, current_user
from app.models import Customer
from app.models import Item

views = Blueprint('views', __name__)

@views.route('/')
def home():
    if current_user.is_authenticated:
        return redirect('/customers')
    return render_template('landing.html')

@views.route('/login')
def login_page():
    return render_template('login.html')

@views.route('/customers')
@login_required
def customers_page():
   all_customers = Customer.select().order_by(Customer.id.desc())
   return render_template('customers.html', customers=all_customers)

@views.route('/invoices')
@login_required
def invoices_page():
    all_invoices = Invoice.select().join(Customer).order_by(Invoice.id.desc())
    return render_template('invoices.html', invoices=all_invoices)

@views.route('/invoices/new')
@login_required
def new_invoice_page():
    customers = Customer.select().order_by(Customer.id.desc())
    items = Item.select().order_by(Item.id.desc())
    return render_template('create_invoice.html', customers=customers, items=items)

@views.route('/items')
@login_required
def items_page():
    items = Item.select().order_by(Item.id.desc())
    return render_template('items.html', items=items)

@views.route('/customers/<int:id>/edit')
@login_required
def edit_customer_page(id):
    customer = Customer.get_by_id(id)
    return render_template('edit_customer.html', customer=customer)

@views.route('/items/<int:id>/edit')
@login_required
def edit_item_page(id):
    item = Item.get_by_id(id)
    return render_template('edit_item.html', item=item)