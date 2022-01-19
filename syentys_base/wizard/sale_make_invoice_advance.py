# -*- coding: utf-8 -*-


from odoo import fields, models


class SaleAdvancePaymentInv(models.TransientModel):
    _inherit = "sale.advance.payment.inv"

    def create_invoices(self):
        res = super(SaleAdvancePaymentInv, self).create_invoices()
        invoice_id = self.env['account.move'].browse(res.get('res_id'))
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
                                            'sequence': 0,
                                        })]
        return res
