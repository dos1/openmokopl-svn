
__author__="yoyo"
__date__ ="$Jan 22, 2009 11:03:36 PM$"


import elementary

import os,sys,time

import pprint

import xml.dom.minidom
from xml.dom.minidom import Node

"""
<raster> set align for label to 0.5 0.5
<raster> for all buttons set them to -1.0 -1.0
<raster> set weight for all to 1.0 1.0
<yoyo> I need tu understend align -1.0 0.5..... and weight ....
<raster> -1.0 for align == fill the area given
<raster> 0.0-1.0 is alignment (left to right, top to bottom)
<raster> 0.5 of course is centered
"""
tStart = time.time()
def Deb( s ):
	print "[eleGlade] ["+str( time.time()-tStart )+"] ["+str(s)+"]"

def getPropertyFromWidget( p, name ):
	for b in p.childNodes:
		Deb("getPropertyFromWidget: localName"+str(b.localName) )
		if str(b.localName) == "property":
			if b.getAttribute("name") == name:
				return str(b.childNodes[0].nodeValue)
	return ""

def getSignalFromWidget( p, objName ):
	global objectsSignalsList

	for b in p.childNodes:
		Deb( "getSignalFromWidget: localName"+str(b.localName) )
		if str(b.localName) == "signal":
			objectsSignalsList.append( [ objName, b.getAttribute("name"), b.getAttribute("handler")] )


def packing( obj, path ):
	obj.size_hint_weight_set(1.0, 1.0)
	obj.size_hint_align_set(-1.0, -1.0)

	parent = path[0].parentNode.parentNode.childNodes
	for i in parent:
		if str(i.localName) == "packing":

			for p in i.childNodes:
				if str(p.localName) == "property":
					if str(p.getAttribute("name")) == "expand":
						if p.childNodes[0].nodeValue == "False":
							print "packing expand false"
							obj.size_hint_weight_set(-1.0, -1.0)
						else:
							print "packing expand true"
							obj.size_hint_weight_set(1.0, 1.0)
	return obj

def searchForLabel( path, search4 = "label" ):
	for i in path:
		if str(i.localName) == "property":
			if i.getAttribute("name") == search4:
				return str(i.childNodes[0].nodeValue)

	return ""

def eleWindow( path, name ):
	win = elementary.Window(name, elementary.ELM_WIN_BASIC)
	win.title_set( searchForLabel(path, "title") )
	#win.show()
	return win


def eleVBox( path, parentObj ):
	tr = elementary.Box( parentObj )
	tr = packing( tr, path )
	tr.show()
	return tr

def eleHBox( path, parentObj ):
	tr = elementary.Box( parentObj )
	tr.horizontal_set(True)
	tr = packing( tr, path )
	tr.show()
	return tr

def eleButton( path, parentObj ):
	bt = elementary.Button( parentObj )
	bt.label_set( searchForLabel(path) )
	bt = packing( bt, path )
	bt.show()
	return bt

def eleLabel( path, parentObj ):
	lb = elementary.Label( parentObj )
	lb.label_set(searchForLabel(path))
	lb = packing ( lb, path )
	lb.show()
	return lb

def eleToggle( path, parentObj ):
	tr = elementary.Toggle( parentObj)
	label = searchForLabel(path).split("#,#")
	tr.label_set( label[0] )
	tr = packing ( tr, path )
	try:
		on = label[1]
		off = label[2]
	except:
		on = "I"
		off = "0"
	tr.states_labels_set(on,off)
	tr.show()
	return tr


def eleFrame( path, parentObj ):
	fr = elementary.Frame( parentObj )
	fr.label_set( "ophonekitd" )
	Deb( "-------------- frame --------------------" )
	child = 0
	for i in path:
		if str(i.localName) == "property":
			print str(i.getAttribute("name") )

		if str(i.localName) == "child" and child == 0:
			child+=1
		elif str(i.localName) == "child" and child == 1:
			for wid in i.childNodes:
				if str( wid.localName ) == "widget" :
					fr.label_set(  getPropertyFromWidget( wid, "label") )



	print "-------------- frame --------------------"

	fr = packing ( fr, path )
	fr.show()
	return fr


def eleScroller( path, parentObj ):
	tr = elementary.Scroller( parentObj )
	tr = packing ( tr, path )
	tr.show()
	return tr


def eleImage( path, parentObj ):
	tr = elementary.Icon( parentObj )
	try:
		tr.file_set(str(getPropertyFromWidget(path[0].parentNode, "pixbuf") ))
		Deb( "icon file_set: found" )
	except:
		Deb( "icon file_set: not found" )
		
	
	tr = packing ( tr, path )
	tr.show()
	return tr


def eleBubble( path, parentObj ):
	tr = elementary.Bubble( parentObj )
	tr = packing ( tr, path )
	tr.show()
	return tr

window = 0

objectsList = []
objectsSignalsList = []



def buildElementsFromXml( g, parentName = "", parentObj = "", frameParent = "" ):
	Deb( "parsing child " )
	for i in g.childNodes:
		if i.localName == "widget":
			_class = i.getAttribute("class")
			_id = i.getAttribute("id")

			Deb(  "widget class:"+str(_class)+\
				" id:"+str(_id)+\
				" parent:"+str(parentName) )
			if _class == "GtkWindow":
				win = eleWindow( i.childNodes, _id )
				objectsList.append( [str(_id),win ] )
				getSignalFromWidget( i, str(_id) )
				bg = elementary.Background(win)
				win.resize_object_add(bg)
				bg.size_hint_weight_set(1.0, 1.0)
				bg.show()

				for s in i.childNodes:
					buildElementsFromXml( s, _id , win )

			if _class == "GtkVBox":
				vbox = eleVBox( i.childNodes, parentObj )
				objectsList.append( [str(_id),vbox ] )
				if frameParent == 1:
					parentObj.content_set( vbox )
				else:
					global window
					if window == 0:
						parentObj.resize_object_add( vbox )
						window = 1
					else:
						parentObj.pack_end( vbox )

				for s in i.childNodes:
					buildElementsFromXml( s, parentName , vbox )


			if _class == "GtkHBox":
				hbox = eleHBox( i.childNodes, parentObj )
				objectsList.append( [str(_id),hbox] )
				if frameParent == 1:
					parentObj.content_set( hbox )
				else:
					parentObj.pack_end( hbox )
				for s in i.childNodes:
					buildElementsFromXml( s, parentName , hbox )

			if _class == "GtkScrolledWindow":
				sc = eleScroller( i.childNodes, parentObj )
				objectsList.append( [str(_id),sc ])
				if frameParent == 1:
					parentObj.content_set( sc )
				else:
					parentObj.pack_end( sc )
				for s in i.childNodes:
					buildElementsFromXml( s, parentName , sc, 1 )


			if _class == "GtkExpander":
				exp = eleFrame( i.childNodes, parentObj )
				objectsList.append( [str(_id),exp])
				parentObj.pack_end( exp )

				s = i.childNodes[5]
				Deb(  "expander: "+str(s.localName) )
				buildElementsFromXml( s, parentName , exp, 1 )


			if _class == "GtkButton":
				bt = eleButton(i.childNodes, parentObj)
				objectsList.append( [str(_id),bt])
				getSignalFromWidget( i, str(_id) )
				parentObj.pack_end( bt )

			if _class == "GtkImage":
				img = eleImage(i.childNodes, parentObj)
				objectsList.append( [str(_id),img])
				parentObj.pack_end( img )

			if _class == "GtkViewport":
				vp = eleBubble(i.childNodes, parentObj)
				objectsList.append( [str(_id),vp])
				parentObj.pack_end( vp )
				for s in i.childNodes:
					buildElementsFromXml( s, parentName , vp, 1 )

			if _class == "GtkLabel":
				lb = eleLabel(i.childNodes, parentObj)
				objectsList.append( [str(_id),lb])
				if frameParent == 1:
					parentObj.content_set( lb )
				else:
					parentObj.pack_end( lb )

			if _class == "GtkToggleButton":
				tb = eleToggle( i.childNodes, parentObj)
				objectsList.append( [str(_id),tb])
				getSignalFromWidget( i, str(_id) )
				parentObj.pack_end( tb )

	Deb( "parsing child done" )

class eTree:
	def __init__( self, objList, objSignalsList ):
		self.objList = objList
		self.objSignalsList = objSignalsList


	def get_widget( self, searchObj ):
		try:
			for i in self.objList:
				if str(i[0]) == searchObj:
					return i[1]
					
		except:
			return None

	def signal_autoconnect( self, dic ):
		for d in dic:
			for s in self.objSignalsList:
				if str(s[2]) == d:
					obj = self.get_widget(s[0])
					if s[1] == "clicked":
						obj.clicked = dic[d]
					elif s[1] == "toggled":
						obj.changed = dic[d]
					elif s[1] == "destroy":
						obj.destroy = dic[d]
					else:
						print "signal_autoconnect error!!"+str(s)+\
							" not connected eleGlade not support it :(\n"+\
							" signal name:"+str(s[1])+"\n"+\
							"----------------"


def XML(filename):
	doc = xml.dom.minidom.parse( filename )
	elementary.init()
	glade = doc.getElementsByTagName("glade-interface")
	for i in glade:
		buildElementsFromXml( i )

	global objectsList
	global objectsSignalsList
	Deb( objectsSignalsList )
	return eTree( objectsList, objectsSignalsList )




