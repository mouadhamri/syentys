# -*- coding: utf-8 -*-

from odoo import fields, models


class ResCompany(models.Model):
    _inherit = "res.company"

    num_guaranteed_date = fields.Integer(string="Date de garantie (mois)")
