import csv
import jinja2
import pdfkit
import os
from datetime import datetime
import shutil

# Setup wkhtmltopdf config
wkhtmltopdf_path = shutil.which('wkhtmltopdf')
if not wkhtmltopdf_path:
    raise FileNotFoundError("wkhtmltopdf binary not found.")
config = pdfkit.configuration(wkhtmltopdf=wkhtmltopdf_path)

# Prepare invoice output folder
os.makedirs('invoices', exist_ok=True)

# Load Jinja2 template
template_loader = jinja2.FileSystemLoader('.')
template_env = jinja2.Environment(loader=template_loader)
template = template_env.get_template('billing.html')

# Process each client from CSV
with open('clients.csv', newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        name = row['name']
        item1, item2, item3 = row['item1'], row['item2'], row['item3']
        subtotal1, subtotal2, subtotal3 = float(row['subtotal1']), float(row['subtotal2']), float(row['subtotal3'])
        total = subtotal1 + subtotal2 + subtotal3
        today_date = datetime.today().strftime("%d %b, %Y")
        month = datetime.today().strftime("%B")

        context = {
            'client_name': name,
            'today_date': today_date,
            'month': month,
            'item1': item1, 'subtotal1': f"${subtotal1:.2f}",
            'item2': item2, 'subtotal2': f"${subtotal2:.2f}",
            'item3': item3, 'subtotal3': f"${subtotal3:.2f}",
            'total': f"${total:.2f}"
        }

        rendered_html = template.render(context)
        pdf_filename = f"invoices/{name.replace(' ', '_')}_invoice.pdf"
        pdfkit.from_string(rendered_html, pdf_filename, configuration=config, css='billing.css')

        print(f"[✓] Invoice created for {name} -> {pdf_filename}")
