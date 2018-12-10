# -*- coding: utf-8 -*-
# Copyright 2018 Nova Code (http://www.novacode.nl)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html)

from odoo import api, fields, models


class FieldLog(models.AbstractModel):
    _name = 'flow.field.log'
    _description = 'Flow: Field log'

    def _flow_fields_log(self):
        return []

    @api.multi
    def write(self, vals):
        model = False
        fieldlog = []
        for f in self._flow_fields_log():
            if f in vals:
                if not model:
                    model = self.env.ref('helpdesk.model_helpdesk_ticket')
                domain = [('name', '=', f), ('model_id.model', '=', self._name)]
                field = self.env['ir.model.fields'].search(domain, limit=1)
                # Prepare vals for fieldlog.
                fieldlog_vals = {
                    'model_id': model.id,
                    'res_id': self.id,
                    'field_id': field.id
                }
                if field.ttype == 'boolean':
                    fieldlog_vals['old_value_boolean'] = getattr(self, field.name)
                    fieldlog_vals['new_value_boolean'] = vals.get(f)
                    fieldlog.append(fieldlog_vals)
        res = super(FieldLog, self).write(vals)
        if self.write_date and fieldlog:
            for fl_vals in fieldlog:
                fl_vals['log_date'] = self.write_date
                self.env['flow.field.log.line'].create(fl_vals)
        return res


class FieldLogLine(models.Model):
    _name = 'flow.field.log.line'
    _description = 'Flow: Field log line'
    _rec_name = 'field_id'

    model_id = fields.Many2one('ir.model', required=True)
    res_id = fields.Integer(required=True)
    field_id = fields.Many2one('ir.model.fields', required=True)
    field_type = fields.Selection(related='field_id.ttype')
    old_value_boolean = fields.Boolean()
    new_value_boolean = fields.Boolean()
    old_value_char = fields.Char()
    new_value_char = fields.Char()
    old_value_date = fields.Date()
    new_value_date = fields.Date()
    old_value_datetime = fields.Datetime()
    new_value_datetime = fields.Datetime()
    old_value_float = fields.Float()
    new_value_float = fields.Float()
    old_value_integer = fields.Integer()
    new_value_integer = fields.Integer()
    log_date = fields.Datetime()

    def get_last(self, model_id, field_id, add_domain=[]):
        domain = [('model_id', '=', model_id), ('field_id', '=', field_id)]
        if add_domain:
            [domain.append(_filter) for _filter in add_domain]
        res = self.search(domain, limit=1, order='create_date DESC')
        return res
