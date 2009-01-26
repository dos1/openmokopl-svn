#!/usr/bin/env python

import sys,os

from threading import Thread
import threading

import dbus
from dbus.mainloop.glib import DBusGMainLoop

import time
import gobject
import gtk

#opkg install http://downloads.tuxfamily.org/3v1deb/openmoko/python-mokoui2_0.1.0+svnr4342_armv4t.ipk


def Deb( name ):
	print "[yphonekitd] "+str(time.ctime())+" ["+str(name)+"]"


__author__="yoyo"
__date__ ="$Jan 19, 2009 3:34:24 PM$"

class My_cmd(threading.Thread):
	def __init__(self, cmd):
		Thread.__init__(self)
		self.cmd = cmd
	def run(self):
		Deb("My_cmd cmd")
		os.system(self.cmd)
		Deb("My_cmd done")

class My_handler_network(threading.Thread):
	def gsm_network_status(self, status, status1=""):
		Deb("My_handler_network gsm_network_status status:\t["+str(status)+"]")

	def gsm_network_signal(self, signal, status1=""):
		Deb("My_handler_network gsm_network_signal signal:\t["+str(signal)+"]")

	def gsm_network_incoming(self, ussd, status1=""):
		Deb("My_handler_network gsm_network_incoming ussd:\t["+str(ussd)+"]")

	def gsm_network_cipher(self, status, status1=""):
		Deb("My_handler_network gsm_network_cipher status:\t["+str(status)+"]")

	def gsm_sim_incomingMessage(self, id, status1=""):
		Deb("My_handler_network gsm_sms_incomingMessage\n"+
			"id:\t["+str(id)+"]"
			)
		#mb = self.gsm_sim_iface.RetrieveMessagebook('unread')
		#for m in mb:
		Deb("My_handler_network gsm_sms_incomingMessage making thread")
		os_cmd = "cd ./mb && python ./mb.py recive "+str(id)
		mCmd = My_cmd( os_cmd )
		mCmd.start()
		Deb("My_handler_network gsm_sms_incomingMessage end")


class My_handler_call(threading.Thread):
	def gsm_call_call_status(self, id="", status="", properties=""):
		Deb("My_handler_call gsm_call_call_status"+
			"\n id:\t["+str(id)+"]"+
			"\n status:\t["+str(status)+"]"+
			"\n properties:\t["+str(properties)+"]"
			)





if __name__ == "__main__":
	Deb("__name__ start")


	DBusGMainLoop(set_as_default=True)
	bus = dbus.SystemBus()

	while 1:
		try:
			usage_obj = bus.get_object('org.freesmartphone.ousaged', '/org/freesmartphone/Usage')
			usage_iface = dbus.Interface(usage_obj, 'org.freesmartphone.Usage')

			
			try:
				usage_obj.ReleaseResource("GSM")
				Deb("__name__ ReleaseResource")
			except:
				Deb("__name__ ReleaseResource error")

			gsm_device_obj = bus.get_object( 'org.freesmartphone.ogsmd', '/org/freesmartphone/GSM/Device' )
			gsm_call_iface = dbus.Interface(gsm_device_obj, 'org.freesmartphone.GSM.Call')
			gsm_device_iface = dbus.Interface(gsm_device_obj, 'org.freesmartphone.GSM.Device')
			gsm_network_iface = dbus.Interface(gsm_device_obj, 'org.freesmartphone.GSM.Network')
			gsm_sim_iface = dbus.Interface(gsm_device_obj, 'org.freesmartphone.GSM.SIM')
			Deb("__name__ dbus present")
			
			Deb("__name__ RequestResource")
			usage_obj.RequestResource("GSM")
			Deb("__name__ SetAntennaPower")
			gsm_device_iface.SetAntennaPower(True)
			Deb("__name__ Register")
			gsm_network_iface.Register()
			break
		except:
			Deb("__name__ dbus not present try in 5 sec")
			time.sleep(5)


	Deb("__name__ Teoretical redy :)")
	Deb("__name__ setting callbacks")
	Deb("__name__ setting callbacks for network")
	my_handler_network = My_handler_network()
	bus.add_signal_receiver(my_handler_network.gsm_network_status, dbus_interface="org.freesmartphone.GSM.Network",     signal_name="Status")
	bus.add_signal_receiver(my_handler_network.gsm_network_signal, dbus_interface="org.freesmartphone.GSM.Network",     signal_name="SignalStrength")
	bus.add_signal_receiver(my_handler_network.gsm_network_incoming, dbus_interface="org.freesmartphone.GSM.Network",     signal_name="IncomingUssd")
	bus.add_signal_receiver(my_handler_network.gsm_network_cipher, dbus_interface="org.freesmartphone.GSM.Network",     signal_name="CipherStatus")

	Deb("__name__ setting callbacks for sms")
	Deb("__name__ gsm_device_iface.SetSimBuffersSms(1) :["+str(gsm_device_iface.SetSimBuffersSms(1))+"]")
	bus.add_signal_receiver(my_handler_network.gsm_sim_incomingMessage, dbus_interface="org.freesmartphone.GSM.SIM",     signal_name="IncomingStoredMessage")
	gobject.idle_add( my_handler_network.start )

	Deb("__name__ setting callbacks for call")
	my_handler_call = My_handler_call()
	bus.add_signal_receiver(my_handler_call.gsm_call_call_status, dbus_interface="org.freesmartphone.GSM.Call",     signal_name="CallStatus")
	gobject.idle_add( my_handler_call.start )

	Deb("__name__ making primitive phonebookcash start")
	Deb("__name__ making primitive phonebookcash res:[\n"+str(os.popen("./contact_cash.py \"casch\"").read())+"]")
	Deb("__name__ making primitive phonebookcash end")

	dialer_test = os.popen("ps ax | grep [d]ialer").read().replace("\n","")
	if dialer_test == "":
		Deb("__name__ starting dialer")
		os.system("cd ./dial && ./dialer.py &")
	else:
		Deb("__name__ starting dialer in running")

		

	Deb("__name__ starting main loop")
	gtk.main()

	usage_obj.ReleaseResource("GSM")

	Deb("__name__ end")


	