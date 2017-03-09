app = {
	log: function(txt) {
		console.log(txt)
	},
	byid: function(id) {
		return document.getElementById(id)
	}
}


function load_personal() {

	$.ajax({
		url: "/personal_data"
		/* ,
		beforeSend: function( xhr ) {
			xhr.overrideMimeType( "text/plain; charset=x-user-defined" );
		} */
	}).done(function( data ) {
		var js = jQuery.parseJSON(data);
		//app.log(js);
			
		// append nodes
		p = $("#users")
		for(i=0; i<js.length; i++) {
			e = js[i]
			n = document.createElement("li");
			b = document.createElement("span");
			b.setAttribute("class", "badge")
			b.appendChild(document.createTextNode(e.kuerzel))
			n.appendChild(b);
			n.setAttribute("class", "list-group-item");
			n.appendChild(document.createTextNode(e.name + " " + e.vorname + " " + e.pid));
			//app.log(e.name + " " + e.vorname)
			p.append(n)
		}
	});
}


function init_ta() {
	$('.typeahead').typeahead({
		hint: false,
		highlight: true,
		minLength: 1
	},
	{
		name: 'states',
		displayKey: 'value',
		source: substringMatcher(names.options)
	});
	
	pid = null
	
	function handleSearch(e, data) {
		/*
		if (e.type == "keyup" && (e.keyCode == 13 || e.keyCode == 10)) {
			document.location.href = "/personal/" + data.pid
		}
		*/
		
		if (data)
			document.location.href = "personal/" + data.pid
	}
	
	function autocomplete(e, data) {
		app.log(data)
	
		//pid = data.pid
		//alert(pid)
		/*
		if (e.type == "keyup" && (e.keyCode == 13 || e.keyCode == 10)) {
			selectMa()
		} else if (e.type != "keyup") {
			selectMa()
		}
		*/
	}
	
	$('.typeahead')
		.on('typeahead:selected', handleSearch)
		//.on('typeahead:autocompleted', autocomplete)
		.on('keyup', handleSearch);
}


function init_datepicker() {
	options = {
		pickTime: false,
		format: "DD.MM.YYYY"
		/* , defaultDate: new Date() */
	}
	
	$('.date').datetimepicker(options);
	
	/*
  $(".date").on("dp.change", function(e) {
		//submit_dates()
  });		
	*/
	
}

var _load_handler = [init_ta, init_datepicker]
function add_load_handler(handler) {
	_load_handler.push(handler);
}

var substringMatcher = function(strs) {
  return function findMatches(q, cb) {
    var matches, substrRegex;
 
    // an array that will be populated with substring matches
    matches = [];
 
    // regex used to determine if a string contains the substring `q`
    substrRegex = new RegExp(q, 'i');
 
    // iterate through the pool of strings and for any string that
    // contains the substring `q`, add it to the `matches` array
    $.each(strs, function(i, str) {
      if (substrRegex.test(str.str)) {
        // the typeahead jQuery plugin expects suggestions to a
        // JavaScript object, refer to typeahead docs for more info
        matches.push({ value: str.str, pid: str.pid });
      }
    });
    //app.log(matches)
 
    cb(matches);
  };
};


var notes = {
	setValue: function(val) {
		var wysihtml5Editor = $("#comment").data("wysihtml5").editor;
		//wysihtml5Editor.composer.commands.exec("bold");
		wysihtml5Editor.setValue(val)
	},
	
	getEditor: function() {
		return $("#comment").data("wysihtml5").editor;
	},
	
	focus: function(o) {
		app.log("Focus")
		$("#fake-editor").css("display", "none")
		$("#real-editor").css("display", "block")
		//$(".wysihtml5-sandbox").focus();
		
		// make sure the editor has the focus
		$(".wysihtml5-sandbox")[0].contentWindow.document.getElementsByTagName("body")[0].focus()
		//app.log($(".wysihtml5-sandbox")[0].contentWindow.document)
		
		//alert("Focus")
		//$(".wysihtml5-toolbar").css("display", "block");
		//$('#notiz_controls').css("display", "block");
		//$('#comment').css("height", "7em")
		//$('iframe').css("height", "7em")
		//$("#comment").attr("rows", 5);
		
		//notes.getEditor().composer.commands.exec("insertHTML", "")
		
		return true
	},
	
	collapse: function(o) {
		app.log("collapse")
		$("#fake-editor").css("display", "block")
		$("#real-editor").css("display", "none")
		
		//$(".wysihtml5-toolbar").css("display", "none");
		/*
		$('#notiz_controls').css("display", "none");
		$("#comment").attr("rows", 1);
		*/
		
		//$("#comment").html("");
		notes.setValue("");
		$("#note").attr("action", "rotnote/0")
	},
	
	submit: function() {
		// post a jason record, default:
		dt = null
		if ($('#due_input', '#note').val())
			dt = parseInt($('#due').data("DateTimePicker").getDate().format("X"))
		app.log(dt)
		//t = parseInt($('input[name=type]:checked', '#note').val())
		//var t = parseInt($('input[name=type]').eq(1).addClass('active').val())
		
		// get selected group button
		var t = 0;
		$('#note_type .active').each(function(){
			t = $(this).children()[0].getAttribute("value")
		}); 
		
		if (isNaN(t))
			t = 0;
		t = parseInt(t);
		
		tags = $("#notetag").tagit("assignedTags")
		payload = {
			pid: app.selected_pid,
			comment: $('#comment', '#note').val(),
			type: t,
			due: dt,
			action: "insert",
			tags: tags.join(",")
		}
		
		app.log(payload);
		
		act = $("#note").attr("action")
		if (act != "rotnote/0") {
			payload.action = "update";
		}
		
		app.log($("#note").attr("action"))
		app.log(payload)
		
		$.ajax({
			url: act,
			type: "POST",
			//contentType: "application/json; charset=utf-8",
			//dataType: "json",
			//data: escape("payload="+JSON.stringify(payload))
			data: payload
			/* ,
			beforeSend: function( xhr ) {
				xhr.overrideMimeType( "text/plain; charset=x-user-defined" );
			} */
		}).done(function(data) {
			if (data.success) {
				$('#comment', '#note').html("")
				$('#due_input', '#note').val(null)
				
				document.location.href = document.location.href
			} else {
				alert("Error: " + data.error + "\n\nData could not be saved.")
			}
		})
		.fail(function(data) {
			alert("Failed to communicate with Server")
		})
	},
	
	delete: function(id) {
		
		if (!confirm("Wirklich löschen?"))
			return true;
		
		$.ajax({
			url: "rotnote/"+id,
			type: "POST",
			data: {action: "delete"}
		}).done(function(data) {
			if (data.success) {
				//app.log(data)
				$("#note_"+data.id).remove();
			} else {
				alert("Error: " + data.error + "\n\nData could not be deleted.")
			}
		})
		.fail(function(data) {
			alert("Failed to communicate with Server")
		})
	},
	
	get: function(id) {
		$.ajax({
			url: "rotnote/"+id,
			type: "GET"
		}).done(function(data) {
			if (data.success) {
				app.log(data)
				notes.focus({})
				//$("#comment").val(data.data.comment)
				
				/*
				var wysihtml5Editor = $("#comment").data("wysihtml5").editor;
				//wysihtml5Editor.composer.commands.exec("bold");
				wysihtml5Editor.setValue(data.data.comment)
				*/
				notes.setValue(data.data.comment);
				
				if (data.data.bis)
					$('#due_input', '#note').val(data.data.bis)
				else
					$('#due_input', '#note').val(null)
				if (data.data.type == 2)
					$('#duedate').css('display', 'block')
				else
					$('#duedate').css('display', 'none')
				app.log(data.data.bis)
				
				$("#note").attr("action", "rotnote/" + data.data.id)
				$('input:radio[name=type]').attr('checked', false);
				$(".typecheck").removeClass("active")
				id = "#type_btn_"+data.data.type
				$(id).addClass("active")
				$('input:radio[name=type]').filter('[value='+data.data.type+']').attr('checked', true);
				//app.log(data.data.id)
				//$("#note_"+data.id).remove();
				
				// setup tags
				//$("#notetag").empty()
				$("#notetag").tagit("removeAll");
				for(e in data.data.tags)
					$("#notetag").tagit("createTag", data.data.tags[e]);
				
			} else {
				alert("Error: " + data.error + "\n\nData could not be deleted.")
			}
		})
		.fail(function(data) {
			alert("Failed to communicate with Server")
		})
	}
}
