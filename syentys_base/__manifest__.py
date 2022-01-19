# -*- coding: utf-8 -*-
{
    'name': "Syentys Base",
    'description': """
        Adding specific tools to Odoo project
    """,
    'author': "Syentys",
    'website': "http://www.syentys.fr",
    'category': 'Services/Project',
    'version': '15.0.1.0.0',
    'depends': ['base', 'project', 'account', 'sale', 'sale_timesheet', 'helpdesk'],
    'data': [
        'security/ir.model.access.csv',
        'views/project_views.xml',
        'wizard/sale_add_task_wizard.xml',
        'views/sale_views.xml',
        'views/helpdesk_views.xml',
        'views/res_company_views.xml',
        'views/account_move_views.xml',
    ],
    'license': 'LGPL-3',
}
