frappe.pages['moldex3d-spa'].on_page_load = function(wrapper) {
	var page = frappe.ui.make_app_page({
		parent: wrapper,
		title: 'Moldex 3D SPA',
		single_column: true
	});

	/* frappe.require('spa_dashboard.bundle.js', ()=>{
		console.log('spa bundle loaded');
	}) */
}
/*bench build --app [my app ]*/