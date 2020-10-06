#!/usr/bin/env python2

import sys
import codecs
import yaml
import locale
import argparse

from pybars import Compiler
from weasyprint import HTML

parser = argparse.ArgumentParser(description='Convert HTML template to pdf with data from yaml')
parser.add_argument('--template', help='The name of the template to use (e.g. invoice)', default="invoice")
parser.add_argument('--yaml_file', help='The yaml file to use for data', default=None, type=argparse.FileType('r'))
parser.add_argument('--output_pdf', help='The output pdf file', default="pdf.pdf",  type=argparse.FileType('wb'))
parser.add_argument('--locale', help='The locale to use', default="")

args = parser.parse_args()
locale.setlocale(locale.LC_ALL, args.locale)

document_url = 'documents/'+args.template
base_url = document_url+'/template'
index_html = base_url+'/index.html'

if args.yaml_file:
    yml_file = args.yaml_file
else:
    yml_file = codecs.open(document_url+'/data.yml', encoding="utf-8")

document_data = yaml.load(yml_file)

pos_number = 1
document_data['totals'] = {
    'net': 0,
    'gross': 0,
    'tax': 0        
}
for pos in document_data['positions']:
    if not 'tax_rate' in pos:
        pos['tax_rate'] = document_data['tax_rate']

    pos['pos_number'] = pos_number
    pos['total_net_price'] = pos['net_price'] * pos['amount']
    pos['total_tax'] = pos['total_net_price'] * (pos['tax_rate'] / float(100))
    pos['total_gross_price'] = pos['total_net_price'] + pos['total_tax']

    document_data['totals']['net'] += pos['total_net_price']
    document_data['totals']['gross'] += pos['total_gross_price']
    document_data['totals']['tax'] += pos['total_tax']

    pos['amount'] = locale.format_string("%.2f", pos['amount'])
    pos['tax_rate'] = locale.format_string("%.2f", pos['tax_rate'])
    pos['net_price'] = locale.format_string("%.2f", pos['net_price'])
    pos['total_net_price'] = \
        locale.format_string("%.2f", pos['total_net_price'])
    pos['text'] = pos['text'].replace('\n', '<br>')

    pos_number += 1

document_data['totals']['net'] = \
    locale.format_string("%.2f", document_data['totals']['net'])
document_data['totals']['gross'] = \
    locale.format_string("%.2f", document_data['totals']['gross'])
document_data['totals']['tax'] = \
    locale.format_string("%.2f", document_data['totals']['tax'])

with codecs.open(index_html, encoding="utf-8") as index_file:
    html_text = index_file.read()
    
    compiler = Compiler()
    template = compiler.compile(html_text)

    html_text = template(document_data)

    weasytemplate = HTML(string=html_text, base_url=base_url)
    weasytemplate.write_pdf(args.output_pdf)

