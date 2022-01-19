# -*- coding: utf-8 -*-

from odoo import models, fields


class HelpdeskTicket(models.Model):
    _inherit = 'helpdesk.ticket'

    project_id = fields.Many2one('project.project', string='Projet')
    us_id = fields.Many2one('project.task', string='US')
    task_id = fields.Many2one('project.task', string='Tâche')
