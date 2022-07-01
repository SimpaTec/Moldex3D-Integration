
import frappe

from frappe import _
from frappe import publish_progress
from frappe.core.doctype.file.file import create_new_folder
from frappe.utils.file_manager import save_file

import io
import csv
import random



@frappe.whitelist()
def attach_csv(doc, event=None):
    #settings = frappe.get_single("PDF on Submit Settings")
    #enabled = [row.document_type for row in settings.enabled_for]

    """ if doc.doctype not in enabled:
        return """

    fallback_language = frappe.db.get_single_value("System Settings", "language") or "en"
    """ args = {
        "doctype": doc.doctype,
        "name": doc.name,
        "title": doc.get_title(),
        "lang": getattr(doc, "language", fallback_language),
        "show_progress": not settings.create_pdf_in_background
    } """
    args = {
        "doctype": doc.doctype,
        "name": doc.name,
        "title": doc.customer
    }

    """ if settings.create_pdf_in_background:
        enqueue(args)
    else:
        execute(**args) """
    execute(**args)


def enqueue(args):
    """Add method `execute` with given args to the queue."""
    frappe.enqueue(method=execute, queue='long',
                   timeout=30, is_async=True, **args)


def execute(doctype, name, title, content, lang=None, show_progress=False):
    """
    Queue calls this method, when it's ready.
    1. Create necessary folders
    2. Get raw PDF data
    3. Save PDF file and attach it to the document
    show_progress=True # restore to true
    """
    progress = frappe._dict(title=_("processing csv ..."), percent=0, doctype=doctype, docname=name)

    if lang:
        frappe.local.lang = lang

    if show_progress:
        publish_progress(**progress)

    #Home/Mac Moldex
    doctype_folder = create_folder(_(doctype), "Home")
    #title_folder = create_folder(title, doctype_folder)

    if show_progress:
        progress.percent = 33
        publish_progress(**progress)

    #pdf_data = get_pdf_data(doctype, name)
    #csv_data = get_csv_data(doctype, name)

    if show_progress:
        progress.percent = 66
        publish_progress(**progress)

    save_and_attach(content, doctype, name, doctype_folder)

    if show_progress:
        progress.percent = 100
        publish_progress(**progress)


def create_folder(folder, parent):
    """Make sure the folder exists and return it's name."""
    #Home/Mac Moldex
    new_folder_name = "/".join([parent, folder])
    
    if not frappe.db.exists("File", new_folder_name):
        create_new_folder(folder, parent)
    
    return new_folder_name


def get_pdf_data(doctype, name):
    """Document -> HTML -> PDF."""
    html = frappe.get_print(doctype, name)
    return frappe.utils.pdf.get_pdf(html)

def get_csv_data(doctype, name):

    file = open("bizerp.dev/public/files/people.csv")
    csvreader = csv.reader(file)
    header = next(csvreader)
    rows = []
    rows.append(header)
    for row in csvreader:
        rows.append(row)
    #print(f'\n\n\n\n to-time: f.name : {rows}  \n\n\n\n')
    return rows


def save_and_attach(content, to_doctype, to_name, folder):
    """
    Save content to disk and create a File document.
    File document is linked to another document.
    """
    #file_name = "{}.pdf".format(to_name.replace(" ", "-").replace("/", "-"))
    file_name = "{}.csv".format(to_name.replace(" ", "-").replace("/", "-"))
    save_file(file_name, content, to_doctype,
              to_name, folder=folder, is_private=1)

@frappe.whitelist()
def pension_remit(company=None, from_date=None, to_date=None):
    
    output = io.StringIO() #added
    records=20
    fieldnames=['id','name','age','city']    
    swriter = csv.DictWriter(open("bizerp.dev/public/files/people.csv", "w"), fieldnames=fieldnames)
    #writer = csv.DictWriter(output, fieldnames=fieldnames)
    names=['Deepak', 'Sangeeta', 'Geetika', 'Anubhav', 'Sahil', 'Akshay']
    cities=['Delhi', 'Kolkata', 'Chennai', 'Mumbai']
    swriter.writerow(dict(zip(fieldnames, fieldnames)))
    for i in range(0, records):
        swriter.writerow(dict([
            ('id', i),
            ('name', random.choice(names)),
            ('age', str(random.randint(24,26))),
            ('city', random.choice(cities))]))
    csv_output = output.getvalue().encode('utf-8')
    
    print(f'\n\n\n\n to time is: {csv_output} \n\n\n\n')
