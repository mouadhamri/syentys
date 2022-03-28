# -*- coding: utf-8 -*-
from odoo import models, fields


class Lead(models.Model):
    _inherit = "crm.lead"

    department = fields.Char(string="Département")
    region = fields.Char(string="Région")
    siret = fields.Char(string="Siret")
    naf = fields.Char(string="Naf")
    tranche_effectif = fields.Char(string="Tranche de l'effectif")
    code_ape = fields.Char(string="Code APE")
    task_name = fields.Char(string="Étiquettes/Nom")
