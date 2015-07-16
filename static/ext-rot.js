Object.clone = function(obj) {
	if (null == obj || "object" != typeof obj) return obj;
	var copy = obj.constructor();
	for (var attr in obj) {
		if (obj.hasOwnProperty(attr)) copy[attr] = obj[attr];
	}
	return copy;
}

rot = {};
rot.init = function() {
	rot.grid.init();
}

rot.dbgtpl = function(o) {
	console.log(o)
}

rot.grid = {}
rot.grid.meta = null
rot.grid.cellwidth = 50
rot.meta = null

rot.grid.modified = function() {
	
	var updated = []
	
	var store = Ext.getStore('rotStore');
	for (i in store.data.items) {
		var it = store.data.items[i]; 
		if (it.dirty) {
			//console.log(it.data)
			// console.log(it.data.rid)
			//console.log(it.modified)
			//console.log(it)
			
			for (e in it.modified) {
				rec = {
					id: it.data.id,
					rid: it.data.rid,
					ym: e,
					v: it.data[e]
				}
				
				updated[updated.length] = rec
			}
		}
	}
	
	console.log(updated)
}

/*
// hashtable for quick id to kuerzel lookup
rot.kuerzel = []
rot.kuerzelupdate = function(store, records, successful, eOpts) {
	rot.kuerzel = []
	for (e in records) {
		rot.kuerzel[records[e].data.pid] = records[e].data.kuerzel
	}
	//console.log(rot.kuerzel)
}
*/

// FIXME: this event handler migh not be used anymore.
rot.grid.celledit = function(editor, context, eOpts) {
	//console.log(editor)
	//console.log(context)
	//console.log(eOpts)
	
	// aknowledge change
	//console.log(context.record)
	//console.log(context.record.modified)
	ym = ""
	for (e in context.record.modified) {
		ym = e;
		break;
	}
	
	rec = {
		id: context.record.data.id,
		rid: context.record.data.rid,
		ym: ym,
		v: context.record.data[ym]
	}
	//console.log(rec)
	
	// now remove the first element from modified
	mod = {}
	first = true;
	for (e in context.record.modified) {
		if (first) {
			first = false;
			continue;
		}
		
		mod[e] = context.record.modified[e]
	}
	
	//context.record.modified = mod
	
	
	//context.record.modified.shift()
	/*
	delete context.record.modified[rec.ym]
	
	console.log(context.record)
	*/
	
	//context.record.data[context.field] = context.value;
	console.log(context.record)
	//console.log(context.record.data)
	//Ext.getStore('rotStore').sync()
	
	// BUG: using tab hangs the editor.
	
	rot.log("NewV " + context.colIdx + ":" + context.rowIdx + "> " + context.value)
	//rot.grid.modified();
	
	// TODO: fire off an ajax update event

	Ext.Ajax.request({
		url: '../../update_rot',
		method: "get",
		params: rec,
		success: function(response){
			var text = response.responseText;
			result = Ext.decode(text)
			console.log(result);
		}
	});	
}

rot.get = function(selector) {
	return Ext.ComponentQuery.query(selector)[0];
}

rot.error = function(title, message) {
	Ext.MessageBox.alert(title, message);
}


rot.get_meta = function(field, newValue, oldValue) {
	rot.grid.selection = {
		von: {y: null, m: null},
		bis: {y: null, m: null}
	}
	
	// read the time span
	var vonm = parseInt(rot.get("#vonm").getValue())
	var vony = parseInt(rot.get("#vony").getValue())
	var bism = parseInt(rot.get("#bism").getValue())
	var bisy = parseInt(rot.get("#bisy").getValue())
	// rot.log(vonm + "." + vony + " " + bism + "." + bisy)
	
	console.log("field: ")
	console.log(field)
	if (isNaN(vonm) || isNaN(vony) || isNaN(bism) || isNaN(bisy)) {
		// TODO: notify user about error
		field.setValue(oldValue);
		rot.error("Error", "Invalid date value.");
		return false;
	}
	
	vonix = "" + vony;
	bisix = "" + bisy;
	vonix += (vonm < 10) ? "0" + vonm : vonm;
	bisix += (bism < 10) ? "0" + bism : bism;
	
	if (bisix < vonix) {
		// TODO: notify user about error
		field.setValue(oldValue);
		rot.error("Error", "End date must be large than start date.");
		return false;
	}
	
	// make selected parameters globally available
	rot.grid.selection.von.y = vony;
	rot.grid.selection.von.m = vonm;
	rot.grid.selection.bis.y = bisy;
	rot.grid.selection.bis.m = bism;

	Ext.Ajax.request({
		url: '../../get_meta',
		method: "get",
		params: {
			von: vonix,
			bis: bisix
		},
		success: function(response){
			var text = response.responseText;
			//console.log(Ext.decode(text));
			rot.grid.meta = Ext.decode(text).metaData
			
			// convert function stringos into objects
			for (x in rot.grid.meta.columns) {
				var e = rot.grid.meta.columns[x]
				if (!e.columns)
					continue;
				//console.log(e.columns)
				
				//console.log("Columns")
				//console.log(e.columns)
				for (xx in e.columns) {
					var ee = e.columns[xx]
					if (!ee.editor)
						continue
					//if (!ee.editor.renderer)
					//	continue
					//console.log("-- columns")
					//console.log(ee)
					
					//console.log(ee.editor.renderer)
					if (ee.renderer) {
						//if ("rot.grid.cell_renderer" == ee.editor.renderer)
						//	ee.editor.renderer = rot.grid.cell_renderer
						ee.renderer = eval(ee.renderer)
					} 
				}
				/*
				*/
			}
			
			
		}
	});
}

function get_meta() {
	return rot.get_meta();
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

rot.rotStore = {}
rot.rotStore.metaData = null
rot.rotStore.load = function(store, records, successful, eOpts) {
	//console.log(store);
}

rot.rotStore.metaChange = function(store, meta, eOpts) {
	rot.rotStore.metaData = meta;
}


rot.grid.cellIndex = null
rot.grid.rowIndex = null

rot.grid.add_row = function(button, e, eOpts) {
	if (rot.grid.cellIndex === null) {
		rot.log("No selection")
		return;
	}
	
	var store = Ext.getStore('rotStore');
	var proxy = store.getProxy();
	
	// get the current record, clone it, empty id, set new id and append
	var selection = rot.get("#contentGrid").getSelection()
	//console.log(selection)
	
	// copy record, give it a unique id
	var rec = selection[0].copy(++rot.rotStore.metaData.maxid)
	console.log(rec)
	
	// clear all vlaues, increment sort to place it under the cloned record
	for (e in rec.data) {
		if (e.substr(0, 2) == "20") {
			rec.data[e] = ""
		}
		
		if (e == "srt")
			rec.data[e] = "" + (parseInt(rec.data[e]) + 1) // cast to int, increment, cast to str
	}
	
	/*
	// var data = Object.clone(selection[0].data)
	for (e in data) {
		if (e.substr(0, 2) == "20") {
			data[e] = "111"
		}
		
		if (e == "id")
			data[e] = ++rot.rotStore.metaData.maxid;
	}
	//console.log(data)
	var rec = Ext.create("calendar.store.rotStore", data);
	*/
	
	store.addSorted(rec)
	store.sort("srt", "ASC")
	return true;
	
	var store = Ext.getStore('rotStore');
	var proxy = store.getProxy();
	
	var rec = Ext.create("calendar.store.rotStore", {
		id: ++rot.rotStore.metaData.maxid, 
		group_sort: "sort001",
		rot_group: "Viszeral/Urologie/Lunge", 
		name: "sdfsdfdf", 
		description: null, 
		srt: "100000"
	})
	
	store.addSorted(rec)
	store.sort("srt", "ASC")
}

rot.grid.selection_change = function(model, selected, eOpts) {
	if(selected.length) {
		//console.log(model);
		//console.log(selected);
		//console.log(eOpts);

		cellIndex = model.nextSelection.colIdx;
		rowIndex = model.nextSelection.rowIdx;

		rot.grid.cellIndex = cellIndex;
		rot.grid.rowIndex = rowIndex;
		rot.get("#dbgx").setValue(rowIndex);
		rot.get("#dbgy").setValue(cellIndex);

		/*
		rot.log(cellIndex + " " + rowIndex)
		console.log(cellIndex + " " + rowIndex)
		console.log(e)
		console.log(eOpts)
		console.log(tableview)
		console.log(record)
		*/
		//rot.log(cellIndex + " " + rot.grid.selection.von.m)
		selected_date = rot.add_month(cellIndex, rot.grid.selection.von);
		//rot.log(selected_date.y + " " + selected_date.m)

		if (rot.lastym && selected_date.y == rot.lastym.y && selected_date.m == rot.lastym.m)
			return;

		rot.lastym = Object.clone(selected_date);

		// get a reference to the data store and proxy
		var store = Ext.getStore('monthempStore');
		var proxy = store.getProxy();

		proxy.setExtraParam("ym", rot.month_str(selected_date));
		store.load();

	} else {
		/*
		console.log(model);
		console.log(selected);
		console.log(eOpts);
		*/
		;
	}
}

rot.grid.onclick = function(tableview, td, cellIndex, record, tr, rowIndex, e, eOpts) {
	/*
	rot.grid.cellIndex = cellIndex
	rot.grid.rowIndex = rowIndex
	rot.get("#dbgx").setValue(rowIndex);
	rot.get("#dbgy").setValue(cellIndex);
	
	/*
	rot.log(cellIndex + " " + rowIndex)
	console.log(cellIndex + " " + rowIndex)
	console.log(e)
	console.log(eOpts)
	console.log(tableview)
	console.log(record)
	* /
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
	*/
}

rot.grid.ondblclick = function(tableview, td, cellIndex, record, tr, rowIndex, e, eOpts) {
	rot.get("#dbgx").setValue(rowIndex);
	rot.get("#dbgy").setValue(cellIndex);
}

rot.grid.cell_renderer = function(value) {
	//console.log("rot.grid.cell_renderer")
	//return "uuu";
	ret = value;
	try {
		ret = rot.personal[value]
	} catch(err) {
		ret = value;
	}
	
	return ret
}

rot.grid.init = function() {
	
	// set store for combobox month
	//var monthStore = Ext.getStore('monthStore');
	//Ext.ComponentQuery.query('#vonm')[0].setStore(monthStore);
	
	rot.grid.grid = Ext.ComponentQuery.query('#contentGrid')[0];
	rot.log("==> rot.grid.init()")
	
	//rot.loadData()
	rot.get_meta();
}

rot.log = function(str) {
	c = Ext.ComponentQuery.query('#debugConsole')[0];
	c.setValue(c.getValue() + str + "\n");
}

rot.prepare_load = function() {
	console.log("rot.prepare_load")
	/*
	// get a reference to the data store and proxy
	var store = Ext.getStore('rotStore');
	var proxy = store.getProxy();
	
	// create a new model
	rot.model = Ext.define('calendar.model.rotModel', {
		extend: 'Ext.data.Model',
		requires: [
			'Ext.data.field.Integer',
			'Ext.data.field.String'
		],
		
		fields: rot.meta.fields
	});
	
	// apply new model to store
	store.setModel(rot.model);
	
	// apply new store to grid
	rot.grid.grid.reconfigure(store, rot.meta.columns);
	
	// set time range parameters
	proxy.setExtraParam("von", rot.meta.von)
	proxy.setExtraParam("bis", rot.meta.bis)
	*/
}

rot.personal = []
rot.personal_load = function(store, records, successful, eOpts) {
	rot.personal = []
	//console.log(records)
	for (e in records) {
		rot.personal[records[e].data.pid] = records[e].data.kuerzel
	}
}

rot.loadPersonal = function(vonix, bisix) {
	// get a reference to the data store and proxy
	var store = Ext.getStore('assiStore');
	var proxy = store.getProxy();
	
	proxy.setExtraParam("von", vonix)
	proxy.setExtraParam("bis", bisix)
	store.load()
}

// double declaration to make architects event handling happy
rot.loadData = function(button, e, eOpts) {
	console.log("loadData")
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
	rot.loadPersonal(vonix, bisix);
	
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
	
	/*
	// count number of months
	cm = vonm;
	cy = vony;
	months = 0;
	
	
	rot.fields = [
		{type: 'int', mapping: 0, name: 'id'},
		{type: 'string', mapping: 1, name: "rot_group"},
		{type: 'string', mapping: 2, name: 'name'},
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
	*/
	
	
	// create a new model
	/*
	rot.model = Ext.define('calendar.model.rotModel', {
		extend: 'Ext.data.Model',
		requires: [
			'Ext.data.field.Integer',
			'Ext.data.field.String'
		],
		
		fields: rot.grid.meta.fields
	});
	*/
	
	// update fields on our existing model
	var model = proxy.getModel()
	model.fields = rot.grid.meta.fields
	
	
	// create new column list for the grid
	//var columns = rot.columns
	
	// apply new model to store
	//store.setModel(rot.model);
	
	// apply new store to grid
	rot.grid.grid.reconfigure(store, rot.grid.meta.columns);
	
	// set time range parameters
	proxy.setExtraParam("von", vonix)
	proxy.setExtraParam("bis", bisix)
	// reload store
	console.log("Reloading rotStore ...")
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



