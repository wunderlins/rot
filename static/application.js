function load_personal() {

	$.ajax({
		url: "/personal_data",
		beforeSend: function( xhr ) {
			xhr.overrideMimeType( "text/plain; charset=x-user-defined" );
		}
	}).done(function( data ) {
		if ( console && console.log ) {
			var js = jQuery.parseJSON(data);
			//console.log(js);
				
			// append nodes
			/**
			 <li class="list-group-item">
			 <span class="badge">14</span>
			 Cras justo odio
			 </li>
			**/
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
				//console.log(e.name + " " + e.vorname)
				p.append(n)
			}
		}
	});
}


function init_ta() {
	$('.typeahead').typeahead({
		hint: true,
		highlight: true,
		minLength: 1
	},
	{
		name: 'states',
		displayKey: 'value',
		source: substringMatcher(names.options)
	});
	
	function handleSearch(e, data) {
		if (data)
			document.location.href = "/personal/" + data.pid
		
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
		//.on('typeahead:autocompleted', handleSearch)
		.on('keyup', handleSearch);
}

var _load_handler = [init_ta]
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
    //console.log(matches)
 
    cb(matches);
  };
};

