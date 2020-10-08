import os
import codecs
import yaml
import locale
import argparse
from pybars import Compiler
from weasyprint import HTML


def create_and_save_doc(document_data, index_html, output_pdf):
    """
    Creates a PDF invoice by filling an HTML template with a YML file.

    Parameters
    ----------
    document_data : dict
        Data to use for filling the HTML template.
    index_html : str
        Absolute path to html template file.
    output_pdf : str
        Name of the output PDF file.

    Returns
    -------
    Saves the output PDF to output/ directory
    """
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
        pos['total_tax'] = \
            pos['total_net_price'] * (pos['tax_rate'] / float(100))
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

        weasytemplate = HTML(string=html_text)
        weasytemplate.write_pdf(os.path.join('/app', 'output', output_pdf))
    return


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate PDF invoice from HTML'
                                                 ' template using a yaml file.')
    parser.add_argument('--template', help='The directory name of the HTML '
                                           'template to use (e.g. template_1).',
                        default="template")
    parser.add_argument('--yaml_file', help='The name of the yaml file in the '
                                            'invoice directory.', default=None)
    parser.add_argument('--output_pdf', help='The name of the output PDF',
                        default="output.pdf")
    parser.add_argument('--locale', help='The locale to use', default="")

    args = parser.parse_args()
    locale.setlocale(locale.LC_ALL, args.locale)

    document_url = os.path.join('/app', 'documents', 'invoice')
    base_url = os.path.join(document_url, args.template)
    index_html = os.path.join(base_url, 'index.html')

    with open(os.path.join(document_url, args.yaml_file)) as yml_file:
        document_data = yaml.load(yml_file)

    create_and_save_doc(document_data, index_html, args.output_pdf)
