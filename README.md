## This is a fork of https://github.com/ecmonline/invoice-generator

Generate invoices using python, weasyprint and yaml.
Just add your data to `documents/invoice/data.yml` and run the `./buildpdf.py` script.

Usage see `./buildpdf.py --help`:


    usage: buildpdf.py [-h] [--template TEMPLATE] [--yaml_file YAML_FILE]
                    [--output_pdf OUTPUT_PDF] [--locale LOCALE]

    Convert HTML template to pdf with data from yaml

    optional arguments:
    -h, --help            show this help message and exit
    --template TEMPLATE   The name of the template to use (e.g. invoice)
    --yaml_file YAML_FILE
                            The yaml file to use for data
    --output_pdf OUTPUT_PDF
                            The output pdf file
    --locale LOCALE       The locale to use
    
    
## Credits
- Template 1: `https://github.com/jonathantneal/html5-invoice`
- Template 2: `https://github.com/sendwithus/templates/`
- Template 3: `https://github.com/rimiti/html-invoice-template`
- Template 4: `https://github.com/Inambe/html-invoice-template`