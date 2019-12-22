# -*- coding: utf-8 -*-
# Copyright Nova Code (http://www.novacode.nl)
# See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class MailTemplate(models.Model):
    _inherit = 'mail.template'

    module_name = fields.Char(string='Module')
    xmlid = fields.Char(string='XML ID')

    def action_update_external_id(self):
        for r in self:
            ext_id = r.get_external_id()
            if ext_id and ext_id.get(r.id):
                xmlid = ext_id.get(r.id).split('.')
                if len(xmlid) > 1:
                    vals = {'module_name': xmlid[0], 'xmlid': xmlid[1]}
                else:
                    vals = {'xmlid': xmlid[0]}
                r.write(vals)

    def init(self):
        templates = self.env['mail.template'].search([])
        for r in templates:
            ext_id = r.get_external_id()
            if ext_id and ext_id.get(r.id):
                xmlid = ext_id.get(r.id).split('.')
                if len(xmlid) > 1:
                    vals = {'module_name': xmlid[0], 'xmlid': xmlid[1]}
                else:
                    vals = {'xmlid': xmlid[0]}
                r.write(vals)
