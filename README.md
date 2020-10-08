## This is a fork of https://github.com/ecmonline/invoice-generator

## Overview
Generate invoices using Python, Weasyprint and YAML. We populate HTML invoice
templates with data from a YAML file.

## Usage 
See `./buildpdf.py --help`:

## HTML Template Format
The HTML templates and their corresponding stylesheet(s) define how the invoice
document looks and feels. The program supports the following data bindings in
the HTML template:

Standalone:
- `{{from.name}}`
- `{{from.street}}`
- `{{from.postcode}}`
- `{{from.city}} `
- `{{to.name}}`
- `{{to.street}}`
- `{{to.postcode}} `
- `{{to.city}}`
- `{{@root.currency}} `
- `{{tax_rate}}`
- `{{total_net_price}}`
- `{{totals.net}}`
- `{{totals.tax}}`
- `{{totals.gross}}`

Contained within `{{#positions}} {{/positions}}`  iterator:
- `{{pos_number}} `
- `{{{text}}}` 
- `{{amount}}`
- `{{net_price}} `
   
## YML Format
We populate our HTML files with YML files. The format of the YML files is as 
follows:
```
from:
    name: str
    street: str
    postcode: str
    city: str

to:
    name: str
    street: str
    postcode: str
    city: str

customer_number: str
currency: float
tax_rate: float
invoice:
    number: str
    date: mm.dd.yyy
    pay_until_date: mm.dd.yyy

positions:
    - net_price: float
      amount: int
      text: str
     
    - ...
    
    - ...
```
    
## Credits
- Template 1: `https://github.com/jonathantneal/html5-invoice`
- Template 2: `https://github.com/sendwithus/templates/`
- Template 3: `https://github.com/rimiti/html-invoice-template`
- Template 4: `https://github.com/Inambe/html-invoice-template`