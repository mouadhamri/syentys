# -*- coding: utf-8 -*-
{
    'name': "Portale customisation",
    'description': """
        Custome portale
    """,
    'author': "Syentys",
    'website': "http://www.syentys.fr",
    'category': 'Services/Project',
    'version': '15.0.1.0.0',
    'depends': ['base', 'project', 'account', 'sale', 'sale_timesheet', 'helpdesk'],
    "depends": [
        "portal",
        "sale",
        "sale_timesheet",
        "project",
        "hr_timesheet",
        "purchase",
        "appointment",
    ],
    "data": [
        "views/custome_portal_templates.xml",
    ],
    "installable": True,
}
