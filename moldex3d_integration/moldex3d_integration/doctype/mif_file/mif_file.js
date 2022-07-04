// Copyright (c) 2022, Jide Olayinka and contributors
// For license information, please see license.txt

frappe.ui.form.on('MIF File', {
	refresh: function(frm) {
		if(frm.is_new() ){
			frm.set_df_property("file_section", "hidden", 1);
		}	
	}
});
