
frappe.listview_settings['MAC File'] = {
    onload: function(list_view) {
		let me = this;
		//var filedata = "";
		list_view.page.add_inner_button(__("Process Mac File"), function() {
					
			let dialog = new frappe.ui.Dialog({
					title: __("Process Mac File"),
					fields: [
						{
							fieldname: "upload_component",
							label: "Upload Component",
							fieldtype: "HTML",
							options: "<input id=\"upload_mac\" type=\"file\" accept=\".mac\" value=\"process\">"
						},
					],
					primary_action(data) {
						let filedata = $('#upload_mac')[0].files[0];
						if (!filedata || (filedata && !filedata.name)) {
							frappe.throw(__("Upload a .mac file"));
						} 
						else {							

							frappe.confirm(__('Process Mac file '), () => {
								frappe.call({
									method: "moldex3d_integration.moldex3d_integration.doctype.mac_file.mac_file.process_moldex_mac",
									args: {
										data: list_view.doctype
									},
									callback: function (r) {										
										if (r.message) {
											me.upload_and_attach_macfile(r.message, list_view.doctype, filedata)
											frappe.show_alert({
												message: __("Mac file Processed ... : ",r.message),
												indicator: 'blue'
											});
										}
									}
								});
							})
							
						}							
						dialog.set_df_property("upload_component", "options", []);
						dialog.hide();
						list_view.refresh();					
						
					},
					primary_action_label: __('Process Mac File')

			});
			
			dialog.show();
			dialog.$wrapper.find('.btn-modal-primary').removeClass('btn-primary').addClass('btn-dark');		
			
		});
		list_view.page.change_inner_button_type('Process Mac File',null, 'dark');

	},

	// upload_and_attach_macfile: function (r, macfiledata, list_view) {
	upload_and_attach_macfile: function (doctype, docname, macfiledata) {
		let macfile = new FormData();

		macfile.append('doctype',doctype);
		macfile.append('docname', docname);
		macfile.append('folder', "Home/"+doctype);
		macfile.append('file', macfiledata);

		fetch('/api/method/moldex3d_integration.moldex3d_integration.doctype.mac_file.mac_file.upload_attach_macfile', {
			headers: {
				'X-Frappe-CSRF-Token': frappe.csrf_token
			},
			method: 'POST',
			body: macfile
		})
	},
	
    
}

