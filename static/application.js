$.ajax({
	url: "/personal",
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
