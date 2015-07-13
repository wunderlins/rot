/*
 * File: app.js
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

// @require @packageOverrides
Ext.Loader.setConfig({

});


Ext.application({
    models: [
        'rotModel',
        'monthModel'
    ],
    stores: [
        'rotStore',
        'monthStore'
    ],
    views: [
        'MainView'
    ],
    controllers: [
        'rotController'
    ],
    name: 'calendar',

    launch: function() {
        Ext.create('calendar.view.MainView');

        rot.grid.init()
    }

});
