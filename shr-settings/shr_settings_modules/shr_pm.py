
import module, os, re, sys, elementary
import threading
import dbus
from dbus.mainloop.glib import DBusGMainLoop

class Pm(module.AbstractModule):
    def name(self):
        return "Power"

    def poweroffbtClick(self, obj, event):
        iface = get_usage_iface()
        if iface:
            iface.Shutdown()
        else:
            print "Shutdown by dbus cmd error"

    def restartbtClick(self, obj, event):
        iface = get_usage_iface()
        if iface:
            iface.Reboot()
        else:
            print "Reboot by dbus cmd error"

    def get_usage_iface(self):
        try:
            DBusGMainLoop(set_as_default=True)
            bus = dbus.SystemBus()
            usage_obj = bus.get_object( 'org.freesmartphone.ousaged', '/org/freesmartphone/Usage' )
            return dbus.Interface(usage_obj, 'org.freesmartphone.Usage')
            
            #self.usage_iface.Suspend()
            
        except:
            print "suspend by dbus cmd error"
            return 0


        

    def suspendbtClick(self, obj, event):
        iface = get_usage_iface()

        if os.popen("cat /proc/cpuinfo | grep GTA01").read() == "GTA01\n":
            print "suspend for GTA01"
            os.system("/etc/init.d/fso-gsmd stop")
            time.sleep(0)


            if iface:
                iface.Suspend()
            else:
                print "suspend by dbus cmd error2"

            time.sleep(0)
            os.system("/etc/init.d/fso-gsmd start")
        else:
            if iface:
                iface.Suspend()
            else:
                print "suspend by dbus cmd error2"
            
    def refreshAct(self):
        self.apml.label_set( os.popen("apm").read().replace("\n","") )
        vol = "1234"
        temp = "1234"
        cur = "1234"


        vol =  open("/sys/class/power_supply/bat-th-gta01/voltage_now","r").readline().replace("\n","")
        temp = open("/sys/class/power_supply/bat-th-gta01/temp","r").readline().replace("\n","")
        cur =  int(open("/sys/class/power_supply/bat-th-gta01/current_now","r").readline().replace("\n",""))/1000
        sta = open("/sys/class/power_supply/bat-th-gta01/status","r").readline().replace("\n","")

        self.voll.label_set("Voltage: "+str(vol)[0]+"."+str(vol)[1]+str(vol)[2]+str(vol)[3]+" V")
        self.templ.label_set("Temperature: "+str(temp)[0]+str(temp)[1]+"."+str(temp)[2]+" 'C")
        self.curl.label_set("Current: "+str(cur)+" mA")
        self.stal.label_set("Status: "+sta)

    def refreshbtClick(self, obj, event):
        self.refreshAct()

    def view(self, win):
        self.win = win
        
        self.box1 = elementary.Box(win)


        boxOp = elementary.Box(win)
        boxOp.size_hint_weight_set(1.0, 1.0)
        boxOp.size_hint_align_set(-1.0, 0.0)

        self.apml = elementary.Label(win)
    	self.apml.size_hint_align_set(-1.0, 0.0)
    	self.apml.show()
    	boxOp.pack_start(self.apml)

    	self.apml = elementary.Label(win)
    	self.apml.size_hint_align_set(-1.0, 0.0)
    	self.apml.show()
    	boxOp.pack_start(self.apml)


        fo = elementary.Frame(win)
        fo.label_set( "apm:" )
        fo.size_hint_align_set(-1.0, 0.0)
        fo.show()
        fo.content_set( boxOp )

        boxOp.show()
        self.box1.pack_end(fo)



        box1p = elementary.Box(win)
        box1p.size_hint_weight_set(1.0, 1.0)
        box1p.size_hint_align_set(-1.0, 0.0)

        self.stal = elementary.Label(win)
    	self.stal.size_hint_align_set(-1.0, 0.0)
    	self.stal.show()
    	box1p.pack_start(self.stal)

        self.voll = elementary.Label(win)
    	self.voll.size_hint_align_set(-1.0, 0.0)
    	self.voll.show()
    	box1p.pack_start(self.voll)

        self.templ = elementary.Label(win)
    	self.templ.size_hint_align_set(-1.0, 0.0)
    	self.templ.show()
    	box1p.pack_start(self.templ)

        self.curl = elementary.Label(win)
    	self.curl.size_hint_align_set(-1.0, 0.0)
    	self.curl.show()
    	box1p.pack_start(self.curl)

        fo = elementary.Frame(win)
        fo.label_set( "battery:" )
        fo.size_hint_align_set(-1.0, 0.0)
        fo.show()
        fo.content_set( box1p )

        box1p.show()
        self.box1.pack_end(fo)


        startbt = elementary.Button(win)
        startbt.clicked = self.refreshbtClick
        startbt.label_set("refresh")
        startbt.size_hint_align_set(-1.0, 0.0)
        startbt.show()
        self.box1.pack_end(startbt)


        self.refreshAct()





        box2p = elementary.Box(win)
        box2p.size_hint_weight_set(1.0, 1.0)
        box2p.size_hint_align_set(-1.0, 0.0)

        poweroffbt = elementary.Button(win)
        poweroffbt.clicked = self.suspendbtClick
        poweroffbt.label_set("power off")
        poweroffbt.size_hint_align_set(-1.0, 0.0)
        poweroffbt.show()
        box2p.pack_end(poweroffbt)

        restartbt = elementary.Button(win)
        restartbt.clicked = self.restartbtClick
        restartbt.label_set("restart")
        restartbt.size_hint_align_set(-1.0, 0.0)
        restartbt.show()
        box2p.pack_end(restartbt)

        suspendbt = elementary.Button(win)
        suspendbt.clicked = self.suspendbtClick
        suspendbt.label_set("suspend")
        suspendbt.size_hint_align_set(-1.0, 0.0)
        suspendbt.show()
        box2p.pack_end(suspendbt)


        fo = elementary.Frame(win)
        fo.label_set( "actions:" )
        fo.size_hint_align_set(-1.0, 0.0)
        fo.show()
        fo.content_set( box2p )

        box2p.show()
        self.box1.pack_end(fo)






        return self.box1



