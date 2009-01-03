import elementary, module
import dbus
from dbus.mainloop.glib import DBusGMainLoop

class Profile(module.AbstractModule):
    name = "Profile"


    def defbt_click(self, obj, event):
        if self.stan!="":
            self.pr_iface.SetProfile('default')
            self.cur.label_set('default')

    def silbt_click(self, obj, event):
        if self.stan!="":
            self.pr_iface.SetProfile('silent')
            self.cur.label_set('silent')


    def createView(self):

        self.stan = ""
        try:
            DBusGMainLoop(set_as_default=True)
            bus = dbus.SystemBus()
            pr_device_obj = bus.get_object( "org.freesmartphone.opreferencesd", "/org/freesmartphone/Preferences" )
            self.pr_iface = dbus.Interface(pr_device_obj, "org.freesmartphone.Preferences" )
            self.stan = self.pr_iface.GetProfile()
            
        except:
            print "can't connect to dbus :/"


        boxh = elementary.Box(self.window)
        boxh.horizontal_set(True)
        la = elementary.Label(self.window)
        la.label_set("Current profile:")
        la.show()
        boxh.pack_start(la)
        self.cur = elementary.Label(self.window)
        if self.stan!="":
            self.cur.label_set(self.stan)
        else:
            self.cur.label_set("dbus error")
        boxh.pack_end(self.cur)
        self.cur.show()


        defbt = elementary.Button(self.window)
        defbt.clicked = self.defbt_click
        defbt.label_set("default" )
        defbt.size_hint_align_set(-1.0, 0.0)
        defbt.show()
        boxh.pack_end(defbt)

        silbt = elementary.Button(self.window)
        silbt.clicked = self.silbt_click
        silbt.label_set("silent" )
        silbt.size_hint_align_set(-1.0, 0.0)
        silbt.show()
        boxh.pack_end(silbt)


        return boxh
