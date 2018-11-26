odoo.define('web_tree_field_add_class', function (require) {
    'use strict';

    var ListRenderer = require('web.ListRenderer');
    var pyeval = require('web.pyeval');

    ListRenderer.include({
        /**
         * Add class attribute on a table td (cell) during it's render
         *
         * @override
         */
        _renderBodyCell: function (record, node, colIndex, options) {
            var $td = this._super.apply(this, arguments);
            this.addClass($td, node);
            return $td;
        },

        /**
         * Add class attribute on a table th (heading) during it's render
         *
         * @override
         */
        _renderHeaderCell: function (node) {
            var $th = this._super.apply(this, arguments);
            this.addClass($th, node);
            return $th;
        },

        /**
         * @param {Query Node} $el a tag (td,th) inside a table representing a list view
         * @param {Object} node an XML node (must be a <field>)
         */
        addClass: function ($el, node, ctx) {
            if (!node.attrs.options) { return; }
            if (node.tag !== 'field') { return; }
            var nodeOptions = node.attrs.options;
            if (!_.isObject(nodeOptions)) {
                nodeOptions = pyeval.py_eval(nodeOptions);
            }
            this.addClassHelper($el, nodeOptions, node, ctx);
        },

        /**
         * @param {Object} nodeOptions a mapping of nodeOptions parameters
         * @param {Object} node an XML node (must be a <field>)
         */
        addClassHelper: function ($el, nodeOptions, node, ctx) {
            if (nodeOptions['add_class']) {
                $el.addClass(nodeOptions['add_class']);
            }
        },
    });
});
