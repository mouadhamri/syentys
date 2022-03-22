# -*- coding: utf-8 -*-

import base64
import io

from odoo import models, fields, api



class AccountMove(models.Model):
    _inherit = "account.move"

    def gen_report(self):
        report_obj = self.env['ir.actions.report']
        report_id = report_obj.search([('report_name','=','account.report_invoice_with_payments')])
        print(report_id)
        #report_id = self.env.ref('account.report_invoice_with_payments')
        if report_id:
            invoice_pdf, _ = report_id._render_qweb_pdf(self.id)
            name = f'inv_{self.id}.pdf'
            with open(name, 'wb') as report_file:
                report_file.write(invoice_pdf)
            #print(invoice_pdf)
        print("gen_report")



