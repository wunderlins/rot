#!/usr/bin/env python
# -*- coding: utf8 -*-

import ldap, sys #, json

class usbauth(object):
	
	@property
	def lastobj(self):
		return self.__lastobj
	
	# configuration
	baseauth = {
		"dn": "CN=MUANA,OU=GenericMove,OU=Users,OU=USB,DC=ms,DC=uhbs,DC=ch",
		"pw": "anaana"
	}
	baseDN = "ou=USB,dc=ms,dc=uhbs,dc=ch"
	search_property = "sAMAccountName"
	host = "ms.uhbs.ch"
	
	def __init__(self):
		self.__conn = None
		self.__lastobj = None
		
		# open an ldap connection for searching 
		self.__conn = ldap.open(self.host)
		self.__conn.protocol_version = ldap.VERSION3
		self.__conn.simple_bind_s(self.baseauth["dn"], self.baseauth["pw"])

	def auth(self, username, pw):
		""" check password, retruns True on success """
		try:
			userdn = self.lookup(username)
			if not userdn:
				return userdn
			
			l = ldap.open(self.host)
			l.protocol_version = ldap.VERSION3
			l.simple_bind_s(userdn, pw)
			
		except ldap.LDAPError, e:
			return None # e.message["desc"]
		
		return True
	
	def lookup(self, username):
		""" returns the DN of an object with the sAMAccountName == username 
		
		returns the DN as String or None if not found, False on error
		"""
		
		self.__lastobj = None
		ldap_result_id = self.__conn.search(self.baseDN, 
		                                    ldap.SCOPE_SUBTREE, 
		                                    self.search_property+"="+username, 
		                                    None)
		result_type, result_data = self.__conn.result(ldap_result_id, 0)
		#print result_type, result_data
		
		if (result_type != 100):
			return False
		
		#print result_type
		try:
			self.__lastobj = result_data[0]
			#print self.__lastobj
			return self.__lastobj[0]
		except:
			return None
	
	def info(self, obj):
		""" Display data of a user
		
		do a self.lookup first
		
		"""
		ret = {
			"dn" : None,
			"username": None,
			"phone": None,
			"email": None,
			"firstname": None,
			"lastname": None,
			"idmid": None,
			"emplyeeNumber": None
		}
		
		try: ret["dn"] = obj[0]; 
		except: pass
		try: ret["username"] = obj[1][self.search_property][0]; 
		except: pass
		try: 
			ret["phone"] = obj[1]["telephoneNumber"][0];
			if obj[1]["otherTelephone"][0] != "":
				ret["phone"] = obj[1]["otherTelephone"][0];
		
		except: pass
		try: ret["email"] = obj[1]["mail"][0]; 
		except: pass
		try: ret["firstname"] = obj[1]["givenName"][0]; 
		except: pass
		try: ret["lastname"] = obj[1]["sn"][0]; 
		except: pass
		try: ret["idmid"] = int(obj[1]["employeeID"][0]); 
		except: pass
		try: ret["emplyeeNumber"] = int(obj[1]["employeeNumber"][0]); 
		except: pass
		
		return ret
	
	@staticmethod
	def main(username, password):
		""" main function """
		
		try:
			a = usbauth()
		except ldap.LDAPError, e:
			print "Failed to connect to ldap, with message: %s" % (e.message["desc"])
			return False
		ret = a.auth(username, password)
		if ret != True:
			return ret
		
		return a.info(a.__lastobj)

def check(username, pw):
	return usbauth.main(username, pw)

def lookup(username):
	a = usbauth()
	obj = a.lookup(username)
	if (obj):
		return a.info(a.lastobj)
	else:
		return None
	
if __name__ == "__main__":
	usage = """Usage: auth.py <username> [password]
	
When only a username is provided, then we do a lookup of the user via ldap.

If username and password is provided, we do an authentication.

Exit code 0 means success, 1 means not found, 2 means wrong password. 127
means argument error.
"""
	# check how many arguments we've got.	
	if len(sys.argv) == 2:
		emp = lookup(sys.argv[1])
		if (emp == None):
			sys.exit(1)
		
		print emp
		sys.exit(0)
		
	elif len(sys.argv) == 3:
		emp = check(sys.argv[1], sys.argv[2])
		#print emp
		if (not emp):
			#print emp
			if emp == None:
				sys.stderr.write("Failed to authenticate\n")
				sys.exit(2)
			else:
				sys.stderr.write("User not found\n")
				sys.exit(1)
		
		print emp
		sys.exit(0)
		
	else:
		print usage
		sys.exit(127)
	
	# authenticate a user
	#emp = check("muana", "anaana")

