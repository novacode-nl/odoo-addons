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

        if not self.style_id or 'body_html' not in results:
            return results

        if self.print_ref:
            results['body'] += self._print_ref()
            results['body_html'] += self._print_ref()

        body_html = '<style>%s</style>' % self.style_id.css
        body_html += results['body_html']

        results['body'] = body_html
        results['body_html'] = body_html

        return results

    def _print_ref(self):
        ref = '<div id="mail_mail_template_ref" class="mt32"><small>(template ID: %s)</small></div>' % self.id
        return ref


class MailMail(models.Model):
    _inherit = 'mail.mail'

    @api.multi
    def send_get_mail_body(self, partner=None):
        self.ensure_one()
        body_html = self.body_html or ''

        if '<style>' in body_html and '</style>' in body_html:
            body_html = body_html.replace('<style>', '<head><style>')
            body_html = body_html.replace('</style>', '</style></head><body>')
            body_html = '<html>{body_html}</body></html>'.format(body_html=body_html)
        return body_html
