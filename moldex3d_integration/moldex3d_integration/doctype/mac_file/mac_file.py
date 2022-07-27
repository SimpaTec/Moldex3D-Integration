# Copyright (c) 2022, Jide Olayinka and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import now
from moldex3d_integration.app.utils import process_mac_csv,create_folder

class MACFile(Document):
	pass


@frappe.whitelist()
def process_moldex_mac(data):

	doc_dict = {
		'doctype': data,
		'macfile_attached':True
	}
	moldex_pro = frappe.get_doc(doc_dict).insert()	
	moldex_pro.ignore_permissions = True		
	moldex_pro.save()

	doctype_folder = create_folder(_(data), "Home")
	#title_folder = create_folder(title, doctype_folder)

	return moldex_pro.name
	
	


@frappe.whitelist()
def update_moldex_mac(doctype,docname,data_file):
	"""read mac file and update fields"""
	csv_content = process_mac_csv(doctype,docname,data_file)
	#return {"name": invoice_doc.name, "status": invoice_doc.docstatus}
	return csv_content
