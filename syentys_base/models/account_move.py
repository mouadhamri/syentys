# -*- coding: utf-8 -*-
from odoo import models, fields, api


class AccountMove(models.Model):
    _inherit = "account.move"

    tasks_count = fields.Integer(string="Nombre de tâches", compute='_compute_tasks_count')
    payment_delay_days = fields.Integer(string="Retrad de paiement (jours)", compute='_compute_payemnt_delay', group_operator="avg", store=True)

    def _compute_tasks_count(self):
        for rec in self:
            tasks = rec.env['project.task'].search_count([('invoice_id', '=', rec.id)])
            rec.tasks_count = tasks

    def action_view_related_task(self):
        action = self.env["ir.actions.actions"]._for_xml_id("project.action_view_task")
        action['domain'] = [('invoice_id', 'in', self.ids)]
        return action

    @api.depends('line_ids','invoice_line_ids','invoice_date_due','amount_residual','line_ids.matched_debit_ids','line_ids.matched_credit_ids')
    def _compute_payemnt_delay(self):
        today = fields.Date.today()
        for inv in self:
            res = 0
            if inv.invoice_date_due and today > inv.invoice_date_due:
                if inv.amount_residual > 0:
                    res = (today - inv.invoice_date_due).days
                else:
                    dates = []
                    for line in inv._get_reconciled_invoices_partials():
                        _, _, move = line
                        dates.append(move.date)
                    if dates:
                        res = (max(dates) - inv.invoice_date_due).days
            inv.payment_delay_days = res

