/*
 * File: app/view/MainView.js
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

Ext.define('calendar.view.MainView', {
    extend: 'Ext.container.Viewport',
    alias: 'widget.mainview',

    requires: [
        'calendar.view.MainViewViewModel',
        'calendar.view.MainViewViewController',
        'Ext.form.field.ComboBox',
        'Ext.form.field.TextArea',
        'Ext.grid.Panel',
        'Ext.grid.View',
        'Ext.grid.column.Column',
        'Ext.selection.CellModel',
        'Ext.grid.feature.Grouping',
        'Ext.XTemplate',
        'Ext.grid.plugin.CellEditing',
        'Ext.tab.Panel',
        'Ext.tab.Tab'
    ],

    controller: 'mainview',
    viewModel: {
        type: 'mainview'
    },
    itemId: 'mainView',
    layout: 'border',
    defaultListenerScope: true,

    items: [
        {
            xtype: 'panel',
            region: 'center',
            split: true,
            itemId: 'centerPanel',
            header: false,
            title: 'Content',
            layout: {
                type: 'vbox',
                align: 'stretch'
            },
            items: [
                {
                    xtype: 'panel',
                    flex: 1,
                    height: 150,
                    maxHeight: 150,
                    minHeight: 150,
                    bodyPadding: 10,
                    titleCollapse: true,
                    layout: {
                        type: 'hbox',
                        align: 'stretch'
                    },
                    items: [
                        {
                            xtype: 'container',
                            flex: 0.6,
                            layout: {
                                type: 'vbox',
                                align: 'stretch'
                            },
                            items: [
                                {
                                    xtype: 'container',
                                    autoScroll: true,
                                    layout: {
                                        type: 'table',
                                        tdAttrs: {
                                            style: 'padding-right: 10px;'
                                        }
                                    },
                                    items: [
                                        {
                                            xtype: 'combobox',
                                            itemId: 'vonm',
                                            width: 100,
                                            fieldLabel: 'Von',
                                            labelWidth: 30,
                                            value: 1,
                                            allowBlank: false,
                                            allowOnlyWhitespace: false,
                                            enableKeyEvents: true,
                                            selectOnFocus: true,
                                            displayField: 'name',
                                            forceSelection: true,
                                            queryMode: 'local',
                                            store: 'monthStore',
                                            typeAhead: true,
                                            typeAheadDelay: 100,
                                            valueField: 'id'
                                        },
                                        {
                                            xtype: 'textfield',
                                            itemId: 'vony',
                                            width: 60,
                                            hideLabel: true,
                                            labelPad: 0,
                                            labelWidth: 0,
                                            value: 2015
                                        },
                                        {
                                            xtype: 'combobox',
                                            itemId: 'bism',
                                            width: 100,
                                            fieldLabel: 'Von',
                                            labelWidth: 30,
                                            value: 12,
                                            allowBlank: false,
                                            allowOnlyWhitespace: false,
                                            enableKeyEvents: true,
                                            selectOnFocus: true,
                                            displayField: 'name',
                                            forceSelection: true,
                                            queryMode: 'local',
                                            store: 'monthStore',
                                            typeAhead: true,
                                            typeAheadDelay: 100,
                                            valueField: 'id'
                                        },
                                        {
                                            xtype: 'textfield',
                                            itemId: 'bisy',
                                            width: 60,
                                            hideLabel: true,
                                            labelPad: 0,
                                            labelWidth: 0,
                                            value: 2015
                                        },
                                        {
                                            xtype: 'button',
                                            itemId: 'btnReload',
                                            text: 'Yeppers'
                                        }
                                    ]
                                },
                                {
                                    xtype: 'container',
                                    layout: {
                                        type: 'table',
                                        tdAttrs: {
                                            style: 'padding-right: 10px;'
                                        }
                                    },
                                    items: [
                                        {
                                            xtype: 'textfield',
                                            itemId: 'dbgx',
                                            width: 100,
                                            fieldLabel: 'x',
                                            labelWidth: 30,
                                            readOnly: true
                                        },
                                        {
                                            xtype: 'textfield',
                                            itemId: 'dbgy',
                                            width: 100,
                                            fieldLabel: 'y',
                                            labelWidth: 30,
                                            readOnly: true
                                        },
                                        {
                                            xtype: 'button',
                                            text: 'Add',
                                            listeners: {
                                                click: 'onButtonClick'
                                            }
                                        }
                                    ]
                                }
                            ]
                        },
                        {
                            xtype: 'container',
                            flex: 0.4,
                            items: [
                                {
                                    xtype: 'textareafield',
                                    height: '100%',
                                    itemId: 'debugConsole',
                                    width: '100%',
                                    fieldLabel: 'Label',
                                    hideLabel: true,
                                    labelPad: 0,
                                    labelWidth: 0,
                                    readOnly: true,
                                    emptyText: 'Console'
                                }
                            ]
                        }
                    ]
                },
                {
                    xtype: 'gridpanel',
                    flex: 1,
                    height: 150,
                    itemId: 'contentGrid',
                    titleCollapse: false,
                    sortableColumns: false,
                    store: 'rotStore',
                    viewConfig: {
                        listeners: {
                            cellclick: {
                                fn: 'onViewCellClick',
                                scope: 'controller'
                            }
                        }
                    },
                    columns: [
                        {
                            xtype: 'gridcolumn',
                            draggable: false,
                            hidden: true,
                            resizable: false,
                            sortable: false,
                            dataIndex: 'id',
                            hideable: false,
                            locked: true,
                            menuDisabled: true,
                            text: 'Id'
                        },
                        {
                            xtype: 'gridcolumn',
                            hidden: true,
                            dataIndex: 'name',
                            locked: true,
                            text: 'Name'
                        }
                    ],
                    selModel: {
                        selType: 'cellmodel',
                        enableKeyNav: false,
                        listeners: {
                            select: 'onCellModelSelect',
                            focuschange: 'onCellModelFocusChange'
                        }
                    },
                    features: [
                        {
                            ftype: 'grouping',
                            showSummaryRow: true,
                            collapsible: false,
                            groupHeaderTpl: Ext.create('Ext.XTemplate', 
                                '<!--{columnName}: --><!--button class="x-btn x-btn-default-small"><span class="x-btn-inner x-btn-inner-default-small">+</span></button-->',
                                '{children:this.dbgtpl}',
                                {
                                    dbgtpl: function(o) {
                                        //return rot.dbgtpl(o);
                                        //console.log(o[0]);
                                        return o[0].data.rot_group;
                                    }
                                }
                            )
                        }
                    ],
                    plugins: [
                        {
                            ptype: 'cellediting'
                        }
                    ]
                }
            ]
        },
        {
            xtype: 'panel',
            region: 'west',
            split: true,
            hidden: true,
            itemId: 'leftPanel',
            width: 200,
            title: 'Left'
        },
        {
            xtype: 'tabpanel',
            region: 'east',
            split: true,
            itemId: 'rightPanel',
            width: 350,
            title: '',
            activeTab: 0,
            items: [
                {
                    xtype: 'panel',
                    autoScroll: true,
                    title: 'Verfügbar',
                    items: [
                        {
                            xtype: 'gridpanel',
                            itemId: 'gridVerfuegbar',
                            titleCollapse: false,
                            autoLoad: true,
                            store: 'monthempStore',
                            columns: [
                                {
                                    xtype: 'gridcolumn',
                                    renderer: function(value, metaData, record, rowIndex, colIndex, store, view) {
                                        // metaData.tdAttr = ' data-qtip="' + record.data.vorname + " " + record.data.name + '"';
                                        return "<b>" + value + "</b> " + record.data.vorname + " " + record.data.name;
                                    },
                                    width: 200,
                                    dataIndex: 'kuerzel',
                                    text: 'Name'
                                },
                                {
                                    xtype: 'gridcolumn',
                                    renderer: function(value, metaData, record, rowIndex, colIndex, store, view) {
                                        if (record.data.bg != '#FFFFFF')
                                        metaData.tdStyle = " background-color: "+record.data.bg+";";
                                        metaData.style = " color: "+record.data.fg+";";
                                        metaData.tdAttr = ' data-qtip="' + record.data.vorname + " " + record.data.name + '"';

                                        //console.log(metaData);
                                        if (!value) return "<i>" + record.data.comment + "</i>";
                                        return parseInt(value*100);
                                    },
                                    width: 80,
                                    align: 'right',
                                    dataIndex: 'bgrad',
                                    text: '%'
                                },
                                {
                                    xtype: 'gridcolumn',
                                    hidden: true,
                                    dataIndex: 'comment',
                                    text: 'Comment'
                                }
                            ]
                        }
                    ]
                },
                {
                    xtype: 'panel',
                    title: 'Miratbeiter'
                }
            ]
        },
        {
            xtype: 'panel',
            region: 'south',
            split: false,
            height: 150,
            hidden: true,
            itemId: 'footerPanel',
            hideCollapseTool: true,
            title: 'Footer'
        }
    ],

    onButtonClick: function(button, e, eOpts) {

        rot.grid.add_row(button, e, eOpts);
    },

    onCellModelSelect: function(cellmodel, record, row, column, eOpts) {
        //console.log(cellmodel.getPosition());
        //console.log("onCellModelSelect " + row + " " + column);
        //console.log(cellmodel.selection.column.dataIndex);



    },

    onCellModelFocusChange: function(model, oldFocused, newFocused, eOpts) {
        //console.log("onCellModelFocusChange ");
        //console.log(oldFocused);
        //console.log(newFocused);
    }

});