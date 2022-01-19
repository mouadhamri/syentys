# -*- coding: utf-8 -*-
from odoo import models, fields


class AccountMove(models.Model):
    _inherit = "account.move"

    tasks_count = fields.Integer(string="Nombre de tâches", compute='_compute_tasks_count')

    def _compute_tasks_count(self):
        for rec in self:
            tasks = rec.env['project.task'].search_count([('invoice_id', '=', rec.id)])
            rec.tasks_count = tasks

    def action_view_related_task(self):
        action = self.env["ir.actions.actions"]._for_xml_id("project.action_view_task")
        action['domain'] = [('invoice_id', 'in', self.ids)]
        return action
