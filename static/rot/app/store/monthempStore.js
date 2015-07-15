/*
 * File: app/store/monthempStore.js
 *
 * This file was generated by Sencha Architect version 3.1.0.
 * http://www.sencha.com/products/architect/
 *
 * This file requires use of the Ext JS 5.0.x library, under independent license.
 * License of Sencha Architect does not include license for Ext JS 5.0.x. For more
 * details see http://www.sencha.com/license or contact license@sencha.com.
 *
 * This file will be auto-generated each and everytime you save your project.
 *
 * Do NOT hand edit this file.
 */

Ext.define('calendar.store.monthempStore', {
    extend: 'Ext.data.Store',

    requires: [
        'calendar.model.monthempModel',
        'Ext.data.proxy.Ajax',
        'Ext.data.reader.Json'
    ],

    constructor: function(cfg) {
        var me = this;
        cfg = cfg || {};
        me.callParent([Ext.apply({
            storeId: 'monthempStore',
            model: 'calendar.model.monthempModel',
            proxy: {
                type: 'ajax',
                url: '../../get_month',
                reader: {
                    type: 'json',
                    rootProperty: 'root',
                    totalProperty: 'count'
                },
                listeners: {
                    metachange: {
                        fn: me.onAjaxMetaChange,
                        scope: me
                    }
                }
            },
            listeners: {
                metachange: {
                    fn: me.onJsonstoreMetaChange,
                    scope: me
                },
                endupdate: {
                    fn: me.onJsonstoreEndupdate,
                    scope: me
                },
                beforeload: {
                    fn: me.onJsonstoreBeforeLoad,
                    scope: me
                }
            }
        }, cfg)]);
    },

    onAjaxMetaChange: function(proxy, meta, eOpts) {
        console.log("Reader MEtaChange");
    },

    onJsonstoreMetaChange: function(store, meta, eOpts) {
        console.log("MetaChange for rotStore");
        /*
        // create a new model
        rot.model = Ext.define('calendar.model.rotModel', {
            extend: 'Ext.data.Model',
            requires: [
                'Ext.data.field.Integer',
                'Ext.data.field.String'
            ],

            fields: meta.fields
        });
        console.log(meta.fields);
        console.log(meta.columns);
        store.setModel(rot.model);
        rot.grid.grid.reconfigure(store, meta.columns);
        */
    },

    onJsonstoreEndupdate: function(eOpts) {
        console.log("Done updating rotStore");
    },

    onJsonstoreBeforeLoad: function(store, operation, eOpts) {
        console.log("onBeforeLoad monthempStore");

        //rot.get_meta(store, operation, eOpts);
        //rot.prepare_load();
    }

});