# Copyright (c) 2022, Jide Olayinka and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import now, cint
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


@frappe.whitelist()
def upload_attach_macfile():
	user: "User" = frappe.get_doc("User", frappe.session.user)
	ignore_permissions = False

	files = frappe.request.files
	is_private = frappe.form_dict.is_private
	doctype = frappe.form_dict.doctype
	docname = frappe.form_dict.docname
	fieldname = frappe.form_dict.fieldname
	file_url = frappe.form_dict.file_url
	folder = frappe.form_dict.folder or "Home"
	filename = frappe.form_dict.file_name
	content = None

	if "file" in files:
		file = files["file"]
		content = file.stream.read()
		filename = file.filename

	frappe.local.uploaded_file = content
	frappe.local.uploaded_filename = filename

	mac_file = frappe.get_doc(
		{
			"doctype": "File",
			"attached_to_doctype": doctype,
			"attached_to_name": docname,
			"attached_to_field": fieldname,
			"folder": folder,
			"file_name": filename,
			"file_url": file_url,
			"is_private": cint(is_private),
			"content": content,
		}
	).save(ignore_permissions=ignore_permissions)

	return update_moldex_mac(doctype,docname,mac_file.file_url)