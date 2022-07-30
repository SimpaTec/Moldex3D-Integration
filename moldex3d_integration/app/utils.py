
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
from frappe.utils import get_datetime,nowdate
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
    """
    'date':'Date',        
        'machine_id':'Machine ID',
    """
    title_mac ={
        'title':'Title' ,
        'version':'Version' ,
        'software':'Software',
        'copyright':'Copyright(c)',
        'tel':'TEL',
        'fax':'FAX',
        'website':'Website',
        'email':'Email',
        'customer':'Customer',        
        'customer_id':'Customer ID',
        'license_mode':'License Mode',
        'customer_class':'Customer Class',        
        'publishing_date':'Publishing Date',
        'date':'Date',        
        'machine_id':'Machine ID'                
    }
    version_mac = {
        'major':'Major',
        'minor':'Minor',
        'license_mode_ver':'LicenseMode',
        'trial_license':'TrialLicense',
    }

    writer = UnicodeWriter()
    
    file_path = frappe.utils.get_site_name(frappe.local.site) + \
            '/public'+data_file

    file = open(file_path)
    csvreader = csv.reader(file)

    expires_date = nowdate() #date = nowdate() if not posting_date else posting_date
    # result = mu_string.replace(",","", 1) #first comma
    for row in csvreader:
        writer.writerow(row)
        title.append(row)  

    """ fcsv = writer.getvalue()
    print(f'\n\n start : {fcsv} \n\n')
     """
    moldex_mac = frappe.get_doc(doctype, docname)    
    for k,v in title_mac.items(): 
        rtro = ""
        verifyr = ("customer" == k)        
        for t in title:
            ht = t[0].split(":")[0].replace(";","",1).strip()
            checkr = ("Customer" == ht)
            if checkr:
                rtro=t[0].split(":")[-1]                
                mac_title["customer"] = rtro
                

            if v in t[0]:                
                if v == "Date":
                    next = t[0]
                    if next.startswith(';'):                        
                        l2 = next[1:]
                        a =  l2.find(':')                    
                        tag = l2[a:].replace(":","", 1)                        
                        mac_title[k] = tag 
                     
                elif v == "Customer":                    
                    print(f'{rtro}')                    
                    
                elif v == "Machine ID":
                    dspa = t[0].split(":")[-1]
                    spa = dspa.split(" ")
                    mac_title['machine_id'] = spa[1]
                    mac_title['computer_name'] = spa[-1].split("/")[0].replace("(","", 1)
                    mac_title['hard_disk'] = spa[-1].split("/")[1]
                    mac_title['mac_address'] = spa[-1].split("/")[-1].replace(")","", -1)
                elif not v == "Machine ID":
                    spa = t[0].split(":")[-1]
                    mac_title[k] = spa
                break
    
    for k,v in version_mac.items():
        for t in title:
            if (not t == [])and (v in t[0]):
                spa = t[0].split("=")[-1]
                mac_title[k] = spa
                break
    
    counter =[]
    for t in range(28,len(title)):
        if (not title[t]== [] and ('[' in title[t][0])):
            counter.append(t)
    
    moldex_mac.update(mac_title)
    mod3x_detail = []
    for z in range(len(counter)):        
        start,end = 0,0
        if (not z == (len(counter)-1)):
            """do your stuff"""                                  
            start = counter[z]+1
            end = counter[z+1]-3
        elif (z == (len(counter)-1)):
            start = counter[z]+1
            end = len(title)-2

        for t in range(start,end,2):
            modxd = {}
            modxd["software_name"] = title[t][0].split("=")[0]
            modxd["software_key"] = title[t][0].split("=")[-1]
            next = title[t+1][0]
            if next.startswith(';'):
                tag = "Floating"
                l2 = next[1:]
                a =  l2.find('(')
                b =  l2.rfind(')')
                if a < b:
                    tag = l2[a:b+1]  
                    
                l2 = l2.split(tag,)[-1].split("-")
                modxd["licensemodesoftware"] = tag
                modxd["expire_date"] =l2[1]
                expires_date = l2[1]
                modxd["no_license"] =l2[-1]
            
            mod3x_detail.append(modxd)
            
    moldex_mac.expires_on = expires_date
    if len(mod3x_detail) > 0 :
        for t in mod3x_detail:
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
        #submx[sx:].split(")")[0]+")"
        
        
    
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
