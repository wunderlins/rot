Object.clone = function(obj) {
	if (null == obj || "object" != typeof obj) return obj;
	var copy = obj.constructor();
	for (var attr in obj) {
		if (obj.hasOwnProperty(attr)) copy[attr] = obj[attr];
	}
	return copy;
}

rot = {};
rot.grid = {}
rot.grid.cellwidth = 50

rot.get = function(selector) {
	return Ext.ComponentQuery.query(selector)[0];
}

rot.grid.selection = {
	von: {y: null, m: null},
	bis: {y: null, m: null}
};

rot.add_month = function(months, ym) {
	ret = Object.clone(ym)
	for (i=0; i<months; i++) {
		ret.m++
		if (ret.m == 13) {
			ret.m = 1
			ret.y++
		}
	}
	
	return ret;
}

rot.month_str = function(ym) {
	var buffer = "" + ym.y
	if (ym.m < 10)
		buffer += "0"
	buffer += ym.m
	
	return buffer
}

rot.model = null;
rot.grid.grid = null;
rot.lastym = null;

rot.grid.onclick = function(tableview, td, cellIndex, record, tr, rowIndex, e, eOpts) {
	
	//rot.log(cellIndex + " " + rot.grid.selection.von.m)
	selected_date = rot.add_month(cellIndex, rot.grid.selection.von)
	//rot.log(selected_date.y + " " + selected_date.m)
	
	if (rot.lastym && selected_date.y == rot.lastym.y && selected_date.m == rot.lastym.m)
		return true;
	
	rot.lastym = Object.clone(selected_date)
	
	// get a reference to the data store and proxy
	var store = Ext.getStore('monthempStore');
	var proxy = store.getProxy();
	
	proxy.setExtraParam("ym", rot.month_str(selected_date))
	store.load()
	
}

rot.grid.ondblclick = function(tableview, td, cellIndex, record, tr, rowIndex, e, eOpts) {
	rot.get("#dbgx").setValue(rowIndex);
	rot.get("#dbgy").setValue(cellIndex);
}

rot.grid.init = function() {
	
	// set store for combobox month
	//var monthStore = Ext.getStore('monthStore');
	//Ext.ComponentQuery.query('#vonm')[0].setStore(monthStore);
	
	rot.grid.grid = Ext.ComponentQuery.query('#contentGrid')[0];
	rot.log("==> rot.grid.init()")
	
	//rot.loadData()
}

rot.log = function(str) {
	c = Ext.ComponentQuery.query('#debugConsole')[0];
	c.setValue(c.getValue() + str + "\n");
}

// double declaration to make architects event handling happy
rot.loadData = function(button, e, eOpts) {
	
	rot.grid.selection = {
		von: {y: null, m: null},
		bis: {y: null, m: null}
	}

	// get a reference to the data store and proxy
	var store = Ext.getStore('rotStore');
	var proxy = store.getProxy();
	//rot.log(store)
	
	// read the time span
	var vonm = parseInt(rot.get("#vonm").getValue())
	var vony = parseInt(rot.get("#vony").getValue())
	var bism = parseInt(rot.get("#bism").getValue())
	var bisy = parseInt(rot.get("#bisy").getValue())
	rot.log(vonm + "." + vony + " " + bism + "." + bisy)
	
	if (isNaN(vonm) || isNaN(vony) || isNaN(bism) || isNaN(bisy)) {
		// TODO: notify user about error
		rot.log("Input format error in date")
		return false;
	}
	
	vonix = "" + vony;
	bisix = "" + bisy;
	vonix += (vonm < 10) ? "0" + vonm : vonm;
	bisix += (bism < 10) ? "0" + bism : bism;
	rot.log("ix: " + vonix + " - " + bisix)
	
	if (bisix < vonix) {
		// TODO: notify user about error
		rot.log("End date must be large than start date")
		return false;
	}
	
	// make selected parameters globally available
	rot.grid.selection.von.y = vony;
	rot.grid.selection.von.m = vonm;
	rot.grid.selection.bis.y = bisy;
	rot.grid.selection.bis.m = bism;
	
	// count number of months
	cm = vonm;
	cy = vony;
	months = 0;
	
	
	rot.fields = [
		{type: 'int', mapping: 0, name: 'id'},
		{type: 'string', mapping: 1, name: 'name'},
		{type: 'string', mapping: 2, name: "rot_group"},
	]
	
	rot.columns =  [
		{
			xtype: 'gridcolumn', 
			hidden: true,
			text: 'Id', 
			dataIndex: 'id', 
			width: 40, 
			locked: true
		},{
			xtype: 'gridcolumn', 
			text: "rot_group", 
			dataIndex: "rot_group", 
			width: rot.grid.cellwidth,
			draggable: false,
			resizable: false,
			hideable: false,
			menuDisabled: true,
			sortable: false,
			hidden: true,
			locked: true
		},{
			xtype: 'gridcolumn', 
			text: 'Name', 
			dataIndex: 'name', 
			width: rot.grid.cellwidth, 
			width: 150,
			locked: true
		},
	]

	rot.columns[rot.columns.length] = {text: cy, columns: [], menuDisabled: true}
	colptr = rot.columns[rot.columns.length-1]
	
	while (true) {
		months++;
		
		// add row
		var n = "" + cy;
		n += (cm < 10) ? "0" + cm : cm;
		
		rot.fields[rot.fields.length] = {type: 'int', mapping: months+2, name: n}
		colptr.columns[colptr.columns.length] = {
			xtype: 'gridcolumn', 
			text: cm, 
			dataIndex: n, 
			width: rot.grid.cellwidth,
			draggable: false,
			resizable: false,
			hideable: false,
			locked: true,
			menuDisabled: true,
			sortable: false
		}
		
		cm++;
		if (cm == 13) {
			cm = 1;
			cy++;
			rot.columns[rot.columns.length] = {text: cy, columns: [], menuDisabled: true}
			colptr = rot.columns[rot.columns.length-1]
		}
		
		if (cm == bism && cy == bisy)
			break;
	}
	
	months++;
	var n = "" + cy;
	n += (cm < 10) ? "0" + cm : cm;
	
	// add last month
	rot.fields[rot.fields.length] = {type: 'int', mapping: months+3, name: n}
	colptr.columns[colptr.columns.length] = {
		xtype: 'gridcolumn', 
		text: cm, 
		dataIndex: n, 
		width: rot.grid.cellwidth,
		draggable: false,
		resizable: false,
		hideable: false,
		menuDisabled: true,
		sortable: false
	}
	
	rot.log("Months: " + months)
	
	
	// create a new model
	rot.model = Ext.define('calendar.model.rotModel', {
		extend: 'Ext.data.Model',
		requires: [
			'Ext.data.field.Integer',
			'Ext.data.field.String'
		],
		
		fields: rot.fields
	});
	
	
	// create new column list for the grid
	var columns = rot.columns
	
	// apply new model to store
	store.setModel(rot.model);
	
	// apply new store to grid
	rot.grid.grid.reconfigure(store, columns);

	// reload store
	store.load();
	
	return true;
}


/*
Ext.define('calendar.model.monthModel', {
    extend: 'Ext.data.Model',

    requires: [
        'Ext.data.field.Integer',
        'Ext.data.field.String'
    ],

    fields: [
        {
            type: 'int',
            name: 'id'
        },
        {
            type: 'string',
            name: 'name'
        }
    ]
});

Ext.define('calendar.store.monthStore', {
    extend: 'Ext.data.Store',

    requires: [
        'calendar.model.monthModel'
    ],

    constructor: function(cfg) {
        var me = this;
        cfg = cfg || {};
        me.callParent([Ext.apply({
            storeId: 'monthStore',
            autoLoad: true,
            model: 'calendar.model.monthModel',
            reader: {
                type: 'json',
                rootProperty: 'root'
            },
            data: {"root": [
                {
                    id: 1,
                    name: 'Jan'
                },
                {
                    id: 2,
                    name: 'Feb'
                },
                {
                    id: 3,
                    name: 'Mar'
                },
                {
                    id: 4,
                    name: 'Apr'
                },
                {
                    id: 5,
                    name: 'Mai'
                },
                {
                    id: 6,
                    name: 'Jun'
                },
                {
                    id: 7,
                    name: 'Jul'
                },
                {
                    id: 8,
                    name: 'Aug'
                },
                {
                    id: 9,
                    name: 'Sep'
                },
                {
                    id: 10,
                    name: 'Nov'
                },
                {
                    id: 11,
                    name: 'Oct'
                },
                {
                    id: 12,
                    name: 'Dez'
                }
            ]
        }}, cfg)]);
    }
});


*/


/*
rot.grid.column = {
	xtype: 'gridcolumn',
	dataIndex: 'string',
	text: 'Rotation'
}

rot.loadData = function() {
	var store = Ext.getStore('rotStore');
	var proxy = store.getProxy();
	rot.log(store)
	
	var start = [2015, 1];
	var count = 12;
	
	var fields = []
	var cols = []
	
	var y = start[0]
	var m = start[1]
	for (i=0; i>=count; i++) {
		mm = (m < 10) ? "0"+m : m;
		yyyymm = "" + y + mm
		ix = "d"+yyyymm
		fields[fields.length] = {name: ix,  type: 'int', 'mapping' : i};
	
		var o = Object.clone(rot.grid.column);
		o.width = 90;
		o.text = ix;
		o.dataIndex = ix;
		cols[cols.length] = o;
		
		if (m == 12) {
			m = 1;
			y++;
		} else {
			m++;
		}
	}
	
	console.log(fields)
	console.log(cols)
	// create a data model
	rot.model = Ext.define('rot.view.gridmodel', {
		extend: 'Ext.data.Model',
		fields: fields,
		itemId: "rotModel"
	});
	console.log(rot.model)
	
	//proxy.setExtraParam("dt_from", dt_from.getSubmitData())
	//proxy.setExtraParam("dt_to",   dt_to.getSubmitData())
	store.setModel(rot.model);
	
	rot.grid.grid.reconfigure(store, cols);
	//proxy.read(operation)
	//store.load();
}
*/

/*
eint.loadData = function() {
	var store = Ext.getStore('StoreShifts');
	var proxy = store.getProxy()
	
	// read dates
	dt_from = Ext.ComponentQuery.query('[itemId=dt_from]')[0]
	dt_to   = Ext.ComponentQuery.query('[itemId=dt_to]')[0]
	if (!dt_from.getValue() || !dt_to.getValue()) {
		alert("Bitte wählen Sie ein Von und Bis Datum aus.")
		return true;
	}
	
	//console.log(dt_from.getValue())
	//console.log(dt_to.getValue())
	
	// calculate num of days inbetween
	days = eint.diff_days(dt_from.getValue(), dt_to.getValue());
	//console.log(days)
	
	// create columns
	var cols = []
	var grid = Ext.ComponentQuery.query('[itemId=plangrid]')[0];
	eint.grid = Ext.ComponentQuery.query('[itemId=plangrid]')[0];
	
	var o = Object.clone(eint.column);
	o.width = 90;
	o.cls = '';
	o.text = "";
	o.dataIndex = "dt";
	o.locked = true;
	o.renderer = eint.cellRenderer
	cols[cols.length] = o;
	
	fields = [
		{name: 'dt',  type: 'string', 'mapping': 0}
	]
	
	i=0;
	for (; i<eint.employees.length; i++) {
		var o = Object.clone(eint.column);
		name = "[---] ";
		if (eint.employees[i][3])
			//name = "[" + eint.employees[i][3] + "] ";
			name = eint.employees[i][3];
		o.text =  name; // + eint.employees[i][2] + " " + eint.employees[i][1];
		o.dataIndex = eint.employees[i][0];
		o.renderer = eint.cellRenderer
		cols[cols.length] = o;
		
		fields[fields.length] = {name: eint.employees[i][0],  type: 'string', 'mapping' : i+1};
	}
	fields[fields.length] = {name: "id",  type: 'int', 'mapping' : i+1};
	
	// create a data model
	var model = Ext.define('speinteilung.view.gridmodel', {
		extend: 'Ext.data.Model',
		fields: fields,
	});

	
	proxy.setExtraParam("dt_from", dt_from.getSubmitData())
	proxy.setExtraParam("dt_to",   dt_to.getSubmitData())
	store.setModel(model);
	
	grid.reconfigure(store, cols);
	//proxy.read(operation)
	store.load();
}
*/



