#!/usr/bin/env python
import elementary, os
import edje
import evas
import dbus
import e_dbus



class Button2(elementary.Button):
    def set_modules(self, modules):
        self.modules = modules
    def get_modules(self):
        return self.modules



class ModulesWindow:
    def __init__(self):
        print "1"
        self.win2 = elementary.Window("settingsMods", elementary.ELM_WIN_BASIC)
        print "2"
        self.win2.title_set("Settings modules")
        print "3"
        self.win2.destroy = self.destroy2
        
    def makeGui(self,  modulesList):
        from shr_settings_modules import shr_gsm, shr_device_timeouts,shr_pm, shr_bt, shr_wifi, shr_gprs, shr_usb, shr_clock, shr_profile, shr_services, shr_misc, shr_test

        mainloop = e_dbus.DBusEcoreMainLoop()
        #dbus_session = dbus.SessionBus(mainloop=self.mainloop) - we don't need atm
        dbus_system = dbus.SystemBus(mainloop=mainloop)

        self.bg2 = elementary.Background(self.win2)
        self.win2.resize_object_add(self.bg2)
        self.bg2.size_hint_weight_set(1.0, 1.0)
        self.bg2.show()


        box02 = elementary.Box(self.win2)
        box02.size_hint_weight_set(1.0, 1.0)
        self.win2.resize_object_add(box02)
        box02.show()



    #    toolbar = elementary.Toolbar(win)
    #    box0.pack_start(toolbar)
    #    toolbar.show()

        sc2 = elementary.Scroller(self.win2)
        sc2.size_hint_weight_set(1.0, 1.0)
        sc2.size_hint_align_set(-1.0, -1.0)
        box02.pack_end(sc2)
        sc2.show()

        quitbt2 = elementary.Button(self.win2)
        quitbt2.clicked = self.destroy2
        quitbt2.label_set("Quit")
        quitbt2.size_hint_align_set(-1.0, 0.0)
        quitbt2.show()
        box02.pack_end(quitbt2)


        box12 = elementary.Box(self.win2)
        box12.size_hint_weight_set(1.0, -1.0)
        sc2.content_set(box12)
        box12.show()



        print "1"
        for mod in modulesList:
            print "2"
            print "loading %s" % mod
            print "3"
            mod2 = mod(self.win2, dbus_system);
            print "4"
            if mod2.isEnabled():
                print "5"
                frame = elementary.Frame(self.win2)

                frame.label_set(mod2.getName()+" settings")
                box12.pack_end(frame)
                frame.size_hint_align_set(-1.0, 0.0)
                frame.show()

                cont = mod2.createView()
                if cont != None:
                    frame.content_set(cont)
                    cont.show()
                else:
                    print " error! module %s method createView() return's nothing!" % mod2

        win2.show()

    def destroy2(self,obj, event, *args, **kargs):
        self.win2.hide()





class MainWindow:

    def destroy(self, obj, event, *args, **kargs):
        print "DEBUG: window destroy callback called! kabum!"
        elementary.exit()

    def displayModulesWin(self, obj,event):
        #odulesWindow:
        #def makeGui(self, dbus_system, modules):
        ModulesWindow().makeGui(  obj.get_modules() )

    def __init__(self):
        self.win = elementary.Window("settings", elementary.ELM_WIN_BASIC)
        self.win.title_set("Settings")
        self.win.destroy = self.destroy

        #dbus init:
        #as in exposure.py:
       

        bg = elementary.Background(self.win)
        self.win.resize_object_add(bg)
        bg.size_hint_weight_set(1.0, 1.0)
        bg.show()

        box0 = elementary.Box(self.win)
        box0.size_hint_weight_set(1.0, 1.0)
        self.win.resize_object_add(box0)
        box0.show()



    #    toolbar = elementary.Toolbar(win)
    #    box0.pack_start(toolbar)
    #    toolbar.show()

        sc = elementary.Scroller(self.win)
        sc.size_hint_weight_set(1.0, 1.0)
        sc.size_hint_align_set(-1.0, -1.0)
        box0.pack_end(sc)
        sc.show()

        quitbt = elementary.Button(self.win)
        quitbt.clicked = self.destroy
        quitbt.label_set("Quit")
        quitbt.size_hint_align_set(-1.0, 0.0)
        quitbt.show()
        box0.pack_end(quitbt)

        box1 = elementary.Box(self.win)
        box1.size_hint_weight_set(1.0, -1.0)
        sc.content_set(box1)
        box1.show()

        #loading modules

        from shr_settings_modules import shr_gsm, shr_device_timeouts,shr_pm, shr_bt, shr_wifi, shr_gprs, shr_usb, shr_clock, shr_profile, shr_services, shr_misc, shr_test

        dirs = [    ["bluetooth","ico_bt_32_32.png",            [ shr_bt.Bt ] ],
                    ["services","ico_initd_32_32.png",         [ shr_services.Services ] ],
                    ["profiles","ico_profile_32_32.png",       [ shr_profile.Profile ] ],
                    ["clock","ico_timeset_32_32.png",       [ shr_clock.Clock ] ],
                    ["GSM","ico_gsm_32_32.png",           [ shr_gsm.Gsm ] ],
                    ["power manager","ico_powermanager_32_32.png",  [ shr_pm.Pm ] ],
                    ["time out","ico_timeout_32_32.png",       [ shr_device_timeouts.Timeouts ] ],
                    ["usb","ico_usb_32_32.png",           [ shr_usb.Usb ] ],
                    ["others", "",                  [ shr_wifi.Wifi, shr_gprs.Gprs, shr_misc.Misc, shr_test.Test ] ]
            ]


        for d in dirs:
            bt = Button2(self.win)
            bt.set_modules( d[1] )

            bt.clicked = self.displayModulesWin
            bt.size_hint_align_set(-1.0, 0.0)
            bt.label_set( str(d[0]) )
            bt.show()


            try:
                f = open("data/"+str(d[1]), "r")
                ic = elementary.Icon(self.win)
                ic.file_set("data/"+str(d[1]) )
                ic.scale_set(0, 0)
                bt.icon_set(ic)
                ic.show()
            except:
                bt.label_set( str(d[0]) )

            box1.pack_end(bt)




        #for mod in modules:
        #    print "loading %s" % mod
        #    load_module(mod, win, dbus_system)

        #end of loading modules



        self.win.show()
        elementary.run()
        elementary.shutdown()

if __name__ == "__main__":
    elementary.init()
    MainWindow()
    

    