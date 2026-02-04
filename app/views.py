from app.models import Customer, Invoice
from flask import Blueprint, render_template
from flask_login import login_required, current_user
from app.models import Customer

views = Blueprint('views', __name__)

@views.route('/')
def home():
    if current_user.is_authenticated:
        return render_template('base.html')
    return render_template('login.html')

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