#! /usr/bin/python

__author__="yoyo"
__date__ ="$Jan 22, 2009 11:03:53 PM$"





import elementary

import eleGlade




def clikCode( arg0, arg1 ):
	print "click for code"

def clicked( arg0, arg1 ):
	print "click for code"

def on_tb_bt01_clicked( arg0, arg1 ):
	print "click for code"

def clikDic( arg0, arg1 ):
	print "click for dic"


def on_togglebutton2_toggled( arg0, arg1 ):
	print "toggle changed"+str(arg0)+"\n"+str(arg1)

def on_toolbutton1_clicked( arg0, arg1 ):
	print "on_toolbutton1_clicked click!!"

def on_tb_bt01_clicked( arg0, arg1 ):
	print "on_tb_bt01_clicked"

def on_window1_destroy( arg0, arg1 ):
	elementary.exit()

if __name__ == "__main__":
	
	eleGladeFile = "test3.glade"
	eleTree = eleGlade.XML(eleGladeFile)
	win = eleTree.get_widget("window1")
	label1 = eleTree.get_widget("label1")
	entry2 = eleTree.get_widget("entry2")
	dic = {
		"on_window1_destroy" : on_window1_destroy,
		"on_tb_bt01_clicked" : on_tb_bt01_clicked
		}
	eleTree.signal_autoconnect( dic )

	label1.label_set("buuuu click<br> deam you")
	label1._callback_add("clicked", clicked)
	entry2.entry_set("ala<br>ma kota<br>a kot ma ale")
	entry2.cursor_changed = clikDic

	win.show()
	

	

	eleGladeFile = "test2.glade"
	eleTree = eleGlade.XML(eleGladeFile)
	win = eleTree.get_widget("window1")
	label12 = eleTree.get_widget( "label12" )
	label4 = eleTree.get_widget("label4")
	button2 = eleTree.get_widget( "button2" )
	viewport1 = eleTree.get_widget("viewport1")
	
	img = elementary.Icon( win )
	img.file_set( "osmupdater.png" )
	img.show()
	#viewport1.corner_set("top_right")
	viewport1.corner_set("bottom_right")
	viewport1.icon_set(img)
	viewport1.label_set("label")
	viewport1.info_set("info set")
	


	label12.label_set("label changed from code :) oo jjeee")
	button2.clicked = clikCode

	dic = {
		"on_button3_clicked" : clikDic,
		"on_togglebutton2_toggled" : on_togglebutton2_toggled,
		"on_window1_destroy" : on_window1_destroy
		}
	eleTree.signal_autoconnect( dic )

	win.show()


	"""

	eleGladeFile = "test1.glade"
	eleTree = eleGlade.XML(eleGladeFile)

	win2 = eleTree.get_widget("window1")
	win2.show()
	"""
	
	elementary.run()
	elementary.shutdown()
	