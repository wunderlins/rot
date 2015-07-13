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

rot.model = null;
rot.grid.grid = null;
rot.grid.init = function() {
	rot.grid.grid = Ext.ComponentQuery.query('#contentGrid')[0];
	rot.log("==> rot.grid.init()")
	
	//rot.loadData()
}

rot.grid.column = {
	xtype: 'gridcolumn',
	dataIndex: 'string',
	text: 'Rotation'
}

rot.log = function(str) {
	c = Ext.ComponentQuery.query('#debugConsole')[0];
	c.setValue(c.getValue() + str + "\n");
}

// double declaration to make architects event handling happy
rot.loadData = function(button, e, eOpts) {
	var store = Ext.getStore('rotStore');
	var proxy = store.getProxy();
	rot.log(store)

	// create a new model
	rot.model = Ext.define('calendar.model.rotModel', {
		extend: 'Ext.data.Model',
		itemid: 'rotModel',

		requires: [
			'Ext.data.field.Integer',
			'Ext.data.field.String'
		],

		fields: [
			{
				type: 'int',
				mapping: 0,
				name: 'id'
			},
			{
				type: 'string',
				mapping: 1,
				name: 'name'
			}
		]
	});
	
	
	// create new column list for the grid
	var columns = [
		{
			xtype: 'gridcolumn',
			dataIndex: 'id',
			text: 'Id'
		},
		{
			xtype: 'gridcolumn',
			dataIndex: 'name',
			text: 'Name'
		}	
	]
	
	// apply new model to store
	store.setModel(rot.model);
	
	// apply new store to grid
	rot.grid.grid.reconfigure(store, columns);

	// reload store
	store.load();
	
	return true;
}

/*
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



