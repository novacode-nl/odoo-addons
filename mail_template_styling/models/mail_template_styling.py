# -*- coding: utf-8 -*-
# Copyright Nova Code (http://www.novacode.nl)
# See LICENSE file for full copyright and licensing details.

import logging

from premailer import transform

from odoo import _, api, fields, models
from odoo.tools import html_sanitize


class MailTemplateStyle(models.Model):
    _name = 'mail.template.style'
    _inherit = 'mail.thread'

    name = fields.Char(required=True)
    css = fields.Text(required=True, track_visibility='onchange')


class MailTemplate(models.Model):
    _inherit = 'mail.template'

    style_id = fields.Many2one('mail.template.style', string="Stylesheet")
    strip_inline_style = fields.Boolean(
        string='Strip Inline Style',
        help="""Remove inline style (CSS attributes) during rendering-time. Just post-processing, which ain't stored."""
)
    print_ref = fields.Boolean(string='Print Reference', track_visibility='onchange')

    def generate_email(self, res_ids, fields=None):
        self.ensure_one()
        results = super(MailTemplate, self).generate_email(res_ids, fields)

        if 'body_html' not in results:
            return results

        body_html = results['body_html']

        if self.strip_inline_style:
            # Just do: strip_style=True
            body_html = html_sanitize(body_html, sanitize_tags=False, sanitize_attributes=False, sanitize_style=False, strip_style=True)
        if self.print_ref:
            body_html += self._print_ref()
        if self.style_id:
            body_html = '<style type="text/css">%s</style>%s' % (self.style_id.css, body_html)
            # premailer (transform) generates inline CSS/style attributes.
            body_html = transform(body_html, allow_network=False)

        results['body'] = body_html
        results['body_html'] = body_html

        return results

    def _print_ref(self):
        ref = '<div id="mail_mail_template_ref"><p>(%s: %s)</p></div>' % (_('template ID'), self.id)
        return ref
