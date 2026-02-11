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
   all_customers = Customer.select()
   return render_template('customers.html', customers=all_customers)

@views.route('/invoices')
@login_required
def invoices_page():
    all_invoices = Invoice.select().join(Customer)
    return render_template('invoices.html', invoices=all_invoices)

@views.route('/invoices/new')
@login_required
def new_invoice_page():
    customers = Customer.select()
    items = Item.select()
    return render_template('create_invoice.html', customers=customers, items=items)

@views.route('/items')
@login_required
def items_page():
    items = Item.select()
    return render_template('items.html', items=items)

