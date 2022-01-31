# -*- coding: utf-8 -*-

from odoo import api, fields, models


class SaleAddTaskWizard(models.TransientModel):
    _name = 'sale.add.task.wizard'
    _description = 'Wizard pour ajout des tasks'

    task_line_ids = fields.One2many('sale.add.task.wizard.line', 'wizard_id')

    @api.model
    def default_get(self, fields):
        res = super(SaleAddTaskWizard, self).default_get(fields)
        order_line = self.env.context.get('active_id', False)
        order_line_id = self.env['sale.order.line'].browse(order_line)
        us_vals = []
        if order_line_id.order_id.project_ids:
            tasks = self.env['project.task'].search(
                [('display_project_id', 'in', order_line_id.order_id.project_ids.ids), ('invoice_id', '=', False), ('sale_line_id.product_id', '=', order_line_id.product_id.id)]) - order_line_id.task_ids
        else:
            tasks = False
        if tasks:
            for task in tasks:
                us_vals.append((0, 0, {'task_id': task.id}))
            res['task_line_ids'] = us_vals
        return res

    def add_tasks(self):
        order_line = self.env.context.get('active_id', False)
        order_line_id = self.env['sale.order.line'].browse(order_line)
        last_planned_hours = 0.0
        if self.task_line_ids and any(l.selected for l in self.task_line_ids):
            tasks = self.task_line_ids.filtered(lambda t: t.selected)
            # Get previous planned hours from line
            if order_line_id.task_ids:
                last_planned_hours = sum(task.planned_hours for task in order_line_id.task_ids)
            for task in tasks:
                line_id = self.env['sale.order.line'].search([('task_ids', 'in', task.task_id.id)])
                # If the task exist in another line
                if line_id and line_id.id != order_line_id.id:
                    line_id.write({'qty_delivered': line_id.qty_delivered - task.task_id.planned_hours})
                task.task_id.order_line_id = order_line_id.id
            planned_hours = sum(task.planned_hours for task in order_line_id.task_ids)
            order_line_id.write({'qty_delivered': order_line_id.qty_delivered + planned_hours - last_planned_hours})

        return True


class SaleAddTaskWizardLine(models.TransientModel):
    _name = 'sale.add.task.wizard.line'
    _description = 'Ligne de wizard add task'

    name = fields.Char(string='Nom', related='task_id.name',store=True)
    wizard_id = fields.Many2one('sale.add.task.wizard')
    task_id = fields.Many2one('project.task', string='US')
    partner_id = fields.Many2one('res.partner', related='task_id.partner_id', string='Client')
    date_deadline = fields.Date(string='Date limite', related='task_id.date_deadline',store=True)
    code = fields.Char(string='Code', related='task_id.code',store=True)
    planned_hours = fields.Float(string='#Heures', related='task_id.planned_hours',store=True)
    project_id = fields.Many2one('project.project', related='task_id.project_id', string='Projet')
    stage_id = fields.Many2one('project.task.type', related='task_id.stage_id', string='Stage',store=True)
    sequence = fields.Integer('Séquence')
    selected = fields.Boolean('Choisi')
