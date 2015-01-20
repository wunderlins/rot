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
		return '&#xe134;'
	return "-"

def wunsch_select_wunsch(rid, wunsch):
	buffer = ""
	buffer += '<select name="wunsch_' + str(rid) + '">'
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
	buffer += '<select name="prio_' + str(rid) + '" class="prio">'
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
