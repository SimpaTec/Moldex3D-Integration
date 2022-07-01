
from frappe import _


def get_data():
	return {
		'fieldname': 'mif_file',
		'non_standard_fieldnames': {
			'MAC File': 'mif_file',
		},
		'transactions': [
			{
				'label': _('Mac File'),
				'items': ['MAC File']
			},
		]
	}
