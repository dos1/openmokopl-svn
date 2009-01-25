#!/usr/bin/env python
import os,sys


fileName = "/tmp/dial_pido"
procesName = sys.argv[0]
procesName = "["+procesName[:1]+"]"+procesName[1:]
myPid = sys.modules["os"].getpid()
cmd = "ps ax | grep "+str(procesName)+\
	" | grep -v "+str(myPid)
test = os.popen(cmd).read().replace("\n", "")
if test != "":
	f = open(fileName,"w")
	f.write("run\n")
	f.close()
	sys.exit()


from threading import Thread
import threading

import dbus
from dbus.mainloop.glib import DBusGMainLoop

import time
import gobject
import gtk
import gtk.glade

tStart = time.time()
def Deb( name ):
	print "[dial]["+str(time.time()-tStart)+"] "+str(time.ctime())+" ["+str(name)+"]"

def get_image( wTree, obj, icoStock ):
	objWid = wTree.get_widget(obj)
	ico = gtk.Image()
	ico.set_from_stock( icoStock, gtk.ICON_SIZE_BUTTON )
	ico.show()
	objWid.set_image( ico )


__author__="yoyo"
__date__ ="$Jan 19, 2009 4:57:02 PM$"

def destroy_all(widget):
	win.hide()
	gtk.main_quit()

def on_buttonKey_clicked( widget ):
	print "bt:"+str(widget.get_label())
	entry_nr.set_text( entry_nr.get_text()+str(widget.get_label()[0]) )

def on_button_backspace_clicked( widget ):
	entry_nr.set_text( entry_nr.get_text()[0:(len(entry_nr.get_text())-1)] )

def on_button_dial_clicked( widget ):
	gsm_call_iface.Initiate( str(entry_nr.get_text()), 'voice' )
	gtk.main_quit()

if __name__ == "__main__":

	
	DBusGMainLoop(set_as_default=True)
	bus = dbus.SystemBus()
	while 1:
		try:
			gsm_device_obj = bus.get_object( 'org.freesmartphone.ogsmd', '/org/freesmartphone/GSM/Device' )
			gsm_call_iface = dbus.Interface(gsm_device_obj, 'org.freesmartphone.GSM.Call')
			gsm_call_iface.ListCalls()
			Deb("dial gsm_call_iface present")
			break
		except:
			Deb("dial gsm_call_iface not present try in 5sec.")
			time.sleep(5)

	win = gtk.Window()
	gladefile = "dial.glade"
	wTree = gtk.glade.XML(gladefile)
	win = wTree.get_widget('window_dial')
	entry_nr = wTree.get_widget('entry_nr')
	get_image(wTree, "button_dial", gtk.STOCK_APPLY)
	win.set_title("dial")
	dic = { "on_button0_clicked" : on_buttonKey_clicked,
			"on_button1_clicked" : on_buttonKey_clicked,
			"on_button2_clicked" : on_buttonKey_clicked,
			"on_button3_clicked" : on_buttonKey_clicked,
			"on_button4_clicked" : on_buttonKey_clicked,
			"on_button5_clicked" : on_buttonKey_clicked,
			"on_button6_clicked" : on_buttonKey_clicked,
			"on_button7_clicked" : on_buttonKey_clicked,
			"on_button8_clicked" : on_buttonKey_clicked,
			"on_button9_clicked" : on_buttonKey_clicked,
			"on_button_star_clicked" : on_buttonKey_clicked,
			"on_button_hasz_clicked" : on_buttonKey_clicked,
			"on_button_backspace_clicked" : on_button_backspace_clicked,
			"on_button_close_clicked" : destroy_all,
			"on_button_dial_clicked" : on_button_dial_clicked
		}
	wTree.signal_autoconnect(dic)
	#win.connect('destroy', gtk.main_quit)
	win.connect('destroy', destroy_all)

	i = 0
	open(fileName,"w").close()
	while 1:
		s = open(fileName,"r")


		win.show_all()

		Deb("dial dial ready")
		gtk.main()
		Deb("dial dial end")

		while 1:
			r = s.readline()[:-1]
			if str(r) == "run":
				s.close()
				open(fileName,"w").close()
				i = 0
				break
			time.sleep(0.7)



	