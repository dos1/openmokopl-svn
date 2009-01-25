#!/usr/bin/env python
import os,sys



import time
tStart = time.time()
def Deb( name ):
	print "[nm] ["+str(time.time()-tStart)+"] "+str(time.ctime())+" ["+str(name)+"]"
Deb("after import time")

import dbus
Deb("after import dbus")
from dbus.mainloop.glib import DBusGMainLoop
Deb("after import dbus main loop")
import gtk,gobject
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


#http://www.tele-servizi.com/janus/engfield1.html




class NM:
	def __init__(self, nm_iface):
		self.nm_iface = nm_iface

	def __initScrolled(self, tv):
		Deb("__initScrolled")
		return tv

	def nm_to_treestore(self, filter = ""):
		self.treestore.clear()
		Deb("nb nm_to_treestore start")

		for i in self.nm_iface.GetNeighbourCellInformation():
			self.treestore.append( None, [i['lac'], i['cid'], i['arfcn'], i['bsic'], int(i['rxlev']) ] )

		Deb("nm nm_to_treestore done")
		gobject.timeout_add( 2000, self.nm_to_treestore)

	def destroy_all(self, widget):
		gtk.main_quit()
		

	def on_button_pb_clicked(self,  widget ):
		gtk.main_quit()


	
	def Gui(self):
		Deb("nm Gui")
				
		self.win = gtk.Window()
		gladefile = "nm.glade"
		wTree = gtk.glade.XML(gladefile)
		self.win = wTree.get_widget('window_nm')
		self.win.set_title("networkmonitor")
		dic = { "on_button_close_clicked" : self.on_button_pb_clicked				
			}
		wTree.signal_autoconnect(dic)

		hbox_nm = wTree.get_widget('hbox_nm')
		self.treestore = gtk.TreeStore(str, str, str, str, int)
		
		self.nm_to_treestore()
		
		self.treeview = gtk.TreeView(self.treestore)
		#self.treeview.connect("cursor-changed", self.cb_scroll)
		
		tvcolumn = gtk.TreeViewColumn('lac')
		self.treeview.append_column(tvcolumn)
		cell = gtk.CellRendererText()
		tvcolumn.pack_start(cell, True)
		tvcolumn.add_attribute(cell, 'text', 0)
		self.treeview.set_search_column(0)
		tvcolumn.set_sort_column_id(0)
		
		tvcolumn = gtk.TreeViewColumn('cid')
		self.treeview.append_column(tvcolumn)
		cell = gtk.CellRendererText()
		#cell.set_property('size-points', 8 )
		tvcolumn.pack_start(cell, True)
		tvcolumn.add_attribute(cell, 'text', 1)
		self.treeview.set_search_column(1)
		tvcolumn.set_sort_column_id(1)

		tvcolumn = gtk.TreeViewColumn('arfcn')
		self.treeview.append_column(tvcolumn)
		cell = gtk.CellRendererText()
		#cell.set_property('size-points', 8 )
		tvcolumn.pack_start(cell, True)
		tvcolumn.add_attribute(cell, 'text', 2)
		self.treeview.set_search_column(2)
		tvcolumn.set_sort_column_id(2)

		tvcolumn = gtk.TreeViewColumn('bsic')
		self.treeview.append_column(tvcolumn)
		cell = gtk.CellRendererText()
		#cell.set_property('size-points', 8 )
		tvcolumn.pack_start(cell, True)
		tvcolumn.add_attribute(cell, 'text', 3)
		self.treeview.set_search_column(3)
		tvcolumn.set_sort_column_id(3)

		tvcolumn = gtk.TreeViewColumn('rxlev')
		self.treeview.append_column(tvcolumn)
		cell = gtk.CellRendererProgress()
		tvcolumn.pack_start(cell, True)
		tvcolumn.add_attribute(cell, 'text', 4)
		tvcolumn.add_attribute(cell, 'value', 4)
		self.treeview.set_search_column(4)
		tvcolumn.set_sort_column_id(4)

		hbox_nm.add( self.__initScrolled( self.treeview ) )
		self.treeview.show()
		
		self.win.connect('destroy', self.on_button_pb_clicked)
		Deb("nm Gui obj redy need to show_all")
		self.win.show()
		Deb("nm Gui done")

	def scrollToRow(self, widget ):
		print "click"
		treeselection = self.treeview.get_selection()
		tm, tree_iter = treeselection.get_selected()
		path = tm.get_path(tree_iter)
		col = self.treeview.get_column(1)
		self.treeview.scroll_to_cell(  path, col, True, 0.5,0 )



if __name__ == "__main__":
	Deb("__name__ start")
	DBusGMainLoop(set_as_default=True)
	bus = dbus.SystemBus()

	while 1:
		try:
			gsm_device_obj = bus.get_object( 'org.freesmartphone.ogsmd', '/org/freesmartphone/GSM/Device' )
			gsm_nm_iface = dbus.Interface(gsm_device_obj, 'org.freesmartphone.GSM.Monitor')
			Deb("nm gsm_nm_iface present")
			break
		except:
			Deb("nm gsm_nm_iface not present try in 5sec.")
			time.sleep(5)

	Deb("__name__ init main gui")
	cs = NM( gsm_nm_iface )
	cs.Gui()
	Deb("__name__ init main gui done")
	
	gtk.main()

			