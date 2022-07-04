
from __future__ import unicode_literals
from datetime import date
from operator import le
import frappe
from frappe import _
import io
import csv
import random
import six
from six import StringIO, text_type, string_types
from frappe.utils import encode, cstr, cint, flt
from frappe.core.doctype.file.file import create_new_folder
from frappe.utils import get_datetime
#from .attach_csv import execute


@frappe.whitelist()
def process_mac_csv(doctype,docname,data_file):
    
    title = []
    mac_title = {
			'doctype': doctype,
			'docname': docname,
		}
    mac_moldex_table = {
    }
    #'date':'Date',
    title_mac ={
        'title':'Title' ,
        'version':'Version' ,
        'software':'Software',
        'copyright':'Copyright(c)',
        'tel':'TEL',
        'fax':'FAX',
        'website':'Website',
        'email':'Email',
        'customer_id':'Customer ID' ,
        'customer':'Customer',
        'customer_class':'Customer Class',
        'license_mode':'License Mode',
        'publishing_date':'Publishing Date',        
        'machine_id':'Machine ID',        
    }
    version_mac = {
        'major':'Major',
        'minor':'Minor',
        'license_mode_ver':'LicenseMode',
        'trial_license':'TrialLicense',
    }
    moldex3d_start_index = 0 #[Moldex3D]
    moldex3d_end_index = 0 #[Moldex3D Mesh]

    writer = UnicodeWriter()
    
    file_path = frappe.utils.get_site_name(frappe.local.site) + \
            '/public'+data_file

    file = open(file_path)
    csvreader = csv.reader(file)

    stop_checker = False
    # result = mu_string.replace(",","", 1) #first comma
    for row in csvreader:
        writer.writerow(row)
        title.append(row)  

    """ fcsv = writer.getvalue()
    print(f'\n\n\n\n start : {fcsv} \n\n\n\n')
     """

    moldex_mac = frappe.get_doc(doctype, docname) 
    """ elif v == "Date":
                    spa = t[0].split(":")[-1]
                    mac_title[k] = get_datetime(spa) """

    for k,v in title_mac.items():
        for t in title:
            if v in t[0]:
                if not v == "Machine ID":
                    spa = t[0].split(":")[-1]
                    mac_title[k] = spa
                
                elif v == "Machine ID":
                    dspa = t[0].split(":")[-1]
                    spa = dspa.split(" ")
                    mac_title['machine_id'] = spa[1]
                    mac_title['computer_name'] = spa[-1].split("/")[0].replace("(","", 1)
                    mac_title['hard_disk'] = spa[-1].split("/")[1]
                    mac_title['mac_address'] = spa[-1].split("/")[-1].replace(")","", -1)
                break
    
    for k,v in version_mac.items():
        for t in title:
            if (not t == [])and (v in t[0]):
                spa = t[0].split("=")[-1]
                mac_title[k] = spa
                break
    #print(f'\n\n\n\n {mac_title} \n\n')  

    moldex3d_start_index = moldex_index(title,"[Moldex3D]") 
    moldex3d_end_index = moldex_index(title,"[Moldex3D Mesh]") - 3
    moldex3d_mesh_start = moldex_index(title,"[Moldex3D Mesh]") 
    moldex3d_caddoctor_start = moldex_index(title,"[Moldex3D CADdoctor]") 
    moldex3d_tools_start = moldex_index(title,"[Moldex3D Tools]") 
    moldex3d_end_line = len(title)

    mod3x_detail = get_moldex3d_list(title,moldex3d_start_index+1,moldex3d_mesh_start-3 if moldex3d_mesh_start > 0 else moldex3d_end_line -2)    
    #moldex3d_mesh = get_moldex3d_list(title,moldex3d_mesh_start+1 if moldex3d_mesh_start > 0 else moldex3d_end_line, moldex3d_caddoctor_start-3 if moldex3d_caddoctor_start > 0 else moldex3d_end_line -2)
    moldex3d_mesh = get_moldex3d_list(title,moldex3d_mesh_start+1 if moldex3d_mesh_start > 0 else moldex3d_end_line -2, moldex3d_end_line -2 if moldex3d_mesh_start < 0  else (moldex3d_caddoctor_start-3 if moldex3d_caddoctor_start > 0 else moldex3d_end_line -2) )
    #moldex3d_caddoctor = get_moldex3d_list(title,moldex3d_caddoctor_start+1  if moldex3d_caddoctor_start > 0 else moldex3d_end_line,moldex3d_tools_start-3 if moldex3d_tools_start > 0 else moldex3d_end_line -2)
    moldex3d_caddoctor = get_moldex3d_list(title,moldex3d_caddoctor_start+1  if moldex3d_caddoctor_start > 0 else moldex3d_end_line -2, moldex3d_end_line -2 if moldex3d_caddoctor_start < 0 else (moldex3d_tools_start-3 if moldex3d_tools_start > 0 else moldex3d_end_line -2))
    #moldex3d_tools = get_moldex3d_list(title,moldex3d_tools_start+1 if moldex3d_tools_start > 0 else moldex3d_end_line,moldex3d_end_line -2)
    moldex3d_tools = get_moldex3d_list(title,moldex3d_tools_start+1 if moldex3d_tools_start > 0 else moldex3d_end_line-2, moldex3d_end_line -2)

    #print(f'\n\n\n\n start start:{moldex3d_start_index} \n end index :{moldex3d_end_index} \n\n')
    moldex_mac.update(mac_title)
    if len(mod3x_detail) > 0 :
        for t in mod3x_detail:
            moldex_mac.append("moldex3d",t)

    if len(moldex3d_mesh):
        for t in moldex3d_mesh:
            moldex_mac.append("moldex3d",t)
    if len(moldex3d_caddoctor) > 0:
        for t in moldex3d_caddoctor:
            moldex_mac.append("moldex3d",t)
    
    if len(moldex3d_tools) > 0:
        for t in moldex3d_tools:
            moldex_mac.append("moldex3d",t)
    
    moldex_mac.save()


    #execute('Mac Moldex', to_date, 'csfrder', fcsv, lang=None, show_progress=True)
    file.close()
    
    return True

def moldex_index(mlist, term):
    """list, search term"""
    myreturn = -1
    for t in range(len(mlist)):
        if (not mlist[t] == []) and (term in mlist[t]):
            myreturn = t
            break
    return myreturn

def get_moldex3d_list(mxlist, start, end):
    subtable= ['software_name','software_key','licensemodesoftware','expire_date','no_license']
    mod3x_detail = []

    if (start == end):
        return mod3x_detail
    
    for t in range(start,end,2):
        
        modxd = {}
        modxd["software_name"] = mxlist[t][0].split("=")[0]
        modxd["software_key"] = mxlist[t][0].split("=")[-1]
        sx = len(mxlist[t][0].split("=")[0])+2
        submx = mxlist[t+1][0].split("=")[-1]
        modxd["licensemodesoftware"] = submx[sx:].split(")")[0]+")"
        modxd["expire_date"] =submx[sx:].split(")")[-1].split("-")[1]
        modxd["no_license"] =submx[sx:].split(")")[-1].split("-")[-1]
        
        mod3x_detail.append(modxd)
    
    return mod3x_detail
    
    

class UnicodeWriter:
	def __init__(self, encoding="utf-8", quoting=csv.QUOTE_NONNUMERIC):
		self.encoding = encoding
		self.queue = StringIO()
		self.writer = csv.writer(self.queue, quoting=quoting)

	def writerow(self, row):
		if six.PY2:
			row = encode(row, self.encoding)
		self.writer.writerow(row)

	def getvalue(self):
		return self.queue.getvalue()

def create_folder(folder, parent):
    """Make sure the folder exists and return it's name."""
    """
    Home/Mac Moldex
    doctype_folder = create_folder(_(doctype), "Home")
    title_folder = create_folder(title, doctype_folder)
    """
    new_folder_name = "/".join([parent, folder])
    
    if not frappe.db.exists("File", new_folder_name):
        create_new_folder(folder, parent)
    
    return new_folder_name
    