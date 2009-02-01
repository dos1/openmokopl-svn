
__author__="yoyo"
__date__ ="$Jan 22, 2009 11:03:36 PM$"

import os,sys,time
tStart = time.time()
def Deb( s ):
	#pass
	print "[eleGlade] ["+str( time.time()-tStart )+"] ["+str(s)+"]"

Deb("after import os,sys,time")

import elementary
import pprint
import xml.dom.minidom
from xml.dom.minidom import Node
Deb("after import xml,....")

"""
<raster> set align for label to 0.5 0.5
<raster> for all buttons set them to -1.0 -1.0
<raster> set weight for all to 1.0 1.0
<yoyo> I need tu understend align -1.0 0.5..... and weight ....
<raster> -1.0 for align == fill the area given
<raster> 0.0-1.0 is alignment (left to right, top to bottom)
<raster> 0.5 of course is centered
"""

def getPropertyFromWidget( p, name ):
	for b in p.childNodes:
		if str(b.localName) == "property":
			#Deb("getPropertyFromWidget: localName"+str(b.localName) )
			if b.getAttribute("name") == name:
				return str(b.childNodes[0].nodeValue)
	return ""

def getSignalFromWidget( window, objectsList, objectsSignalsList,  p, objName ):
	for b in p.childNodes:
		if str(b.localName) == "signal":
			#Deb( "getSignalFromWidget: localName"+str(b.localName) )
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
							Deb("packing expand false")
							obj.size_hint_weight_set(-1.0, -1.0)
						else:
							Deb( "packing expand true" )
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

def eleEntry( path, parentObj ):
	tr = elementary.Entry( parentObj )
	tr.single_line_set(True)
	#tr.single_line_set(False)
	tr.entry_set(getPropertyFromWidget(path[0].parentNode, "text"))
	#tr.label_set(searchForLabel(path))
	tr = packing ( tr, path )
	tr.show()
	return tr

def eleTextView( path, parentObj ):
	tr = elementary.Entry( parentObj )
	tr.single_line_set(True)
	tr.single_line_set(False)
	tr.entry_set(getPropertyFromWidget(path[0].parentNode, "text").replace("\n","<br>"))
	#tr.label_set(searchForLabel(path))
	tr = packing ( tr, path )
	tr.show()
	return tr

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
			Deb("eleFrame:["+str(i.getAttribute("name") )+"]")

		if str(i.localName) == "child" and child == 0:
			child+=1
		elif str(i.localName) == "child" and child == 1:
			for wid in i.childNodes:
				if str( wid.localName ) == "widget" :
					fr.label_set(  getPropertyFromWidget( wid, "label") )



	Deb( "-------------- frame --------------------" )

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



def eleToolbar( window, objectsList, objectsSignalsList, path, parentObj ):
	tr = elementary.Toolbar( parentObj )
	tr = packing ( tr, path )
	tr.show()

	for c in path:
		if str(c.localName) == "child":
			for w in c.childNodes:
				if str(w.localName) == "widget":
					item_label = str( getPropertyFromWidget(w, "label") )
					item_ico = str( getPropertyFromWidget(w, "icon") )
					item_name = w.getAttribute("id")
					for b in w.childNodes:
						#Deb( "b localName"+str(b.localName) )
						if str(b.localName) == "signal":
							item_sigName = b.getAttribute("name")
							item_handler = b.getAttribute("handler")
							#Deb("eleToolbar item_handler:"+str(item_handler) )
							break

					img = elementary.Icon( parentObj )
					img.file_set( item_ico )
					img.show()

					objectsList.append(
						[ item_name, img ]
						)
					objectsSignalsList.append(
						[ item_name, item_sigName, item_handler]
						)


					tr.item_add(
						img,
						item_label,
						None
						)


	"""
	img = elementary.Icon( parentObj )
	img.file_set("osmupdater.png")
	img.show()

	tr.item_add(
		img,
		"se text",
		"clicked"
		)
	"""

	return tr

def buildElementsFromXml( window, objectsList, objectsSignalsList, g, parentName = "", parentObj = "", frameParent = "" ):
	#Deb( "parsing child " )
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
				getSignalFromWidget( window, objectsList, objectsSignalsList, i, str(_id) )
				bg = elementary.Background(win)
				win.resize_object_add(bg)
				bg.size_hint_weight_set(1.0, 1.0)
				bg.show()

				for s in i.childNodes:
					buildElementsFromXml( window, objectsList, objectsSignalsList, s, _id , win )

			if _class == "GtkVBox":
				vbox = eleVBox( i.childNodes, parentObj )
				objectsList.append( [str(_id),vbox ] )
				if frameParent == 1:
					parentObj.content_set( vbox )
				else:
					if window == 0:
						parentObj.resize_object_add( vbox )
						window = 1
					else:
						parentObj.pack_end( vbox )

				for s in i.childNodes:
					buildElementsFromXml( window, objectsList, objectsSignalsList, s, parentName , vbox )


			if _class == "GtkHBox":
				hbox = eleHBox( i.childNodes, parentObj )
				objectsList.append( [str(_id),hbox] )
				if frameParent == 1:
					parentObj.content_set( hbox )
				else:
					parentObj.pack_end( hbox )
				for s in i.childNodes:
					buildElementsFromXml( window, objectsList, objectsSignalsList, s, parentName , hbox )

			if _class == "GtkScrolledWindow":
				sc = eleScroller( i.childNodes, parentObj )
				objectsList.append( [str(_id),sc ])
				if frameParent == 1:
					parentObj.content_set( sc )
				else:
					parentObj.pack_end( sc )
				for s in i.childNodes:
					buildElementsFromXml( window, objectsList, objectsSignalsList, s, parentName , sc, 1 )


			if _class == "GtkExpander":
				exp = eleFrame( i.childNodes, parentObj )
				objectsList.append( [str(_id),exp])
				parentObj.pack_end( exp )

				s = i.childNodes[5]
				Deb(  "expander: "+str(s.localName) )
				buildElementsFromXml( window, objectsList, objectsSignalsList, s, parentName , exp, 1 )


			if _class == "GtkButton":
				bt = eleButton(i.childNodes, parentObj)
				objectsList.append( [str(_id),bt])
				getSignalFromWidget( window, objectsList, objectsSignalsList, i, str(_id) )
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
					buildElementsFromXml( window, objectsList, objectsSignalsList, s, parentName , vp, 1 )

			if _class == "GtkLabel":
				lb = eleLabel(i.childNodes, parentObj)
				objectsList.append( [str(_id),lb])
				if frameParent == 1:
					parentObj.content_set( lb )
				else:
					parentObj.pack_end( lb )

			if _class == "GtkEntry":
				en = eleEntry(i.childNodes, parentObj)
				objectsList.append( [str(_id),en])
				if frameParent == 1:
					parentObj.content_set( en )
				else:
					parentObj.pack_end( en )

			if _class == "GtkTextView":
				en = eleTextView(i.childNodes, parentObj)
				objectsList.append( [str(_id),en])
				if frameParent == 1:
					parentObj.content_set( en )
				else:
					parentObj.pack_end( en )


			if _class == "GtkToolbar":
				tb = eleToolbar( window, objectsList, objectsSignalsList,  i.childNodes, parentObj)
				objectsList.append( [str(_id),tb])
				if frameParent == 1:
					parentObj.content_set( tb )
				else:
					parentObj.pack_end( tb )
			
			if _class == "GtkToggleButton":
				tb = eleToggle( i.childNodes, parentObj)
				objectsList.append( [str(_id),tb])
				getSignalFromWidget( window, objectsList, objectsSignalsList, i, str(_id) )
				parentObj.pack_end( tb )

	#Deb( "parsing child done" )

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
					Deb( "signal_autoconnect: [objname:"+str(s[0])+" signal:"+str(s[1])+" handler:"+str(s[2])+"]" )
					obj = self.get_widget(s[0])
					#print str(obj)
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
	Deb("XML start")
	doc = xml.dom.minidom.parse( filename )
	Deb("XML doc")
	elementary.init()
	Deb("XML init")
	glade = doc.getElementsByTagName("glade-interface")
	Deb("XML glade")

	window = 0
	objectsList = []
	objectsSignalsList = []

	for i in glade:
		buildElementsFromXml( window, objectsList, objectsSignalsList, i )

	
	Deb( "objectsSignalsList: ["+str(objectsSignalsList)+"]" )
	Deb( "objectsList: ["+str(objectsList)+"]" )
	Deb("XML end")
	return eTree( objectsList, objectsSignalsList )




