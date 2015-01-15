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
