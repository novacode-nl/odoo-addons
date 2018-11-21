odoo.define('web_tree_field_add_class', function (require) {
    'use strict';

    var ListRenderer = require('web.ListRenderer');
    var pyeval = require('web.pyeval');

    ListRenderer.include({
        /**
         * Add class attribute on a cell during it's render
         *
         * @override
         */
        _renderBodyCell: function (record, node, colIndex, options) {
            var $td = this._super.apply(this, arguments);
            this.addClass($td, record, node);
            return $td;
        },

        /**
         * @param {Query Node} $td a <td> tag inside a table representing a list view
         * @param {Object} node an XML node (must be a <field>)
         */
        addClass: function ($td, record, node, ctx) {
            if (!node.attrs.options) { return; }
            if (node.tag !== 'field') { return; }
            var nodeOptions = node.attrs.options;
            console.log(nodeOptions);
            if (!_.isObject(nodeOptions)) {
                nodeOptions = pyeval.py_eval(nodeOptions);
            }
            this.addClassHelper($td, nodeOptions, node, ctx);
        },

        /**
         * @param {Object} nodeOptions a mapping of nodeOptions parameters
         * @param {Object} node an XML node (must be a <field>)
         */
        addClassHelper: function ($td, nodeOptions, node, ctx) {
            if (nodeOptions['add_class']) {
                $td.addClass(nodeOptions['add_class']);
            }
        },
    });
});
