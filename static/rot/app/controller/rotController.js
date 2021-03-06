/*
 * File: app/controller/rotController.js
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

Ext.define('calendar.controller.rotController', {
    extend: 'Ext.app.Controller',

    control: {
        "#btnReload": {
            click: 'loadData'
        },
        "#vonm": {
            change: 'load_mata_vonm'
        },
        "#vony": {
            change: 'load_mata_vony'
        },
        "#bism": {
            change: 'load_mata_bism'
        },
        "#bisy": {
            change: 'load_mata_bisy'
        }
    },

    loadData: function(button, e, eOpts) {
        rot.loadData(button, e, eOpts);
        //rot.get_meta();
    },

    load_mata_vonm: function(field, newValue, oldValue, eOpts) {
        rot.get_meta(field, newValue, oldValue);
    },

    load_mata_vony: function(field, newValue, oldValue, eOpts) {
        if (newValue > 999)
            rot.get_meta(field, newValue, oldValue);
    },

    load_mata_bism: function(field, newValue, oldValue, eOpts) {
        rot.get_meta(field, newValue, oldValue);
    },

    load_mata_bisy: function(field, newValue, oldValue, eOpts) {
        if (newValue > 999)
            rot.get_meta(field, newValue, oldValue);
    },

    onLaunch: function() {

        /*
        var values = Ext.state.Manager.get('searchForm');
        	alert(values.von.y);

        	rot.get("#vonm").setValue(values.von.m);
        	rot.get("#vony").setValue(values.von.y);
        	rot.get("#bism").setValue(values.bis.m);
        	rot.get("#bisy").setValue(values.von.y);
        */
    }

});
