import os
import cgi
import urllib

def get_get_vars():
	obj = {}
	listo = os.environ['QUERY_STRING'].split('&')
	if listo[0] == '':
		return {}
	for pair in listo:
		t = pair.split('=')
		if t[0] == '':
			return {}
		obj[t[0]] = urllib.unquote(t[1])
	return obj
 
def get_post_vars():
	"""Some of this code was taken from webob"""
	if os.environ['REQUEST_METHOD'] != 'POST':
		return {}
 
	fs  = cgi.FieldStorage(keep_blank_values=True)
	obj = {}
	if fs.list:
		# fs.list can be None when there's nothing to parse
		for field in fs.list:
			if field.filename:
				obj[field.name] = urllib.unquote(field)
			else:
				obj[field.name] = urllib.unquote(field.value)
	return obj