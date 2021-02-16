# Copyright Nova Code (http://www.novacode.nl)
# See LICENSE file for full copyright and licensing details.

from odoo.addons.mail.models.mail_render_mixin import MailRenderMixin


def selection_label(model_obj, field, print_label=False):
    """
    Render the label of a selection field its value.
    
    USAGE (e.g. in mail.template)
    -----------------------------
    ${selection_label(object, "rent_term_type")}
    """
    field_def = model_obj.fields_get([field], ['selection', 'string'])[field]
    for row in field_def['selection']:
        if row[0] == getattr(model_obj, field):
            if print_label:
                return '%s: %s' % (field_def['string'], row[1])
            else:
                return '%s' % row[1]
    else:
        return ''

def monkey_patch(cls):
    """ Return a method decorator to monkey-patch the given class. """
    def decorate(func):
        name = func.__name__
        func.super = getattr(cls, name, None)
        setattr(cls, name, func)
        return func
    return decorate

@monkey_patch(MailRenderMixin)
def _render_jinja_eval_context(self):
    """ Prepare jinja evaluation context, containing for all rendering
    various formatting tools """
    res = _render_jinja_eval_context.super(self)
    res['selection_label'] = lambda model_obj, field: selection_label(model_obj, field)
    return res
