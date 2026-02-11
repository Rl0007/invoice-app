# InvoicePro

A simple, full-stack invoice management system built with Flask. This application allows users to manage customers, track inventory items, and generate PDF invoices with automatic GST calculation and ARN integration.

## Features

* **Dashboard:** View and manage all invoices in one place.
* **Customer Management:** Add, edit, and view customer details.
* **Item Inventory:** Manage products and prices for quick invoicing.
* **Invoice Generation:** Create invoices with dynamic item addition and tax calculation.
* **PDF Download:** Instantly generate and download PDF copies of invoices.
* **ARN Integration:** Automatically fetches an Application Reference Number (ARN) from an external API.

## Tech Stack

* **Backend:** Python, Flask, Peewee (SQLite)
* **Frontend:** HTML, TailwindCSS, JavaScript
* **PDF Generation:** WeasyPrint
* **Database:** SQLite

## Installation & Setup

1.  **Clone the repository:**
    ```bash
    git clone <your-github-repo-url>
    cd invoice-app
    ```

2.  **Create a virtual environment:**
    ```bash
    python -m venv venv
    # Windows
    venv\Scripts\activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Set up environment variables:**
    Create a `.env` file in the root directory and add your API credentials:
    ```ini
    API_URL=[https://buildwithhussain.com/api/v2/method/get_arn_number](https://buildwithhussain.com/api/v2/method/get_arn_number)
    API_KEY=2c70587e2df4779
    API_SECRET=56331804ac8ca7b
    ```

5.  **Initialize the Database:**
    Run the seed script to create tables and the default Admin user.
    ```bash
    python seed.py
    ```

6.  **Run the Application:**
    ```bash
    python run.py
    ```
    
## Login Credentials

* **Email:** `admin@example.com`
* **Password:** `password123`

## Project Structure

* `app/models.py` - Database tables (User, Customer, Invoice, Item).
* `app/routes.py` - API logic for creating invoices and handling data.
* `app/einvoice.py` - External API integration for ARN generation.
* `app/templates/` - HTML files for the frontend.
