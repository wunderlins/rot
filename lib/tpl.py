def btn_ok(onclick=None):
	if onclick == None:
		onclick = ""
	else:
		onclick = " onclick='" + onclick + "' "
	
	return """
	<button type="button" class="btn btn-success" aria-label="OK" """ + onclick + """>
  	<span class="glyphicon glyphicon-ok" aria-hidden="true"></span> <strong>Ok</strong>
	</button>
	"""

def btn_cancel(onclick=None):
	if onclick == None:
		onclick = ""
	else:
		onclick = " onclick='" + onclick + "' "
	
	return """
	<button type="button" class="btn btn-danger" aria-label="Cancel" """ + onclick + """>
  	<span class="glyphicon glyphicon-remove" aria-hidden="true"></span> Cancel
	</button>
	"""

def monat_select(monat, name):
	buffer = ""
	buffer += '<select name="wunsch_' + str(name) + '" class="form-control">'
	buffer += '<option value=""></option>'
	
	buffer += '<option value="1" '
	if monat == 1:
		buffer += 'selected="selected"'
	buffer += '>Jan</option>'
	
	buffer += '<option value="2" '
	if monat == 2:
		buffer += 'selected="selected"'
	buffer += '>Feb</option>'
	
	buffer += '<option value="3" '
	if monat == 3:
		buffer += 'selected="selected"'
	buffer += '>Mar</option>'
	
	buffer += '<option value="4" '
	if monat == 4:
		buffer += 'selected="selected"'
	buffer += '>Apr</option>'
	
	buffer += '<option value="5" '
	if monat == 5:
		buffer += 'selected="selected"'
	buffer += '>Mai</option>'
	
	buffer += '<option value="6" '
	if monat == 6:
		buffer += 'selected="selected"'
	buffer += '>Jun</option>'
	
	buffer += '<option value="7" '
	if monat == 7:
		buffer += 'selected="selected"'
	buffer += '>Jul</option>'
	
	buffer += '<option value="8" '
	if monat == 8:
		buffer += 'selected="selected"'
	buffer += '>Aug</option>'
	
	buffer += '<option value="9" '
	if monat == 9:
		buffer += 'selected="selected"'
	buffer += '>Sep</option>'
	
	buffer += '<option value="10" '
	if monat == 10:
		buffer += 'selected="selected"'
	buffer += '>Okt</option>'
	
	buffer += '<option value="11" '
	if monat == 11:
		buffer += 'selected="selected"'
	buffer += '>Nov</option>'
	
	buffer += '<option value="12" '
	if monat == 12:
		buffer += 'selected="selected"'
	buffer += '>Dez</option>'
	buffer += '</select>'
	return buffer
	
	
def wunsch_prio(prio):
	if prio == 1:
		return '&#xe133;&#xe133;'
	if prio == 2:
		return '&#xe133;'
	if prio == 3:
		return '&#xe082;'
	if prio == 4:
		return '&#xe134;'
	if prio == 5:
		return '&#xe134;&#xe134;'
	return "-"

def wunsch_select_wunsch(rid, wunsch):
	buffer = ""
	buffer += '<select name="wunsch_' + str(rid) + '" class="form-control">'
	buffer += '<option value=""></option>'
	if wunsch["wunsch"] == 1:
		buffer += '<option value="1" selected="selected">Ja</option>'
	else:
		buffer += '<option value="1">Ja</option>'
	if wunsch["wunsch"] == 0:
		buffer += '<option value="0" selected="selected">Nein</option>'
	else:
		buffer += '<option value="0" >Nein</option>'
	if wunsch["wunsch"] == 2:
		buffer += '<option value="2" selected="selected">Gemacht</option>'
	else:
		buffer += '<option value="2">Gemacht</option>'
	buffer += '</select>'
	return buffer

def wunsch_select_prio(rid, wunsch):
	buffer = ""
	buffer += '<select name="prio_' + str(rid) + '" class="prio form-control">'
	buffer += '<option value=""></option>'
	if wunsch["prio"] == 1:
		buffer += '<option value="1" selected="selected">&#xe133;&#xe133;</option>'
	else:
		buffer += '<option value="1">&#xe133;&#xe133;</option>'
	if wunsch["prio"] == 2:
		buffer += '<option value="2" selected="selected"> &#xe133;</option>'
	else:
		buffer += '<option value="2"> &#xe133;</option>'
	if wunsch["prio"] == 3:
		buffer += '<option value="3" selected="selected"> &#xe082;</option>'
	else:
		buffer += '<option value="3"> &#xe082;</option>'
	if wunsch["prio"] == 4:
		buffer += '<option value="4" selected="selected"> &#xe134;</option>'
	else:
		buffer += '<option value="4"> &#xe134;</option>'
	if wunsch["prio"] == 5:
		buffer += '<option value="5" selected="selected">&#xe134;&#xe134;</option>'
	else:
		buffer += '<option value="5">&#xe134;&#xe134;</option>'
	buffer += '</select>'
	return buffer
