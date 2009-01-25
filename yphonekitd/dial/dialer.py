#!/usr/bin/env python

from threading import Thread
import threading

import dbus
from dbus.mainloop.glib import DBusGMainLoop

import time,os
import gobject
import gtk
import gtk.glade

def Deb( name ):
	print "[dialer] "+str(time.ctime())+" ["+str(name)+"]"

__author__="yoyo"
__date__ ="$Jan 19, 2009 4:57:02 PM$"


def get_image( wTree, obj, icoStock ):
	objWid = wTree.get_widget(obj)
	ico = gtk.Image()
	ico.set_from_stock( icoStock, gtk.ICON_SIZE_BUTTON )
	ico.show()
	objWid.set_image( ico )



class My_handler_call(threading.Thread):
	def __init__(self, gsm_call_iface):
		Thread.__init__(self)
		self.gsm_call_iface = gsm_call_iface
		self.win_init_incoming()
		self.win_init_active()
		self.statusDialer = "redy"

	def on_button_pickUp_clicked(self, widget):
		Deb("My_handler_call on_button_pickUp_clicked")
		self.gsm_call_iface.Activate( 1 )
		self.win_incoming.hide()

		

	def on_button_putDown_clicked(self, widget):
		Deb("My_handler_call on_button_putDown_clicked")
		self.gsm_call_iface.Release( 1 )
		self.win_incoming.hide()
		self.win_active.hide()
		self.statusDialer = "redy"

	def win_init_incoming(self):
		self.win_incoming = gtk.Window()

		gladefile = "dialog_incoming.glade"
		wTree = gtk.glade.XML(gladefile)

		self.win_incoming = wTree.get_widget('window_incoming')
		self.win_incoming.set_title("call incoming")
		self.win_incoming_label_nr = wTree.get_widget('label_nr')
		self.win_incoming_label_name = wTree.get_widget('label_name')
		get_image(wTree, "button_pickUp", gtk.STOCK_APPLY)
		get_image(wTree, "button_putDown", gtk.STOCK_CANCEL)
        #self.win_incoming.connect('destroy', gtk.main_quit)

		dic = { "on_button_pickUp_clicked" : self.on_button_pickUp_clicked,
				"on_button_putDown_clicked" : self.on_button_putDown_clicked}
		wTree.signal_autoconnect(dic)

		self.win_incoming.show_all()
		self.win_incoming.hide()

	def win_active_update_time(self):
		Deb("My_handler_call win_active_update_time self.statusDialer:["+str(self.statusDialer)+"]")
		if self.statusDialer == "active":
			Deb("My_handler_call win_active_update_time self.active_time:["+str(self.active_time)+"]")
			gobject.timeout_add( 1000, self.win_active_update_time )
			self.win_active_label_time.set_text(str(self.active_time)+"sec.")
			self.active_time+=1

	def win_init_active(self):
		self.win_active = gtk.Window()

		gladefile = "dialog_active.glade"
		wTree = gtk.glade.XML(gladefile)

		self.win_active = wTree.get_widget('window_active')
		self.win_active.set_title("call active")
		self.win_active_label_nr = wTree.get_widget('label_nr')
		self.win_active_label_name = wTree.get_widget('label_name')
		self.win_active_label_time = wTree.get_widget('label_time')
		self.win_active_label_title = wTree.get_widget('label_title')
		get_image(wTree, "button_putDown", gtk.STOCK_CANCEL)
        #self.win_incoming.connect('destroy', gtk.main_quit)

		dic = { "on_button_active_putDown_clicked" : self.on_button_putDown_clicked}
		wTree.signal_autoconnect(dic)

		self.win_active.show_all()
		self.win_active.hide()
	def gsm_call_call_status(self, id, status, properties):
		Deb("My_handler_call gsm_call_call_status"+
			"\n id:\t["+str(id)+"]"+
			"\n status:\t["+str(status)+"]"+
			"\n properties:\t["+str(properties)+"]"
			)
		try:
			nrDial = str(properties['peer'])
		except:
			nrDial = ""

		if status == "incoming":
			Deb("My_handler_call gsm_call_call_status status:[incoming]")
			if self.statusDialer == "redy":
				self.win_incoming_label_nr.set_text(nrDial)
				self.win_incoming_label_name.set_text(getName_fromNr(nrDial))
				self.win_incoming.show()
				self.statusDialer = "incoming"

		if status == "active":
			Deb("My_handler_call gsm_call_call_status status:[active]")
			self.win_active_label_nr.set_text(nrDial)
			self.win_active_label_name.set_text(getName_fromNr(nrDial))
			self.active_time = 0
			self.statusDialer = "active"
			self.win_active_update_time()
			self.win_active.set_title("call active")
			self.win_active.show()


		if status == "release":
			Deb("My_handler_call gsm_call_call_status status:[release]")
			self.win_incoming.hide()
			self.win_active.hide()
			self.statusDialer = "redy"

		if status == "outgoing":
			Deb("My_handler_call gsm_call_call_status status:[outgoing]")
			self.win_active.set_title("calling to")
			self.win_active_label_title.set_text("calling to")
			self.win_active_label_nr.set_text(str(properties['peer']))
			self.win_active_label_name.set_text(getName_fromNr(nrDial))
			self.win_active_label_time.set_text("")
			self.win_active.show()
			self.statusDialer = "outgoing"

				
def getName_fromNr( nr ):
	return os.popen("../contact_cash.py search "+str(nr) ).read().replace("\n","")


if __name__ == "__main__":


	DBusGMainLoop(set_as_default=True)
	bus = dbus.SystemBus()


	while 1:
		try:
			gsm_device_obj = bus.get_object( 'org.freesmartphone.ogsmd', '/org/freesmartphone/GSM/Device' )
			gsm_call_iface = dbus.Interface(gsm_device_obj, 'org.freesmartphone.GSM.Call')
			gsm_sim_iface = dbus.Interface(gsm_device_obj, 'org.freesmartphone.GSM.SIM')
			gsm_call_iface.ListCalls()
			Deb("dialer gsm_call_iface present")
			break
		except:
			Deb("dialer gsm_call_iface not present try in 5sec.")
			time.sleep(5)


	Deb("dialer setting callbacks for call")
	my_handler_call = My_handler_call( gsm_call_iface )
	bus.add_signal_receiver(my_handler_call.gsm_call_call_status, dbus_interface="org.freesmartphone.GSM.Call",     signal_name="CallStatus")
	gobject.idle_add( my_handler_call.start )


	Deb("dialer dialer ready")
	gtk.main()



	