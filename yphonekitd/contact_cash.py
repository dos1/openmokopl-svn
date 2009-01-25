#!/usr/bin/env python

import os,sys,time
import sqlite3

tStart = time.time()

__author__="yoyo"
__date__ ="$Jan 21, 2009 11:01:58 PM$"

def Deb( name ):
	print "[contact_cash]  ["+str(name)+"]"


def db_create():
	
	Deb("db_create")
	conn = sqlite3.connect("/tmp/pb_cash.db")
	Deb("db_create conn")
	c = conn.cursor()
	Deb("db_create cursor")
	try:
		c.execute(\
			"""create table pb
				(id int, simid int, name text, nr text) """
			)
	except:
		pass
	Deb("db_create execute")
	conn.commit()
	Deb("db_create commit")
	c.close()
	Deb("db_create close")
	Deb("db_create create done")

def build_cash_db():
	db_create()

def select_item_db( what="*", where="1" ):
	Deb("select_item_db")
	conn = sqlite3.connect("/tmp/pb_cash.db")
	c = conn.cursor()
	t = ()
	c.execute(
		"select "+what+" from pb where "+where,
		t
		)
	for i in c:
		return str(i[0])

def insert_item_db( id, name, nr):
	Deb("insert_item_db")

	test = select_item_db("simid", "nr='"+str(nr)+"' AND simid='"+str(id)+"'")
	if str(test) != str(id):
		Deb("insert_item_db add item ["+str(id)+"] ["+str(name)+"] ["+str(nr)+"]")
		conn = sqlite3.connect("/tmp/pb_cash.db")
		c = conn.cursor()

		c.execute(
			"""
			insert into pb
				values( 0, ?, ?, ? )
			""", ( id, name, nr )
			)
		conn.commit()
		c.close()
	else:
		Deb("insert_item_db item present")

	Deb("insert_item_db done")

if __name__ == "__main__":
	# nr to name
	if sys.argv[1] == "search":	
		sender = "NaN"
		nr_s = str(sys.argv[2])
		try:
			if nr_s[0]=="+":
				phoneNr = nr_s[3:]
			else:
				phoneNr = nr_s

			res = os.popen("cat /tmp/pb_casch | grep \"]##\[\""+str(phoneNr)+"\"]##\[\"" ).read().replace("\n","")
			if res != "":
				row = res.split("]##[")
				sender = row[3]
		except:
			print "NaN"

		print sender
	# cash
	if sys.argv[1] == "casch":
		Deb("__name__ action cash")
		import dbus
		from dbus.mainloop.glib import DBusGMainLoop


		DBusGMainLoop(set_as_default=True)
		bus = dbus.SystemBus()		

		while 1:
			try:
				gsm_device_obj = bus.get_object( 'org.freesmartphone.ogsmd', '/org/freesmartphone/GSM/Device' )
				gsm_sim_iface = dbus.Interface(gsm_device_obj, 'org.freesmartphone.GSM.SIM')
				sim_pb = gsm_sim_iface.RetrievePhonebook('contacts')
				break
			except:
				time.sleep(4)


		try:
			build_cash_db()

			Deb("__name__ making primitive phonebookcash file open")
			f = open("/tmp/pb_casch", "w")
			if f:
				for i in sim_pb:
					if i[2]=="+":
						i[2] = i[2][3:]
					f.write( "]##["+str(i[2])+"]##["+str(i[0])+"]##["+str(i[1])+"]##[\n" )
					insert_item_db(int(i[0]), str(i[1]), str(i[2]))
				Deb("__name__ making primitive phonebookcash close")
				f.close()

			select_item_db("nr", "nr='501831583'" )
		except:
			Deb("__name__ making primitive phonebookcash action cash error")

	

