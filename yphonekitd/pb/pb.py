#!/usr/bin/env python
import os,sys


fileName = "/tmp/pb_pido"
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


import time
tStart = time.time()
def Deb( name ):
	print "[PB] ["+str(time.time()-tStart)+"] "+str(time.ctime())+" ["+str(name)+"]"
Deb("after import time")

def get_image( wTree, obj, icoStock ):
	objWid = wTree.get_widget(obj)
	ico = gtk.Image()
	ico.set_from_stock( icoStock, gtk.ICON_SIZE_BUTTON )
	ico.show()
	objWid.set_image( ico )

import dbus
Deb("after import dbus")
from dbus.mainloop.glib import DBusGMainLoop
Deb("after import dbus main loop")
import gtk
Deb("after import gtk")
import gtk.glade
Deb("after import glade")
#try:
#	import mokoui
#	print "mokoui"
#	use_mokoui = True
#except:
#	print "!mokoui"
#	use_mokoui = False
use_mokoui = False



Deb("after imports ")




__author__="yoyo"
__date__ ="$Jan 19, 2009 4:57:02 PM$"



def read_pb_casch():
    Deb("read_pb_casch start")
    f = open("/tmp/pb_casch","r")
    tr = []
    while 1:
	line = f.readline()
	if not line:
	    break
	ob = line.split("]##[")
	tr.append( [ str(ob[2]), str(ob[3]), str(ob[1]) ] )
	
    Deb("read_pb_casch end")
    return tr


	



class ContactSearch:
	def __init__(self, gsm_call_iface):
		self.gsm_call_iface = gsm_call_iface


	def __initScrolled(self, tv):
		Deb("pb __initScrolled")
		return tv
		tab_content = tv
		if use_mokoui:
			self.scrolled = mokoui.FingerScroll()
		else:
			self.scrolled = gtk.ScrolledWindow()
			self.scrolled.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
			
		self.scrolled.show()
		self.scrolled.add_with_viewport(tab_content)

		Deb("pb __initScrolled end")
		return self.scrolled

	def pb_to_treestore(self, filter = ""):
	    Deb("pb pb_to_treestore start")
	    f = 0
	    filter = filter.lower()
	    for i in self.pb:
		if str(i[1]).lower().find(filter) != -1 or str(i[2]).lower().find(filter) != -1 or filter == "":
	    	    f+=1
		    self.treestore.append(None, [str(i[0]), str(i[1]), str(i[2])])
		
	    Deb("pb pb_to_treestore done found:["+str(f)+"]")


	def destroy_all(self, widget):
		gtk.main_quit()
		self.win.hide()
		

	def on_button_pb_clicked(self,  widget ):
		gtk.main_quit()
		self.win.hide()


	def on_button_call_clicked(self,  widget ):
		Deb("pb on_button_call_clicked")
		try:
			treeselection = self.treeview.get_selection()
			model, iter = treeselection.get_selected()
			text = model.get_value(iter, 2)
			self.gsm_call_iface.Initiate( str(text), 'voice' )
			gtk.main_quit()
			self.win.hide()
		except:
			Deb("pb treeview not selected")

	def on_button_sms_clicked(self,  widget ):
		Deb("pb on_button_sms_clicked")
		try:
			treeselection = self.treeview.get_selection()
			model, iter = treeselection.get_selected()
			reciver_name = model.get_value(iter, 1)
			reciver_nr = model.get_value(iter, 2)

			os.system("cd ../mb && ./mb.py send \""+str(reciver_name)+"\" \""+str(reciver_nr)+"\" &")
			gtk.main_quit()
			self.win.hide()
		except:
			Deb("pb on_button_sms_clicked not selected")

	def on_button_edit_clicked(self, widget ):
		Deb("pb on_button_edit_clicked")
		try:
			treeselection = self.treeview.get_selection()
			model, iter = treeselection.get_selected()
			reciver_id = model.get_value(iter, 0)
			reciver_name = model.get_value(iter, 1)
			reciver_nr = model.get_value(iter, 2)
			ce = ContactEdit( self )
			ce.Gui( reciver_id, reciver_name, reciver_nr )
		except:
			ce = ContactEdit( self )
			ce.Gui( "", "", "" )
			Deb("pb on_button_edit_clicked not selected")
		

	def on_entry_search_changed(self,  widget ):
		Deb("pb on_entry_search_changed str:["+str(widget.get_text())+"]")
		self.treestore.clear()
		self.pb_to_treestore( str(widget.get_text()) )

	def on_button_search_clean_clicked(self,  widget ):
		self.entry_search.set_text("")


	def pb_casch_to_self(self):
	    self.pb = read_pb_casch()
	
	def Gui(self):
		Deb("pb Gui")
				
		self.win = gtk.Window()
		gladefile = "pb.glade"
		wTree = gtk.glade.XML(gladefile)
		self.win = wTree.get_widget('window_pb')
		self.win.set_title("pb")
		dic = { "on_button_close_clicked" : self.on_button_pb_clicked,
				"on_button_edit_clicked" : self.on_button_edit_clicked,
				"on_button_sms_clicked" : self.on_button_sms_clicked,
				"on_button_call_clicked" : self.on_button_call_clicked,
				"on_entry_search_changed" : self.on_entry_search_changed,
				"on_button_search_clean_clicked" : self.on_button_search_clean_clicked
			}
		wTree.signal_autoconnect(dic)

		hbox_pb = wTree.get_widget('hbox_pb')
		self.entry_search = wTree.get_widget('entry_search')

		self.treestore = gtk.TreeStore(str, str, str)
		
		self.pb_casch_to_self()
		self.pb_to_treestore()
		
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
		tvcolumn = gtk.TreeViewColumn('Name')
		self.treeview.append_column(tvcolumn)
		cell = gtk.CellRendererText()
		#cell.set_property('size-points', 8 )
		tvcolumn.pack_start(cell, True)
		tvcolumn.add_attribute(cell, 'text', 1)
		self.treeview.set_search_column(1)
		tvcolumn.set_sort_column_id(1)

		tvcolumn = gtk.TreeViewColumn('Tel')
		self.treeview.append_column(tvcolumn)
		cell = gtk.CellRendererText()
		tvcolumn.pack_start(cell, True)
		tvcolumn.add_attribute(cell, 'text', 2)
		self.treeview.set_search_column(2)
		tvcolumn.set_sort_column_id(2)

		#self.treeview.set_reorderable(True)
		self.treeview.connect( "cursor-changed", self.scrollToRow )

		hbox_pb.add( self.__initScrolled( self.treeview ) )
		self.treeview.show()
		
		self.win.connect('destroy', self.on_button_pb_clicked)
		Deb("pb Gui obj redy need to show_all")
		self.win.show()
		Deb("pb Gui done")

	def scrollToRow(self, widget ):
		print "click"
		treeselection = self.treeview.get_selection()
		tm, tree_iter = treeselection.get_selected()
		path = tm.get_path(tree_iter)
		col = self.treeview.get_column(1)
		self.treeview.scroll_to_cell(  path, col, True, 0.5,0 )

class ContactEdit:
	def __init__(self, main_window_obj ):
		self.main_window_obj = main_window_obj

	def on_button_edit_close_clicked( self, widget ):
		Deb("ContactEdit on_button_edit_close_clicked")
		self.win.hide()
		self.main_window_obj.win.show_all()
		self.win = None

	def on_button_edit_del_clicked( self, widget ):
		Deb("ContactEdit on_button_edit_del_clicked")
		global gsm_sim_iface
		gsm_sim_iface.DeleteEntry('contacts', int(self.r_id))
		os.system("../contact_cash.py \"casch\"")
		self.main_window_obj.pb_casch_to_self()
		self.win.hide()
		self.main_window_obj.win.show()
		self.main_window_obj.entry_search.set_text(self.r_name)

	def on_button_edit_clean_clicked( self, widget ):
		Deb("ContactEdit on_button_edit_clean_clicked")
		self.r_id = ""
		self.entryName.set_text("")
		self.entryNr.set_text("")
		if self.r_id == "":
			self.btDel.set_sensitive(False)

	def getLastIndex(self):
		global gsm_sim_iface
		max = 0
		pb = gsm_sim_iface.RetrievePhonebook('contacts')
		for p in pb:
			if max < p[0]:
				max = p[0]
		
		return max

	def on_button_edit_ok_clicked( self, widget ):
		global gsm_sim_iface
		if self.r_id == "":
			Deb("ContactEdit add")
			gsm_sim_iface.StoreEntry('contacts', (int(self.getLastIndex())+1), self.entryName.get_text(), self.entryNr.get_text() )
			self.win.hide()
			self.main_window_obj.win.show()
		else:
			Deb("ContactEdit save")
			gsm_sim_iface.StoreEntry('contacts', int(self.r_id), self.entryName.get_text(), self.entryNr.get_text() )
			self.win.hide()
			self.main_window_obj.win.show()

		os.system("../contact_cash.py \"casch\"")
		self.main_window_obj.pb_casch_to_self()
		self.main_window_obj.entry_search.set_text(self.entryName.get_text())

	def Gui(self, r_id, r_name, r_nr):
		self.win = gtk.Window()
		gladefile = "pb.glade"
		wTree = gtk.glade.XML(gladefile)
		self.win = wTree.get_widget('window_edit')
		self.win.set_title("pb add/edit/save/del")
		dic = {
				"on_button_edit_close_clicked" : self.on_button_edit_close_clicked,
				"on_button_edit_clean_clicked" : self.on_button_edit_clean_clicked,
				"on_button_edit_del_clicked" : self.on_button_edit_del_clicked,
				"on_button_edit_ok_clicked" : self.on_button_edit_ok_clicked

			}
		wTree.signal_autoconnect(dic)

		self.r_id = r_id
		self.r_name = r_name
		self.r_nr = r_nr


		self.entryName = wTree.get_widget('entry_edit_name')
		self.entryNr = wTree.get_widget('entry_edit_nr')

		self.entryName.set_text(self.r_name)
		self.entryNr.set_text(self.r_nr)

		self.btDel = wTree.get_widget('button_edit_del')
		if self.r_id == "":
			self.btDel.set_sensitive(False)


		self.win.connect('destroy', gtk.main_quit)
		self.main_window_obj.win.hide()
		self.win.show()
		


if __name__ == "__main__":
	Deb("__name__ start")
	DBusGMainLoop(set_as_default=True)
	bus = dbus.SystemBus()

	while 1:
		try:
			gsm_device_obj = bus.get_object( 'org.freesmartphone.ogsmd', '/org/freesmartphone/GSM/Device' )
			gsm_call_iface = dbus.Interface(gsm_device_obj, 'org.freesmartphone.GSM.Call')
			gsm_sim_iface = dbus.Interface(gsm_device_obj, 'org.freesmartphone.GSM.SIM')
			Deb("pb gsm_sim_iface present")
			break
		except:
			Deb("pb gsm_sim_iface not present try in 5sec.")
			time.sleep(5)

	Deb("__name__ init main gui")
	cs = ContactSearch( gsm_call_iface )
	cs.Gui()
	Deb("__name__ init main gui done")
	
	i = 0
	open(fileName,"w").close()
	while 1:
		s = open(fileName,"r")


		Deb("pb ready")
		cs.win.show_all()
		gtk.main()
		Deb("pb end")


		while 1:
			r = s.readline()[:-1]
			Deb("pb iter wait")
			if str(r) == "run":
				s.close()
				open(fileName,"w").close()
				i = 0
				break
			time.sleep(0.7)

			