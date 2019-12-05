# -*- coding: utf-8 -*-
# Copyright Nova Code (http://www.novacode.nl)
# See LICENSE file for full copyright and licensing details.

import logging

from odoo import _, api, fields, models

_logger = logging.getLogger(__name__)

class MailTemplateStyle(models.Model):
    _name = 'mail.template.style'
    _inherit = 'mail.thread'

    name = fields.Char(required=True)
    css = fields.Text(required=True, track_visibility='onchange')


class MailTemplate(models.Model):
    _inherit = 'mail.template'

    style_id = fields.Many2one('mail.template.style', string="Style (CSS)")
    print_ref = fields.Boolean(string='Print Reference', track_visibility='onchange')

    @api.multi
    def generate_email(self, res_ids, fields=None):
        self.ensure_one()
        results = super(MailTemplate, self).generate_email(res_ids, fields)

        if self.style_id and 'body_html' in results:
            body = '<style>%s</style>' % self.style_id.css
            body += results['body_html']
            results['body_html'] = body
        if self.print_ref and 'body_html' in results:
            ref = '<div id="mail_mail_template_ref" class="mt32"><small>(template: %s)</small></div>' % self.id

            results['body_html'] += ref
        results['body'] = results['body_html']
        return results
