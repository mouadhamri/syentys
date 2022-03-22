# -*- coding: utf-8 -*-
{
    'name': "Gen invoices",
    'description': """
        Gen reports
    """,
    'author': "Syentys",
    'website': "http://www.syentys.fr",
    'category': 'Services/Project',
    'version': '15.0.1.0.0',
    'depends': ['base', 'project', 'account', 'sale', 'sale_timesheet', 'helpdesk','portal','hr_timesheet'],
    'data': [
        'views/account_views.xml',
    ],
    'license': 'LGPL-3',
}
