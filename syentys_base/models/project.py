# -*- coding: utf-8 -*-

from odoo import models, fields, api
from dateutil.relativedelta import relativedelta


class Project(models.Model):
    _inherit = "project.project"

    task_sequence = fields.Many2one('ir.sequence', string="Séquence de l'US")
    tickets_count = fields.Integer("Nombre de ticket", compute='_compute_tickets_count')

    def _compute_tickets_count(self):
        for project in self:
            project.tickets_count = self.env['helpdesk.ticket'].search_count([('project_id', '=', project.id)])

    @api.model
    def create(self, vals):
        if vals.get('name'):
            IrSequence = self.env['ir.sequence'].sudo()
            val = {
                'name': vals.get('name'),
                'prefix': vals.get('name')[:3].upper(),
                'padding': 5,
                'code': vals.get('name')+".sequence",
            }
            vals['task_sequence'] = IrSequence.create(val).id
        return super(Project, self).create(vals)

    def action_view_ticket(self):
        self.ensure_one()
        action = self.env["ir.actions.actions"]._for_xml_id('helpdesk.helpdesk_ticket_action_main_tree')
        action.update({
            'domain': [('project_id', '=', self.id)],
        })
        return action

    def action_open_project(self):
        return {
            'view_mode': 'form',
            'res_model': 'project.project',
            'res_id': self.id,
            'type': 'ir.actions.act_window',
            'context': self._context
        }


class Task(models.Model):
    _inherit = "project.task"

    code = fields.Char(readonly=True)
    invoice_id = fields.Many2one('account.move', string='Facture')
    order_line_id = fields.Many2one('sale.order.line', string='Commande')
    guaranteed_date = fields.Date(string='Date de garantie', readonly=True, compute='_compute_guaranteed_date')

    @api.depends('stage_id', 'stage_id.update_guaranteed_date', 'company_id', 'company_id.num_guaranteed_date')
    def _compute_guaranteed_date(self):
        for task in self:
            if task.stage_id.update_guaranteed_date:
                task.guaranteed_date = fields.Datetime.now() + relativedelta(months=task.company_id.num_guaranteed_date)
            else:
                task.guaranteed_date = False

    @api.model_create_multi
    def create(self, vals):
        res = super().create(vals)
        if res:
            for rec in res:
                if rec.project_id and rec.project_id.task_sequence and not rec.parent_id:
                    rec.code = self.env['ir.sequence'].next_by_code(rec.project_id.task_sequence.code)
        return res

class ProjectStage(models.Model):
    _inherit = "project.task.type"

    update_guaranteed_date = fields.Boolean(string="Mettre à jour date garantie")
