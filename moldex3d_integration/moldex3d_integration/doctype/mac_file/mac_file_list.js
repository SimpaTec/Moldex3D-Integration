frappe.listview_settings['MAC File'] = {
    onload: function(list_view) {
		let me = this;
		//const _filename = (name) => `${name}-MX3d.csv`; //.pdf
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
                    {
					fieldname: 'upload_mac',
					label: __('Upload mac file'),
					fieldtype: 'Data',
                    hidden: 1
                    }],
				primary_action(data) {
                    var filedata = $('#upload_mac')[0].files[0];
					if (filedata == undefined && filedata.name == null) {
						frappe.msgprint(__("Upload a .mac file"
							));
					} else {
						frappe.confirm(__('Process Mac file '), () => {
                            
                            //console.log(`you: ${filedata.name} `);
							frappe.call({
								method: "moldex3d_integration.moldex3d_integration.doctype.mac_file.mac_file.process_moldex_mac",
								args: {
									data: list_view.doctype
								},
								callback: function (r) {
                                    //
                                    //console.log('first call: ',r.message);
					if (r.message != null ) {
						frappe.show_alert({
							message: __("Mac file Processed ... : ",r.message),
							indicator: 'blue'
						});
						
					}
					if(r.message && filedata){
						//console.log(`${_filename(r.message)} to south: `)
						let imagefile = new FormData();
						//imagefile.append("is_private", 0);
						imagefile.append('doctype',list_view.doctype);
						imagefile.append('docname', r.message);						
						
						imagefile.append('folder', "Home/"+list_view.doctype);						
						//imagefile.append('file_name', _filename(r.message));
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
							//console.log('middle:',data);
							if (data.message){
								//console.log('getin me :',data.message.file_url);
								frappe.call({				
									method: 'moldex3d_integration.moldex3d_integration.doctype.mac_file.mac_file.update_moldex_mac',
									
									args: {
										doctype:list_view.doctype,
										docname: r.message,
										data_file: data.message.file_url
									}
								}).then(r => {
									var options = [];
									//console.log('final call',r.message);
									frm.reload_doc();
								});
								//
							}
						})
						//frm.refresh();
						//frappe.set_route("Form",list_view.doctype,r.message);						
					}
				}
			});
		});
	}					
					dialog.hide();
					list_view.refresh();
				},
				primary_action_label: __('Process Mac File')

			});
			//dialog.$wrapper.find('.btn-modal-primary').css("color","red");
			dialog.$wrapper.find('.btn-modal-primary').removeClass('btn-primary').addClass('btn-dark');
			dialog.show();
		});
		list_view.page.change_inner_button_type('Process Mac File',null, 'dark');
	},
    
}