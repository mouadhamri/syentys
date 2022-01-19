# -*- coding: utf-8 -*-

from odoo import models, fields


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    task_ids = fields.One2many('project.task', 'order_line_id', string='US', readonly=True)
    project_ids = fields.Many2many('project.project', related='order_id.project_ids', string='Projects')
