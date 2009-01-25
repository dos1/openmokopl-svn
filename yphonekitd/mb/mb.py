#!/usr/bin/env python

from threading import Thread
import threading

import dbus
from dbus.mainloop.glib import DBusGMainLoop

import time,os
import gobject
import gtk
import gtk.glade

import sys

def Deb( name ):
	print "[mb] "+str(time.ctime())+" ["+str(name)+"]"

__author__="yoyo"
__date__ ="$Jan 19, 2009 4:57:02 PM$"

def get_image( wTree, obj, icoStock ):
	objWid = wTree.get_widget(obj)
	ico = gtk.Image()
	ico.set_from_stock( icoStock, gtk.ICON_SIZE_BUTTON )
	ico.show()
	objWid.set_image( ico )




class Mb_send:
	def __init__(self, gsm_sim_iface, gsm_sms_iface, parentObj = 0 ):
		self.gsm_sim_iface = gsm_sim_iface
		self.gsm_sms_iface = gsm_sms_iface
		self.parentObj = parentObj

	def destroy_all( self, widget ):
		if self.parentObj == 0:
			gtk.main_quit()
		else:
			self.parentObj.win.show()
			self.win.hide()

	def on_button_send_clicked( self, widget ):
		startiter = self.buff.get_start_iter()
		enditer = self.buff.get_end_iter()

		self.gsm_sms_iface.SendMessage( self.lbnr.get_label(), self.buff.get_text(startiter, enditer ), {} )
		if self.parentObj == 0:
			gtk.main_quit()
		else:
			self.parentObj.win.show()
			self.win.hide()

	def on_textview_sms_key_release_event( self, widget, ik ):
		self.lbchars.set_text("chars ("+str(160-self.buff.get_char_count())+")")


	def Gui(self, reciver="", nr=""):
		self.win = gtk.Window()
		gladefile = "mb_send.glade"
		wTree = gtk.glade.XML(gladefile)

		self.win = wTree.get_widget('window_sms_send')
		lbreciver = wTree.get_widget('label_reciver')
		self.lbnr = wTree.get_widget('label_nr')
		self.lbchars = wTree.get_widget('label_chars')
		txtview = wTree.get_widget('textview_sms')

		lbreciver.set_label( str(reciver) )
		self.lbnr.set_label( str(nr) )
		
		self.buff = gtk.TextBuffer()
		self.buff.set_text( str( "" ) )
		txtview.set_buffer( self.buff )

		self.win.set_title("send sms")
		dic = { "on_button_send_clicked" : self.on_button_send_clicked,
				"on_textview_sms_key_release_event" : self.on_textview_sms_key_release_event,
				"on_button_close_clicked" : self.destroy_all
			}

		wTree.signal_autoconnect(dic)
		self.win.connect('destroy', gtk.main_quit)
		self.win.show_all()






class Mb_recive:
	def __init__(self, gsm_sim_iface, gsm_sms_iface, parentObj = 0 ):
		self.gsm_sim_iface = gsm_sim_iface
		self.gsm_sms_iface = gsm_sms_iface
		self.parentObj = parentObj

	def destroy_all( self, widget ):
		if self.parentObj == 0:
			gtk.main_quit()
		else:
			self.parentObj.win.show()
			self.win.hide()

	def on_button_re_clicked( self, widget ):
		mb_se = Mb_send( self.gsm_sim_iface, self.gsm_sms_iface, self )
		mb_se.Gui( self.lbsender.get_label(), self.lbnr.get_label() )
		self.win.hide()

	def on_button_deleta_clicked( self, widget ):
		Deb("mb on_button_deleta_clicked id:["+self.id+"]")
		self.gsm_sim_iface.DeleteMessage( int(self.id) )
		if self.parentObj == 0:
			gtk.main_quit()
		else:
			#self.parentObj.sim_to_list()

			nr = 0
			for i in self.parentObj.sim_message_list:
				if str(i[0]) == str(self.id):
					self.parentObj.sim_message_list.pop( nr )
					break
				nr+=1

			Deb("mb on_button_deleta_clicked start tv refresh")
			txt = self.parentObj.entry_search.get_text()
			self.parentObj.entry_search.set_text("1234567890")
			self.parentObj.entry_search.set_text( txt )
			Deb("mb on_button_deleta_clicked tv refresh done")
			self.parentObj.win.show()
			self.win.hide()

	def Gui(self, id, sender="", nr="", stime="", txt=""):
		self.win = gtk.Window()
		gladefile = "mb_recive.glade"
		wTree = gtk.glade.XML(gladefile)

		self.win = wTree.get_widget('window_sms_recive')
		self.lbsender = wTree.get_widget('label_sender')
		self.lbnr = wTree.get_widget('label_nr')
		lbtime = wTree.get_widget('label_time')
		txtview = wTree.get_widget('textview_sms')

		get_image(wTree, "button_re", gtk.STOCK_CONVERT)

		self.lbsender.set_label( str(sender) )
		self.lbnr.set_label( str(nr) )
		lbtime.set_label( str(stime)  )

		self.id = id
		buff = gtk.TextBuffer()
		buff.set_text( str( txt ) )
		txtview.set_buffer( buff )

		self.win.set_title("recive sms")
		dic = {
				"on_button_re_clicked" : self.on_button_re_clicked,
				"on_button_deleta_clicked" : self.on_button_deleta_clicked,
				"on_button_close_clicked" : self.destroy_all
			}

		wTree.signal_autoconnect(dic)
		self.win.connect('destroy', gtk.main_quit)
		self.win.show_all()



class Mb_view:
	def __init__(self, gsm_sim_iface, gsm_sms_iface ):
		self.gsm_sim_iface = gsm_sim_iface
		self.gsm_sms_iface = gsm_sms_iface
		self.sim_message_list = []
		self.cb_buffored = 0
		

	def __initScrolled(self, tv):
		Deb("mb __initScrolled")
		return tv

	def nr_to_name_buffer(self, nr):
		Deb("mb nr_to_name_buffer")
		if self.cb_buffored == 0:
			Deb("mb nr_to_name_buffer make buffer")
			self.cb_buffored = 1
			self.nr_buff = []
			f = open("/tmp/pb_casch", "r")
			while 1:
				line = f.readline()
				if not line:
					break
				i = line.split("]##[")
				self.nr_buff.append( [ i[1], i[3] ] )
			Deb("mb nr_to_name_buffer buffer done")
			
		if nr[0]=="+":
			phoneNr = nr[3:]
		else:
			phoneNr = nr

		for n in self.nr_buff:
			if str(n[0]) == str(phoneNr):
				return str(n[1])

		return nr
	

	def on_button_close_clicked( self, widget ):
		gtk.main_quit()


	def sim_to_list_add_item_to_list( self, item ):
		Deb("mb sim_to_list_add_item_to_list")
		if item[1] == "unread":
			adds = "[!]"
		else:
			adds = ""

		self.sim_message_list.append(\
			[ item[0], item[1],  item[2],  item[3], adds+time.strftime("%y-%m-%d %H:%M",time.strptime(item[4]['timestamp'][:24]) ) ]
			)

	def sim_to_list( self ):
		Deb("mb sim_to_list")
		sim = self.gsm_sim_iface.RetrieveMessagebook('all')
		Deb("mb sim_to_list recive list, start parsing")
		self.sim_message_list = []
		for i in sim:
			if str(i[1]) == "read" or str(i[1]) == "unread":
				self.sim_to_list_add_item_to_list( i )

	def list_to_tv( self, filter = "" ):
		Deb("mb list_to_tv")
		f = 0
		filter = str(filter).lower()
		for i in self.sim_message_list:
			name = self.nr_to_name_buffer(str(i[2]))
			if str(i[3]).lower().find(filter) != -1 or name.lower().find(filter) != -1 or filter == "":
				f+=1
				self.treestore.append(None, [str(i[0]), name, str(i[4]), str(i[3]), str(i[2]) ])

		Deb("mb list_to_tv done found:["+str(f)+"]")

	def on_entry_search_changed(self,  widget ):
		Deb("mb on_entry_search_changed str:["+str(widget.get_text())+"]")
		self.treestore.clear()
		self.list_to_tv( str(widget.get_text()) )

	def on_button_search_clean_clicked(self,  widget ):
		self.entry_search.set_text("")

	def on_button_view_clicked( self, widget ):
		Deb("mb on_button_view_clicked")
		try:
			treeselection = self.treeview.get_selection()
			model, iter = treeselection.get_selected()
			reciver_id = model.get_value(iter, 0)
			reciver_sender = model.get_value(iter, 1)
			reciver_time = model.get_value(iter, 2)
			reciver_txt = model.get_value(iter, 3)
			reciver_nr = model.get_value(iter, 4)
			#os.system("./mb.py recive "+str(reciver_id))
			mb_re = Mb_recive( self.gsm_sim_iface, self.gsm_sms_iface, self )
			#self, id, sender="", nr="", stime="", txt=""
			mb_re.Gui( reciver_id, reciver_sender, reciver_nr, reciver_time, reciver_txt )
			self.win.hide()
		except:
			Deb("mb on_button_view_clicked not selected")

	def on_button_sms_clicked( self, widget ):
		Deb("mb on_button_sms_clicked")
		try:
			treeselection = self.treeview.get_selection()
			model, iter = treeselection.get_selected()
			reciver_name = model.get_value(iter, 1)
			reciver_nr = model.get_value(iter, 4)
			#os.system("./mb.py send \""+str(reciver_name)+"\" \""+str(reciver_nr)+"\"" )
			mb_se = Mb_send( self.gsm_sim_iface, self.gsm_sms_iface, self)
			#Gui(self, reciver="", nr=""):
			mb_se.Gui( reciver_name, reciver_nr )
			self.win.hide()
		except:
			Deb("mb on_button_sms_clicked not selected")

	def Gui(self):
		self.win = gtk.Window()
		gladefile = "mb.glade"
		wTree = gtk.glade.XML(gladefile)

		self.win = wTree.get_widget('window_mb')
		self.win.set_title("sms's")
		hbox_mb = wTree.get_widget('hbox_mb')
		self.entry_search = wTree.get_widget('entry_search')

		dic = {
				"on_button_close_clicked" : self.on_button_close_clicked,
				"on_entry_search_changed" : self.on_entry_search_changed,
				"on_button_view_clicked" : self.on_button_view_clicked,
				"on_button_sms_clicked" : self.on_button_sms_clicked,
				"on_button_search_clean_clicked" : self.on_button_search_clean_clicked
			}

		wTree.signal_autoconnect(dic)
		self.win.connect('destroy', self.on_button_close_clicked)


		get_image(wTree, "button_re", gtk.STOCK_CONVERT)
		get_image(wTree, "button_view", gtk.STOCK_EDIT)
		


		self.treestore = gtk.TreeStore(str, str, str, str, str)
		self.treeview = gtk.TreeView(self.treestore)
		#self.treeview.connect("cursor-changed", self.cb_scroll)
		"""
		tvcolumn = gtk.TreeViewColumn('id')
		self.treeview.append_column(tvcolumn)
		cell = gtk.CellRendererText()
		tvcolumn.pack_start(cell, True)
		tvcolumn.add_attribute(cell, 'text', 0)
		self.treeview.set_search_column(0)
		tvcolumn.set_sort_column_id(0)
		"""
		tvcolumn = gtk.TreeViewColumn('Sender')
		self.treeview.append_column(tvcolumn)
		cell = gtk.CellRendererText()
		tvcolumn.pack_start(cell, True)
		tvcolumn.add_attribute(cell, 'text', 1)
		self.treeview.set_search_column(1)
		tvcolumn.set_sort_column_id(1)

		tvcolumn = gtk.TreeViewColumn('Time')
		self.treeview.append_column(tvcolumn)
		cell = gtk.CellRendererText()
		tvcolumn.pack_start(cell, True)
		tvcolumn.add_attribute(cell, 'text', 2)
		self.treeview.set_search_column(2)
		tvcolumn.set_sort_column_id(2)

		tvcolumn = gtk.TreeViewColumn('Content')
		self.treeview.append_column(tvcolumn)
		cell = gtk.CellRendererText()
		tvcolumn.pack_start(cell, True)
		tvcolumn.add_attribute(cell, 'text', 3)
		self.treeview.set_search_column(3)
		tvcolumn.set_sort_column_id(3)



		#self.treeview.set_reorderable(True)
		self.treeview.connect( "cursor-changed", self.scrollToRow )

		self.sim_to_list()
		self.list_to_tv()

		hbox_mb.add( self.__initScrolled( self.treeview ) )
		self.treeview.show()




		self.win.show_all()





	def scrollToRow(self, widget ):
		print "click"
		treeselection = self.treeview.get_selection()
		tm, tree_iter = treeselection.get_selected()
		path = tm.get_path(tree_iter)
		col = self.treeview.get_column(0)
		self.treeview.scroll_to_cell(  path, col, True, 0.5,0 )



def nr_to_name( nr ):
	return os.popen("../contact_cash.py search "+str(nr) ).read().replace("\n","")

if __name__ == "__main__":
	DBusGMainLoop(set_as_default=True)
	bus = dbus.SystemBus()
	while 1:
		try:
			gsm_device_obj = bus.get_object( 'org.freesmartphone.ogsmd', '/org/freesmartphone/GSM/Device' )
			gsm_sim_iface = dbus.Interface(gsm_device_obj, 'org.freesmartphone.GSM.SIM')
			gsm_sms_iface = dbus.Interface(gsm_device_obj, 'org.freesmartphone.GSM.SMS')
			gsm_sim_iface.GetMessagebookInfo()
			Deb("mb gsm_sim_iface present")
			break
		except:
			Deb("mb gsm_sim_iface not present try in 5sec.")
			time.sleep(5)

	
	#args
	# ./mb.py recive id sender nr time text
	killme = 1
	Deb("mb args ----------------")
	try:
		if sys.argv[1] == "recive":
			Deb("mb action recive")
			m = gsm_sim_iface.RetrieveMessage(int(sys.argv[2]))
			killme = 0
			Deb("mb action recive iter m:\n["+str(m)+"]")
			sender = nr_to_name( m[1] )
			mb_re = Mb_recive( gsm_sim_iface, gsm_sms_iface )
			mb_re.Gui( str(sys.argv[2]), sender, str(m[1]), str(m[3]['timestamp']), str(m[2]) )
		if sys.argv[1] == "send":
			Deb("mb action send")
			killme = 0
			mb_se = Mb_send( gsm_sim_iface, gsm_sms_iface )
			mb_se.Gui( str(sys.argv[2]), str(sys.argv[3]) )
	except:
		Deb("mb action view all")
		killme = 0
		mb_v = Mb_view( gsm_sim_iface, gsm_sms_iface )
		mb_v.Gui(  )

	Deb("mb args ----------------")

	Deb("mb ready")
	if killme == 0:
		gtk.main()
	Deb("mb end")


	