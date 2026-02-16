from weasyprint import HTML
import io

def generate_invoice_pdf(invoice):
    subtotal = sum(item.line_total for item in invoice.items)
    tax_amount = invoice.total_amount - subtotal
    tax_label = f"{invoice.tax_type} ({invoice.tax_rate}%)"

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
            body {{ font-family: sans-serif; padding: 20px; }}
            table {{ width: 100%; border-collapse: collapse; margin-top: 20px; }}
            th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
            .header {{ margin-bottom: 20px; }}
            .details {{ margin-bottom: 10px; }}
        </style>
    </head>
    <body>
        <div class="header">
            <h1>INVOICE #{invoice.id}</h1>
            <p>Date: {invoice.date}</p>
            <p><strong>Status:</strong> {invoice.status}</p>
        </div>
        
        <div class="details">
            <h3>Bill To:</h3>
            <p>{invoice.customer.name}</p>
            <p>{invoice.customer.email}</p>
        </div>

        <div class="details">
            <p>ARN: {invoice.arn if invoice.arn else 'Pending'}</p>
        </div>
        
        <table>
            <thead>
                <tr>
                    <th>Item</th>
                    <th>Qty</th>
                    <th>Price</th>
                    <th>Total</th>
                </tr>
            </thead>
            <tbody>
                {rows_html} 
            </tbody>
        </table>
        
        <div class="total" style="text-align: left; margin-top: 20px;">
            <p style="margin: 5px 0;">Subtotal: ₹{subtotal}</p>
            <p style="margin: 5px 0; color: #666;">{tax_label}: ₹{round(tax_amount, 2)}</p>
            <h3 style="margin-top: 10px; border-top: 2px solid #333; display: inline-block; padding-top: 5px;">
                TOTAL: ₹{invoice.total_amount}
            </h3>
        </div>
    </body>
    </html>
    """

    pdf_file = io.BytesIO()
    HTML(string=html_content).write_pdf(pdf_file)
    pdf_file.seek(0)
    return pdf_file