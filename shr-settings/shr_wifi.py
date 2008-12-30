import elementary, module, os, dbus

def getDbusObject (bus, busname , objectpath , interface):
        dbusObject = bus.get_object(busname, objectpath)
        return dbus.Interface(dbusObject, dbus_interface=interface)

class Wifi(module.AbstractModule):
    def name(self):
        return "WiFi"

    def enabled(self):
	if os.popen("cat /proc/cpuinfo | grep Hardware |  awk '{ print $3 }'").read()=="GTA01\n":
	    return 0
	else:
	    return 1
    
    def power_handle(self, obj, event):
        #if obj.state_get():
        wifipower = self.wifi.GetPower()
        self.wifi.SetPower(not(wifipower))
        obj.state_set(not(wifipower))


    def view(self, win):
        bus = dbus.SystemBus()
        self.wifi = getDbusObject (bus, "org.freesmartphone.odeviced", "/org/freesmartphone/Device/PowerControl/WiFi", "org.freesmartphone.Device.PowerControl")

        box1 = elementary.Box(win)
        toggle0 = elementary.Toggle(win)
        toggle0.label_set("WiFi radio:")
        toggle0.size_hint_align_set(-1.0, 0.0)
        toggle0.states_labels_set("On","Off")
	toggle0.changed = self.power_handle
        box1.pack_start(toggle0)
	toggle0.state_set(self.wifi.GetPower())
        toggle0.show()

        return box1
