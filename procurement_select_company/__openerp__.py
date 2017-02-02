# -*- coding: utf-8 -*-
# Copyright 2017 KMEE
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Procurement Select Company',
    'summary': """
        Change procurement wizard to allow the user select the company that he wants to run the scheduler""",
    'version': '8.0.1.0.0',
    'license': 'AGPL-3',
    'author': 'KMEE,Odoo Community Association (OCA)',
    'website': 'www.kmee.com.br',
    'depends': [
	'procurement',
        'stock',
    ],
    'data': [
        'views/procurement_order_compute_all.xml',
    ],
    'demo': [
    ],
}
