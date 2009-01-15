
__author__="yoyo"
__date__ ="$Jan 15, 2009 2:40:18 PM$"


from threading import Thread
import threading
import time,sys,os,random
import pygame

import dbus
from dbus.mainloop.glib import DBusGMainLoop

import gobject 
import gtk







# ---------- need to by set for gta01 and gta02
sysfs_bat_online = "/sys/class/power_supply/bat-th-gta01/online"
sysfs_bat_capacity = "/sys/class/power_supply/bat-th-gta01/capacity"
# ---------- need to by set for gta01 and gta02








# HELPERS --------------------------------
def Deb( s ):
    print "[ "+time.ctime()+" (Debug) ]["+str(s)+"]"


def GetSurfaceCenter_x( surface ):
    return ((screenSize[0]/2)-(surface.get_width()/2))

# HELPERS --------------------------------









clock = pygame.time.Clock()
Deb("Pygame font init start")
pygame.font.init
pygame.font.init()
font160 = pygame.font.Font(None, 160)
font110 = pygame.font.Font(None, 110)
font40 = pygame.font.Font(None, 40)
font25 = pygame.font.Font(None, 25)
font15 = pygame.font.Font(None, 15)
Deb("Pygame font init start")

screenSize = [ 480, 640 ]

onBattery = 0
batteryCapa = 0

signalStre = 0
providerName = ""

idleStatus = ""

usage_iface = 0

lock = 0

Deb("Loading pixmaps start")
pix_bt_charg = pygame.image.load('charge.png')
pix_bt_low = pygame.image.load('low_battery.png')
pix_bg = [ \
    pygame.image.load('bg_virus.png'),
    pygame.image.load('bg_why.png'),
    pygame.image.load('bg_box.png'),
    pygame.image.load('bg.png')
    ]
pix_bg_top =  pygame.image.load('bg_mask_top.png')
pix_bg_unlock = pygame.image.load('bg_unlock.png')
pix_lock_out =  pygame.image.load('lock_out.png')

pix_gsm =  pygame.image.load('gsm.png')
pix_gsm_sig = [ \
    pygame.image.load('gsm_sig_0.png'),
    pygame.image.load('gsm_sig_20.png'),
    pygame.image.load('gsm_sig_40.png'),
    pygame.image.load('gsm_sig_60.png'),
    pygame.image.load('gsm_sig_80.png'),
    pygame.image.load('gsm_sig_100.png')
    ]
pix_battery =  pygame.image.load('battery.png')
Deb("Loading pixmaps end")








# GUI -------------------
class Monit(threading.Thread):
    def __init__(self, pixmap, monitTitle):
        Thread.__init__(self)

        Deb("Monit ("+monitTitle+") __init__ start")

        global clock
        global screenSize
        screen = pygame.display.set_mode( (screenSize) )
        #""", pygame.FULLSCREEN""" )
        pygame.display.set_caption(monitTitle)


        screen.fill( (0,0,0) )

        text_charging = font110.render(monitTitle, 1, (255,255,255))
        screen.blit( text_charging, \
            (GetSurfaceCenter_x(text_charging), 50 )
            )

        screen.blit( pixmap, \
            (GetSurfaceCenter_x(pixmap), 170 )
            )



        pygame.display.flip()

        displayTime = 600
        os.system("mplayer ./info.wav &")

        while displayTime > 0:

            event = pygame.event.poll()
            if event.type == pygame.MOUSEBUTTONUP:
                Deb("Monit ("+monitTitle+") __init__ click end monit")
                break

            displayTime-=1
            clock.tick(100)
            
        pygame.display.quit()
        Deb("Monit ("+monitTitle+") __init__ end")




class LockScreen(threading.Thread):
    def __init__(self):
        Thread.__init__(self)
        Deb("LockScreen __init__ start")
        self.bg_nr = random.randint(0,4)-1
        

    def run(self):
        Deb("LockScreen run() start")
        global lock
        lock = 1
        self.screen = pygame.display.set_mode( (screenSize) , pygame.FULLSCREEN )
        pygame.display.set_caption("lock")

        
        self.repeint()

        

        while lock:
            if idleStatus == "lock" and onBattery == 1:
                Deb("LockScreen ------------ put suspend -----------------")
                Deb("LockScreen ------------ "+time.ctime()+" -----------------")
                os.system("/etc/init.d/fso-gsmd stop")
                usage_iface.Suspend()
                os.system("sleep 6 && /etc/init.d/fso-gsmd stop &")
                Deb("LockScreen ------------ "+time.ctime()+" -----------------")
                Deb("LockScreen ------------ put suspend -----------------")


            event = pygame.event.poll()
            if event.type == pygame.MOUSEBUTTONUP:
                Deb("LockScreen __init__ click MOUSEBUTTONUP lock")
                if self.posibleUnlock == 1:
                    xm = event.pos[0]
                    ym = event.pos[1]
                    Deb("LockScreen MOUSEBUTTONUP at x["+str(xm)+"] y["+str(ym)+"]")
                    if xm>=self.x and xm<=(self.x+96) and  ym>=self.y and ym<=(self.y+96):
                        Deb("LockScreen unlock")
                        lock = 0
                        break
                    else:
                        self.repeint()


            if event.type == pygame.MOUSEBUTTONDOWN:
                Deb("LockScreen __init__ click MOUSEBUTTONDOWN lock")
                ym = event.pos[1]
                self.posibleUnlock = 0
                if ym > 580:
                    self.posibleUnlock = 1
                    Deb("LockScreen posible unlock")
                    self.x = random.randint(10,400)
                    self.y = random.randint(10,400)
                    Deb("LockScreen posible unlock at x["+str(self.x)+"] y["+str(self.y)+"]")
                    self.screen.blit( pix_lock_out, (self.x, self.y))
                    pygame.display.flip()
                else:
                    self.repeint()

            clock.tick(100)

        pygame.display.quit()
        lock = 0
        Deb("LockScreen run() end")
        







    def repeint(self):
        Deb("LockScreen repaint()")

        self.screen.fill((0,0,0))

        
        self.screen.blit( pix_bg[self.bg_nr], (GetSurfaceCenter_x(pix_bg[self.bg_nr]),0) )
        self.screen.blit( pix_bg_top, (0,0))
        self.screen.blit( pix_bg_unlock, (0,570))
        self.screen.blit( pix_gsm, (0,0))
        self.screen.blit( pix_battery, ((screenSize[0]-60),6))

        #signalStre
        pos = (40,12)
        #pix_gsm_sig
        if signalStre < 20 :
            self.screen.blit(pix_gsm_sig[0], pos)
        elif signalStre < 40 :
            self.screen.blit(pix_gsm_sig[1], pos)
        elif signalStre < 60 :
            self.screen.blit(pix_gsm_sig[2], pos)
        elif signalStre < 80 :
            self.screen.blit(pix_gsm_sig[3], pos)
        elif signalStre < 100 :
            self.screen.blit(pix_gsm_sig[4], pos)
        elif signalStre == 100 :
            self.screen.blit(pix_gsm_sig[5], pos)
            

        text_provider = font25.render(providerName, 1, (255,255,255))
        self.screen.blit( text_provider, \
            (GetSurfaceCenter_x(text_provider),2)
            )

        text_batCap = font25.render(str(batteryCapa)+"%", 1, (255,255,255))
        self.screen.blit( text_batCap, \
            ((screenSize[0]-96),2)
            )

        text_clock = font160.render(time.strftime("%H:%M"), 1, (255,255,255))
        self.screen.blit( text_clock, \
            (GetSurfaceCenter_x(text_clock), 30 )
            )

        text_data = font40.render(time.strftime("%Y-%m-%d"), 1, (255,255,255))
        self.screen.blit( text_data, \
            (GetSurfaceCenter_x(text_data), 140 )
            )

        pygame.display.flip()

        



# GUI -------------------


# DEMONS ----------------

class De_Battery(threading.Thread):
    def __init__(self):
        Thread.__init__(self)
        Deb("De_Battery __init__")

        global onBattery

        online = open(sysfs_bat_online).read().replace("\n", "")
        if online == "1":
            self.chargeStatus = 1
            onBattery = 0
        else:
            self.chargeStatus = 0
            onBattery = 1
        Deb("De_Battery self.chargeStatus :["+str(self.chargeStatus)+"]")

        global batteryCapa
        batteryCapa = int(open(sysfs_bat_capacity).read().replace("\n", ""))



        global signalStre
        global providerName
        """
        signalStre = 0
        providerName = ""
        """
        gsm_network = os.popen("mdbus -s org.freesmartphone.ogsmd /org/freesmartphone/GSM/Device org.freesmartphone.GSM.Network.GetStatus").read().split(',\n')
        for i in gsm_network:
            line = i.split("': ")
            name = line[0].replace(" ", "")
            if name == "'provider":
                providerName = line[1].replace("'", "")
            if name == "'strength":
                signalStre = int(line[1].replace("}",""))

        Deb("De_Battery providerName: "+providerName)
        Deb("De_Battery signalStre: "+str(signalStre))

        self.resumeLockAfterCall = 0

        self.screenRotate = 0

    def oevent( self, name, action, seconds):
        Deb("De_Battery oevent signal----------")
        Deb("De_Battery oevent name :["+str(name)+"]")
        Deb("De_Battery oevent action :["+str(action)+"]")
        Deb("De_Battery oevent seconds :["+str(seconds)+"]")

        if name == "AUX" and action == "released" and seconds == 0:
            global lock
            Deb("De_Battery lock status:["+str(lock)+"]")
            if lock == 0:
                Deb("De_Battery lock screen")
                self.lock = LockScreen()
                self.lock.start()

        if name == "AUX" and action == "released" and seconds == 1:
            Deb("De_Battery rotate")
            if self.screenRotate == 0:
                self.screenRotate = 1
            else:
                self.screenRotate = 0
            os.system("xrandr -display :0 -o "+str(self.screenRotate))

        if name == "USB":
            if action == "released":
                self.chargeStatus = 0
            elif action == "pressed":
                self.chargeStatus = 1
                if lock == 0:
                    monit = Monit( pix_bt_charg, "Charging...")
                    gobject.idle_add( monit.start )
                else:
                    os.system("mplayer ./info.wav &")
                time.sleep(1)


        


    def capacity(self, value):
        Deb("De_Battery capacity signal--------------")
        Deb("De_Battery capacity signal :["+str(value)+"]")
        global batteryCapa
        batteryCapa = int(value)

    def gsmNetwork(self,value):
        Deb("De_Battery gsmNetwork signal--------------")
        Deb("De_Battery gsmNetwork signal :["+str(value)+"]")
        global signalStre
        signalStre = int(value)

        if value < 65 and self.chargeStatus == 0:
            if lock == 0:
                monit = Monit( pix_bt_low, "Low battery!")
                gobject.idle_add( monit.start )
            else:
                os.system("mplayer ./info.wav &")
            time.sleep(1)

    def callincomming(self, name, action, seconds):
        Deb("De_Battery callincomming signal----------")
        Deb("De_Battery callincomming name :["+str(name)+"]")
        Deb("De_Battery callincomming action :["+str(action)+"]")
        Deb("De_Battery callincomming seconds :["+str(seconds)+"]")
        if action == "incoming":
            global lock
            if lock == 1:
                self.resumeLockAfterCall = 1
            else:
                self.resumeLockAfterCall = 0
            lock = 0
            Deb("De_Battery callincomming set global lock = 0")
        elif action == "release" and self.resumeLockAfterCall == 1:
            if lock == 0:
                Deb("De_Battery callincomming resumeLockAfterCall")
                self.lock = LockScreen()
                self.lock.start()
        

class De_brightness(threading.Thread):
    def stateChange(self,name):
        Deb("De_brightness stateChange signal------------")
        Deb("De_brightness stateChange signal :["+str(name)+"]")
        global idleStatus
        idleStatus = str(name)
        


        
# DEMONS ----------------

if __name__ == "__main__":
    Deb("pylock Start")

   

    
    Deb("pylock init main dbus loop")
    DBusGMainLoop(set_as_default=True)
    gobject.threads_init()
    bus = dbus.SystemBus()

    Deb("pylock getting dbus usage interface")
    usage_obj = dbus.get_object( 'org.freesmartphone.ousaged', '/org/freesmartphone/Usage' )
    usage_iface = dbus.Interface(usage_obj, 'org.freesmartphone.Usage')
    Deb("pylock getting dbus usage interface got it :)")

    Deb("pylock d_battery")
    d_battery = De_Battery()
    Deb("pylock d_battery.capacity")
    bus.add_signal_receiver(d_battery.capacity, dbus_interface="org.freesmartphone.Device.PowerSupply",     signal_name="Capacity")
    Deb("pylock d_battery.oevent")
    bus.add_signal_receiver(d_battery.oevent, dbus_interface="org.freesmartphone.Device.Input",     signal_name="Event")
    Deb("pylock d_battery.oevent")
    bus.add_signal_receiver(d_battery.oevent, dbus_interface="org.freesmartphone.Device.Input",     signal_name="Event")
    Deb("pylock d_battery.callincomming")
    bus.add_signal_receiver(d_battery.callincomming, dbus_interface="org.freesmartphone.GSM.Call",     signal_name="CallStatus")
    Deb("pylock d_battery make idle")
    gobject.idle_add( d_battery.start )


    Deb("pylock d_brigh")
    d_brigh = De_brightness()
    Deb("pylock d_brigh.stateChange")
    bus.add_signal_receiver( d_brigh.stateChange, dbus_interface="org.freesmartphone.Device.IdleNotifier",     signal_name="State")
    Deb("pylock d_brigh make idle")
    gobject.idle_add( d_brigh.start )

    

    gtk.main()

    Deb("pylock End")
    
