// Copyright (c) 2022, Jide Olayinka and contributors
// For license information, please see license.txt

frappe.ui.form.on('MAC File', {
	refresh: function(frm) {
		if(!frm.is_new() ){
			frm.set_df_property("process_section", "hidden", 1);
		}	

	},
	process_file: function (frm) {
		const _filename = (name) => `${name}-MX3d.mac`; //.pdf
		var filedata = $('#upload_mac')[0].files[0];
		if (filedata != undefined && filedata.name != null) {
			console.log(`you: ${filedata.name} `);
			frappe.call({
				method: "moldex3d_integration.moldex3d_integration.doctype.mac_file.mac_file.process_moldex_mac",
				args: {
					data: frm.doc.doctype
				},
				callback: function (r) {
					//console.log('first call : ',r.message,'doctype : ',frm.doc.doctype);
					if (r.message != null ) {
						frappe.show_alert({
							message: __("Mac file Processed ... : ",r.message),
							indicator: 'blue'
						});
						
					}
					if(r.message && filedata){
						//console.log(`to south: ${r.message}  `)
						
						let imagefile = new FormData();
						//imagefile.append("is_private", 0);
						imagefile.append('doctype',frm.doc.doctype);
						imagefile.append('docname', r.message);						
						
						imagefile.append('folder', "Home/"+frm.doc.doctype);						
						//imagefile.append('file_name', _filename(r.message));
						imagefile.append('file', filedata);

						fetch('/api/method/upload_file', {
							headers: {
								'X-Frappe-CSRF-Token': frappe.csrf_token
							},
							method: 'POST',
							body: imagefile
						})
						.then(res => 
							res.json())
						.then(data => {
							//console.log('middle:',data.message.file_url);
							if (data.message){
								frappe.call({				
									method: 'moldex3d_integration.moldex3d_integration.doctype.moldex_mac.moldex_mac.update_moldex_mac',
									
									args: {
										doctype:frm.doc.doctype,
										docname: r.message,
										data_file: data.message.file_url
									}
								}).then(rs => {
									var options = [];
									console.log('final call :',rs.message);
								
								});
								
							}
						})
						//frm.refresh();
						//frappe.set_route("Form",frm.doc.doctype,r.message);
						frappe.set_route("Form",frm.doc.doctype,'');
					}
				}
				
			});
			frm.reload_doc();
			//frappe.set_route("Form",frm.doc.doctype,r.message);
		}
		else {
			frappe.msgprint('Please select a moldex mac file');
		}
	  },
});