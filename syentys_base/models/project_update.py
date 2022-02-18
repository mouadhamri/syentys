# -*- coding: utf-8 -*-

from odoo import models, fields, api
from dateutil.relativedelta import relativedelta


class projectUpdate(models.Model):
    _inherit = "project.update"

    @api.model
    def _build_description(self, project):
        return "<h1>Description</h1>"