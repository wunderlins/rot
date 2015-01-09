#!/usr/bin/env python
# coding: utf8

import ldap, sys

class aduser(object): 
	def __init__(self):
		# Dies ist der Konstruktor
		self.__User = ""
		self.__Password = ""
		self.__Code = 0
		self.__Vorname = ""
		self.__Nachname = ""
		self.__Email = ""
		self.__Cn = ""
		self.__DistinguishedName = ""
		self.__Error = ""

	def __del__(self): 
	# Dies ist der Destruktor
		pass
	# Hier sind die Methoden
	# Getter Methoden
	def user(self):
		return self.__User
	def code(self):
		return self.__Code
	def vorname(self):
		return self.__Vorname
	def nachname(self):
		return self.__Nachname
	def email(self):
		return self.__Email
	def cn(self):
		return self.__Cn
	def distinguishedName(self):
		return self.__DistinguishedName
	def error(self):
		return self.__Error
		
	# Setter Methoden
	def setUser(self, user):
		if (user[:3] == "ms\\"):
			self.__User = user[3:].lower()
		else:
			self.__User = user.lower()
	
	def setPassword(self, password):
		self.__Password = password
	
	# Property Attribute
	User = property(user, setUser)
	Password = property(None, setPassword)
	Vorname = property(vorname)
	Nachname = property(nachname)
	Email = property(email)
	Cn = property(cn)
	DistinguishedName = property(distinguishedName)
	Error = property(error)
	Code = property(code)
	# Alle weiteren Methoden


	# Richtigen CN herausfinden
	def checkcn(self):
		#code 0 = Alles i.O.
		#code 1 = Benutzername konnte nicht ermittelt werden
		try:
			l = ldap.open("ms.uhbs.ch")
			l.protocol_version = ldap.VERSION3
			username = "cn=mttools medizintechnik,ou=Generic,ou=Users,ou=MTInf,ou=USB,dc=ms,dc=uhbs,dc=ch"
			password = "medtechscan"
			l.simple_bind_s(username, password)
		
		except ldap.LDAPError, e:
			self.__Error = e
			self.__Code = 1
			return False
		
		baseDN = "ou=Users,ou=USB,dc=ms,dc=uhbs,dc=ch"
		searchScope = ldap.SCOPE_SUBTREE
		retrieveAttributes = None 
		searchFilter = "mailNickname=" + self.__User

		try:
			ldap_result_id = l.search(baseDN, searchScope, searchFilter, retrieveAttributes)
			result_set = []
			while 1:
				result_type, result_data = l.result(ldap_result_id, 0)
				if (result_data == []):
					break
				else: 
					if result_type == ldap.RES_SEARCH_ENTRY:
						result_set.append(result_data)	
			
			try:
				if 'cn' in result_set[0][0][1] and 'distinguishedName' in result_set[0][0][1]:
					self.__Cn = result_set[0][0][1]['cn'][0].replace(",","\,")
					self.__DistinguishedName = result_set[0][0][1]['distinguishedName'][0]
				else:
					return False
			except:
				return False
		
		except ldap.LDAPError, e:
			self.__Error = e
			self.__Code = 2
			return False


	def authenticate(self):
		#code 0 = Alles i.O.
		#code 1 = Benutzername oder Passwort falsch
		#code 2 = Benutzer hat zu wenig Rechte.
		
		try:
			l = ldap.open("ms.uhbs.ch")
			l.protocol_version = ldap.VERSION3
			#username = "cn=" + self.__Cn +",ou=Users,ou=USB,dc=ms,dc=uhbs,dc=ch"
			username = self.__DistinguishedName
			l.simple_bind_s(username, self.__Password)
			
		except ldap.LDAPError, e:
			self.__Error = e
			self.__Code = 1
			return False
		
		baseDN = "ou=Users,ou=USB,dc=ms,dc=uhbs,dc=ch"
		searchScope = ldap.SCOPE_SUBTREE
		retrieveAttributes = None 
		searchFilter = "mailNickname=" + self.__User

		try:
			ldap_result_id = l.search(baseDN, searchScope, searchFilter, retrieveAttributes)
			result_set = []
			while 1:
				result_type, result_data = l.result(ldap_result_id, 0)
				if (result_data == []):
					break
				else: 
					if result_type == ldap.RES_SEARCH_ENTRY:
						result_set.append(result_data)	
			
			if 'givenName' in result_set[0][0][1]:
				self.__Vorname = result_set[0][0][1]['givenName'][0]
			
			if 'sn' in result_set[0][0][1]:
				self.__Nachname = result_set[0][0][1]['sn'][0]
			
			if 'mail' in result_set[0][0][1]:
				self.__Email = result_set[0][0][1]['mail'][0]
			
			return True
		
		except ldap.LDAPError, e:
			self.__Error = e
			self.__Code = 2
			return False

if __name__ == "__main__":
	k = aduser()
	k.User= "muana"
	k.Password= "anaana"
	k.checkcn()
	if k.authenticate():
		sys.exit(0)
	else:
		print k.Error
		sys.exit(1)
	









	
