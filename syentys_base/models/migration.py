# -*- coding: utf-8 -*-
from odoo import models, fields


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    so_line_ids = fields.Char('So lines')

class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    inv_line_ids = fields.Char('Inv lines')

class AccountMove(models.Model):
    _inherit = "account.move"

    date_paiement = fields.Date('Date de paiement')