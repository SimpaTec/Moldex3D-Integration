frappe.listview_settings['MAC File'] = {
    onload: function(list_view) {
		//let me = this;
		//var filedata = "";
		list_view.page.add_inner_button(__("Process Mac File"), function() {
					
			let dialog = new frappe.ui.Dialog({
					title: __("Process Mac File"),
					fields: [
						{
							fieldname: "upload_component",
							label: "Upload Component",
							fieldtype: "HTML",
							options: "<input id=\"upload_mac\" type=\"file\" value=\"process\">"
						},
					],
					primary_action(data) {
						let filedata = $('#upload_mac')[0].files[0];						
						if (filedata == undefined && filedata.name == null) {							
						frappe.msgprint(__("Upload a .mac file"));
						} 
						else {							

							frappe.confirm(__('Process Mac file '), () => {
								frappe.call({
									method: "moldex3d_integration.moldex3d_integration.doctype.mac_file.mac_file.process_moldex_mac",
									args: {
										data: list_view.doctype
									},
									callback: function (r) {										
										if (r.message != null ) {
											frappe.show_alert({
											message: __("Mac file Processed ... : ",r.message),
											indicator: 'blue'
											});
								
										}
										if(r.message && filedata){
											let imagefile = new FormData();
								
											imagefile.append('doctype',list_view.doctype);
											imagefile.append('docname', r.message);						
								
											imagefile.append('folder', "Home/"+list_view.doctype);						
								
											imagefile.append('file', filedata);

											fetch('/api/method/upload_file', {
												headers: {
													'X-Frappe-CSRF-Token': frappe.csrf_token
												},
												method: 'POST',
												body: imagefile
											})
											.then(res => res.json())
											.then(data => {
									
												if (data.message){													
											
													frappe.call({				
														method: 'moldex3d_integration.moldex3d_integration.doctype.mac_file.mac_file.update_moldex_mac',
												
														args: {
															doctype:list_view.doctype,
															docname: r.message,
															data_file: data.message.file_url
														}
													})
													.then(r => {
														var options = [];
												
														list_view.refresh();
													});
											
												}
											})
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
    
}