from weasyprint import HTML
import io


def generate_invoice_pdf(invoice):

    rows_html = ""
    for item in invoice.items:
        rows_html += f"""
        <tr>
            <td>{item.item_name}</td>
            <td>{item.quantity}</td>
            <td>₹{item.item_price}</td>
            <td>₹{item.line_total}</td>
        </tr>
        """

    html_content = f"""
    <html>
    <head>
        <style>
            table {{ width: 100%; border-collapse: collapse; margin-top: 20px; }}
            th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
        </style>
    </head>
    <body>
        <div class="header">
            <h1>INVOICE #{invoice.id}</h1>
            <p>Date: {invoice.date}</p>
        </div>
        
        <div class="details">
            <h3>Bill To:</h3>
            <p>{invoice.customer.name}</p>
        </div>
        
        <table>
            <thead>
                <tr>
                    <th>Item</th>
                    <th>Qty</th>
                    <th>Price (at purchase)</th>
                    <th>Total</th>
                </tr>
            </thead>
            <tbody>
                {rows_html} </tbody>
        </table>
        
        <div class="total">
            <h3>TOTAL: ₹{invoice.total_amount}</h3>
        </div>
    </body>
    </html>
    """

    pdf_file = io.BytesIO()
    HTML(string=html_content).write_pdf(pdf_file)
    pdf_file.seek(0)
    return pdf_file
