# -*- coding: utf-8 -*-

from odoo import models, fields

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def _create_invoices(self, grouped=False, final=False, date=None):
        res = super()._create_invoices(grouped=grouped, final=final, date=date)

        for invoice_id in res:
            order_id = self.env['sale.order'].search([('invoice_ids', 'in', invoice_id.ids)], limit=1)
            # Add invoice to task in order_line
            for order_line in order_id.order_line:
                for task in order_line.task_ids:
                    if not task.invoice_id:
                        task.invoice_id = invoice_id.id
            name = ""
            is_task = False

            for line in order_id.order_line:
                for task_id in line.task_ids:
                    name += str(task_id.name) + " " + str(task_id.code) + " " + str(task_id.planned_hours) + "H \n"
                    is_task = True
                line.task_ids = False

            if is_task:
                for move in invoice_id:
                    move.invoice_line_ids = [(0, 0, {
                        'name': name,
                        'display_type': 'line_note',
                        'sequence': 999,
                    })]

        return res

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    task_ids = fields.One2many('project.task', 'order_line_id', string='US', readonly=True)
    project_ids = fields.Many2many('project.project', related='order_id.project_ids', string='Projects')
