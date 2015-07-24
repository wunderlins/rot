/*
 * File: app/store/assiStore.js
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

Ext.define('calendar.store.assiStore', {
    extend: 'Ext.data.Store',

    requires: [
        'calendar.model.assiModel',
        'Ext.data.proxy.Ajax',
        'Ext.data.reader.Json'
    ],

    constructor: function(cfg) {
        var me = this;
        cfg = cfg || {};
        me.callParent([Ext.apply({
            storeId: 'assiStore',
            model: 'calendar.model.assiModel',
            sortOnLoad: false,
            proxy: {
                type: 'ajax',
                url: '../../get_emp',
                reader: {
                    type: 'json',
                    rootProperty: 'root',
                    totalProperty: 'count'
                }
            },
            listeners: {
                load: {
                    fn: me.onJsonstoreLoad,
                    scope: me
                }
            }
        }, cfg)]);
    },

    onJsonstoreLoad: function(store, records, successful, eOpts) {
        //console.log("monthempStoreAll: onJsonstoreLoad");
        rot.personal_load(store, records, successful, eOpts);
    }

});