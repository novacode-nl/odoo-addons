# -*- coding: utf-8 -*-
# Copyright Nova Code (http://www.novacode.nl)
# See LICENSE file for full copyright and licensing details.

{
    'name': 'Flow Field Log',
    'summary': 'Log field changes old/new value',
    'version': '0.2',
    'author': 'Nova Code',
    'website': 'https://www.novacode.nl',
    'license': "LGPL-3",
    'category': 'Extra Tools',
    'depends': ['base'],
    'application': False,
    'installable': False,
    'data': [
        'security/ir_model_access.xml',
        'views/flow_field_log_views.xml'
    ],
    'description': """
Log field changes old/new value
-------------------------------
"""
}
