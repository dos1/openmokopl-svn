
import module, os, re, sys, elementary

import dbus
from dbus.mainloop.glib import DBusGMainLoop

"""
source
- freesmartphone framework
http://git.freesmartphone.org/?p=specs.git;a=blob_plain;f=html/org.freesmartphone.GSM.Device.html;hb=HEAD
- dbus
http://74.125.77.132/search?q=cache:lrCoc3DSa0gJ:www.freesmartphone.org/index.php/Tutorials/GSM_python+python+dbus+%22org.freesmartphone.ogsmd%22&hl=pl&ct=clnk&cd=3&gl=pl&client=firefox-a
"""

class Button2( elementary.Button ):
    mOpeNr = ""
    def set_opeNr( self, mOpeNr ):
        self.mOpeNr = mOpeNr

    def get_opeNr( self ):
        return self.mOpeNr

class GSMstateContener:
    def __init__(self):
        self.dbus_state = 0
        try:
            DBusGMainLoop(set_as_default=True)
            bus = dbus.SystemBus()
            gsm_device_obj = bus.get_object( 'org.freesmartphone.ogsmd', '/org/freesmartphone/GSM/Device' )
            self.gsm_network_iface = dbus.Interface(gsm_device_obj, 'org.freesmartphone.GSM.Network')
            self.gsm_device_iface = dbus.Interface(gsm_device_obj, 'org.freesmartphone.GSM.Device')
            #test
            self.gsm_device_iface.GetAntennaPower()
            #test end
            self.dbus_state = 1
        except:
            self.dbus_state = 0
            print "GSM GSMstateContener [error] can't connect to dbus"

    def dbus_getState(self):
        return self.dbus_state

    def gsmdevice_getAntennaPower(self):
        if self.dbus_state==0:
            return 0
        else:
            try:
                tr = self.gsm_device_iface.GetAntennaPower()
            except:
                tr = 0
            return tr
    def gsmdevice_setAntennaPower(self, b):
        if self.dbus_state==1:
            self.gsm_device_iface.SetAntennaPower(b)

    def gsmnetwork_setRegisterWithProvider(self, b):
        if self.dbus_state==1:
            self.gsm_network_iface.RegisterWithProvider(int(b))

class Gsm(module.AbstractModule):
    def name(self):
        return "GSM"

    def destroy(self, obj, event, *args, **kargs):
        print "DEBUG: window destroy callback called! kabum!"
        #TODO - zamkniecie okna
        self.winope.hide()
        # to jest totalna proteza trzeba to poprawic
        
    def operatorSelect(self, obj, event, *args, **kargs):
        #os.popen("echo \"gsmnetwork.RegisterWithProvider( "+obj.get_opeNr()+" )\" | cli-framework", "r");
        print "GSM operatorSelect [info] ["+obj.get_opeNr()+"]"
        self.gsmsc.gsmnetwork_setRegisterWithProvider( obj.get_opeNr() )
        self.winope.hide()
        print "clik"

    def operatorsList(self, obj, event, *args, **kargs):
        self.opebt.label_set("Operators [search...]")
        
        print "Operators list\nStart query cli-framework\n-------"
        self.operatorsList = os.popen("echo \"gsmnetwork.ListProviders()\" | cli-framework", "r");
        #self.operatorsList = os.popen("cat /tmp/operators", "r");

        row = 1
        res = ""
        while 1:
            row+=1
            line = self.operatorsList.readline();
            if not line:
                break
            if row>=2:
                lineParse = line.replace(" ", "").replace(">>>", "").replace("[", "").replace("]", "").replace("),", ")")
                if len(lineParse) > 5:
                    res+= lineParse
                    print lineParse
        print "-------\nEnd query cli-framework"

        self.winope = elementary.Window("listProviders", elementary.ELM_WIN_BASIC)
        self.winope.title_set("List Providers")
        self.winope.autodel_set(True)

        self.bg = elementary.Background(self.winope)
        self.winope.resize_object_add(self.bg)
        self.bg.size_hint_weight_set(1.0, 1.0)
        self.bg.show()

        box0 = elementary.Box(self.winope)
        box0.size_hint_weight_set(1.0, 1.0)
        self.winope.resize_object_add(box0)
        box0.show()

        fr = elementary.Frame(self.winope)
        fr.label_set("List Providers")
        fr.size_hint_align_set(-1.0, 0.0)
        box0.pack_end(fr)
        fr.show()

        sc = elementary.Scroller(self.winope)
        sc.size_hint_weight_set(1.0, 1.0)
        sc.size_hint_align_set(-1.0, -1.0)
        box0.pack_end(sc)
        sc.show()

        cancelbt = elementary.Button(self.winope)
        cancelbt.clicked = self.destroy
        cancelbt.label_set("Cancel")
        cancelbt.size_hint_align_set(-1.0, 0.0)
        cancelbt.show()
        box0.pack_end(cancelbt)

        box1 = elementary.Box(self.winope)
        box1.size_hint_weight_set(1.0, -1.0)
        sc.content_set(box1)
        box1.show()


        resA = res.split("\n")
        btNr = 0
        for l in resA:
            line = l.split(",")
            if len(line)>2:
                opeAvbt = Button2(self.winope)
                if line[1]=="'current'":
                    add = " [current]"
                else :
                    add = "";
                btNr+= 1
                opeAvbt.label_set( line[2].replace("'","")+add )
                opeAvbt.set_opeNr( str(line[0].replace("(","")) )
                opeAvbt.clicked = self.operatorSelect
                opeAvbt.size_hint_align_set(-1.0, 0.0)
                opeAvbt.show()
                box1.pack_end(opeAvbt)

        self.opebt.label_set("Operators")
        self.winope.show()

    def GSMmodGUIupdate(self):
        self.ap = self.gsmsc.gsmdevice_getAntennaPower()

        self.toggle0.state_set( self.ap )
        if self.ap:
            self.opebt.show()
            self.toggle0.state_set( self.ap )
        else:
            self.opebt.hide()
            self.toggle0.state_set( self.ap )


    def toggle0bt(self, obj, event, *args, **kargs):
        if self.gsmsc.gsmdevice_getAntennaPower():
            print "GSM set off"
            self.gsmsc.gsmdevice_setAntennaPower(0)
            self.opebt.hide()
            obj.state_set( 0 )
        else:
            print "GSM set on"
            self.gsmsc.gsmdevice_setAntennaPower(1)
            self.opebt.show()
            obj.state_set( 1 )
        
        self.GSMmodGUIupdate()

    def view(self, win):
        self.gsmsc = GSMstateContener()
        
        box1 = elementary.Box(win)
        self.toggle0 = elementary.Toggle(win)
        self.toggle0.label_set("GSM antenna:")
        self.toggle0.size_hint_align_set(-1.0, 0.0)
        self.toggle0.states_labels_set("On","Off")
        self.toggle0.show()
        box1.pack_start(self.toggle0)
       
        if self.gsmsc.dbus_getState():

            self.opebt = elementary.Button(win)
            self.opebt.clicked = self.operatorsList
            self.opebt.label_set("Operators")
            self.opebt.size_hint_align_set(-1.0, 0.0)
            box1.pack_end(self.opebt)

            self.toggle0.changed = self.toggle0bt

            self.GSMmodGUIupdate()
        else:
            errlab = elementary.Label(win)
            errlab.label_set("can't connect to dbus")
            errlab.size_hint_align_set(-1.0, 0.0)
            errlab.show()
            box1.pack_end( errlab )
            print "GSM view [info] can't connect to dbus"
       
        return box1


