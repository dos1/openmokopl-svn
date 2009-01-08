import time, dbus
import module
import elementary, ecore
import os

"""
- gta01
/sys/devices/platform/s3c2410-i2c/i2c-adapter/i2c-0/0-0008/neo1973-pm-bt.0/
- gta02
/sys/devices/platform/s3c2440-i2c/i2c-adapter/i2c-0/0-0073/neo1973-pm-bt.0/

"""
btModels = [ \
"/sys/devices/platform/s3c2410-i2c/i2c-adapter/i2c-0/0-0008/neo1973-pm-bt.0",
"/sys/devices/platform/s3c2440-i2c/i2c-adapter/i2c-0/0-0073/neo1973-pm-bt.0",
"/sys/bus/platform/devices/neo1973-pm-bt.0"]

class SimMstateContener:
    def __init__(self, bus):
        self.state = 0
        try:
            gsm_sim_obj = bus.get_object( 'org.freesmartphone.ogsmd', '/org/freesmartphone/GSM/Device' )
            self.gsm_sim_iface = dbus.Interface(gsm_sim_obj, 'org.freesmartphone.GSM.SIM')
            #self.gsm_sim_iface.getSimInfo()
            self.state = 1
            print "SimMstateContener can connect to dbus"
        except:
            self.state = 0
            print "SimMstateContener can't connect to dbus"

    def getDbusState(self):
        return self.state

    def getSimInfo(self):
        if self.state == 0:
            return 0
        else:
            return self.gsm_sim_iface.GetSimInfo()

    def ListPhonebooks(self):
        if self.state == 0:
            return 0
        else:
            return self.gsm_sim_iface.ListPhonebooks()

    def GetPhonebookInfo(self, a):
        if self.state == 0:
            return 0
        else:
            return self.gsm_sim_iface.GetPhonebookInfo(a)


    def GetMessagebookInfo(self):
        if self.state == 0:
            return 0
        else:
            return self.gsm_sim_iface.GetMessagebookInfo()


    def MessageBookClean(self):
        messageMax = self.GetMessagebookInfo()['last']
        print "MessageBookClean max: "+str(messageMax)
        for i in range(1, (messageMax+1), 1):
            print "remove id: "+str(i)
            try:
                self.gsm_sim_iface.DeleteMessage(i)
            except:
                pass
        print "DONE"

    def getService(self):
        ser = os.popen("ps -A | grep hci").read().replace("\n","")
        if ser != "":
            return 1
        else:
            return 0

    def getServiceObex(self):
        ser = os.popen("ps -A | grep obexftpd").read().replace("\n","")
        if ser != "":
            return 1
        else:
            return 0
        

    def setPower(self, b ):
        print "BT BtMstateContener setPower [inf] "+self.model
        if b==0:
            print "BT BtMstateContener setPower [inf] turn off bt by sysfs"
            #print "stop /etc/init.d/bluetooth"
            #os.system("/etc/init.d/bluetooth stop")
            #time.sleep(1)

            print "power_on"
            os.system("echo "+str(b)+" > "+btModels[2]+"/power_on")

            print "sleep"
            time.sleep(1)
        
            print "reset"
            os.system("echo 1 > "+btModels[2]+"/reset")
            

        else:
            print "BT BtMstateContener setPower [inf] turn on bt by sysfs"
            print "power_on"
            os.system("echo "+str(b)+" > "+btModels[2]+"/power_on")

            if self.model == "gta02":
                print "sleep"
                time.sleep(1)

                print "reset"
                os.system("echo 0 > "+btModels[2]+"/reset")

            #time.sleep(1)
            #print "start /etc/init.d/bluetooth"
            #os.system("/etc/init.d/bluetooth start")

        

    def getPower(self):
        if self.model=="gta01":
            f0 = open(btModels[2]+"/power_on", "r")
        elif self.model=="gta02":
            f0 = open(btModels[2]+"/power_on", "r")
        elif self.model=="":
            return self.state

        while f0:
            line = f0.readline()
            if not line:
                f0.close()
                break
            else:
                self.state = int(line)
        return self.state

    def setVisibility(self, b):
        if b:
            print "hciconfig hci0 piscan"
            os.system("hciconfig hci0 up")
            os.system("hciconfig hci0 piscan")
        else:
            print "hciconfig hci0 pscan"
            os.system("hciconfig hci0 up")
            os.system("hciconfig hci0 pscan")

    def getVisibility(self):
        piscan = os.popen("hciconfig dev")
        self.visible = -1
        self.iscan = 0
        self.pscan = 0

        s = 1
        while s:
            line = piscan.readline()
            if not line:
                break
            else:
                s = line.split(" ")
                self.visible = 0
                for i in s:
                    if i=="ISCAN":
                        self.iscan = 1
                    elif i=="PSCAN":
                        self.pscan = 1

        if self.iscan==1:
            return 1
        return 0
        


class Sim(module.AbstractModule):
    name = "SIM"
    section = "Connectivity"

    def BtmodGUIupdate(self):
        s = self.btmc.getPower()
        v = self.btmc.getVisibility()
        ser = self.btmc.getService()
        obex = self.btmc.getServiceObex()
        print "BT BtmodGUIupdate [info] power:"+str(s)+"; visibility:"+str(v)+" services:"+str(ser)+" obxeftpd:"+str(obex)
        if s == 1:
            self.toggle1.show()
            if v:
                self.toggle1.state_set(1)
            else:
                self.toggle1.state_set(0)

            if ser:
                self.toggle2.state_set(1)
            else:
                self.toggle2.state_set(0)

            self.toggle0.state_set( 1 )

            self.toggle2.show()
        else:
            self.toggle1.hide()
            self.toggle2.hide()
            self.toggle0.state_set( 0 )

        self.toggle3.state_set( obex )

        if self.guiUpdate:
            ecore.timer_add( 5.4, self.BtmodGUIupdate)

    def toggle0Click(self, obj, event, *args, **kargs):
#        if self.btmc.getPower():
	if self.btmc.getPower()==obj.state_get():
		return 0
	if obj.state_get()==0:
            print "Bt toggle0Click BT set OFF"
            self.btmc.setPower( 0 )
            self.toggle1.hide()
        else:
            print "Bt toggle0Click BT set ON"
            self.btmc.setPower( 1 )
            self.toggle1.show()

        
        

    def toggle1Click(self, obj, event, *args, **kargs):
        print "BT toggle1Cleck set Visibility"
        if self.btmc.getVisibility()==obj.state_get():
            return 0
    #        s = self.btmc.getVisibility()
    #        print str(s)
    #        if s:
        if obj.state_get()==0:
            print "Turn off"
            self.btmc.setVisibility(0)
        else:
            print "Turn on"
            self.btmc.setVisibility(1)

    def toggle2Click(self, obj, event, *args, **kargs):
        print "BT toggle2Cleck set on off spi hci servis"
        if self.btmc.getService()==obj.state_get():
            return 0
    #        s = self.btmc.getVisibility()
    #        print str(s)
    #        if s:
        if obj.state_get()==0:
            print "Turn off"
            os.system("/etc/init.d/bluetooth stop")
        else:
            print "Turn on"
            os.system("/etc/init.d/bluetooth start")


    def toggle3Click(self, obj, event, *args, **kargs):
        print "BT toggle3Cleck set on off obexftpd servis"
        if self.btmc.getServiceObex()==obj.state_get():
            return 0
    #        s = self.btmc.getVisibility()
    #        print str(s)
    #        if s:
        if obj.state_get()==0:
            print "Turn off"
            os.system("killall -9 obexftpd")
        else:
            print "Turn on"
            os.system("cd /tmp && obexftpd -b -c /tmp &")

    def cleanMessageBookClick(self, obj, event):
        self.simmc.MessageBookClean()


    def createView(self):
        self.guiUpdate = 1
        
        self.simmc = SimMstateContener( self.dbus )
        print "3"
        print "sim dbus"+str(self.simmc.getDbusState())
        print "4"

        box1 = elementary.Box(self.window)
        print "5"

        if self.simmc.getDbusState==0:
            label =elementary.Label(self.window)
            label.label_set("can't find file in sysfs")
            label.size_hint_align_set(-1.0, 0.0)
            label.show()
            box1.pack_start(label)
        else:
            simInfo = self.simmc.getSimInfo()
            frameInfo = elementary.Frame(self.window)
            frameInfo.label_set("SIM information:")
            box1.pack_end(frameInfo)
            frameInfo.size_hint_align_set(-1.0, 0.0)
            frameInfo.show()
            
            boxInfo = elementary.Box(self.window)
            frameInfo.content_set(boxInfo)
            
            for s in simInfo:
                if s != "subscriber_numbers":
                    boxS = elementary.Box(self.window)
                    boxS.horizontal_set(True)
                    boxS.size_hint_align_set(-1.0, 0.0)
                    boxS.show()

                    labelN =elementary.Label(self.window)
                    labelN.label_set(str(s)+":")
                    labelN.size_hint_align_set(-1.0, -1.0)
                    labelN.size_hint_weight_set(1.0, 1.0)
                    labelN.show()
                    boxS.pack_start(labelN)

                    labelV =elementary.Label(self.window)
                    labelV.size_hint_align_set(-1.0, 0.0)
                    labelV.label_set( str( simInfo[s] ) )
                    labelV.show()
                    boxS.pack_end(labelV)

                    boxInfo.pack_start( boxS )

            phoneBooks = self.simmc.ListPhonebooks()
            for b in phoneBooks:
                #frame
                frameBook = elementary.Frame(self.window)
                frameBook.label_set("Book "+b+":")
                box1.pack_end(frameBook)
                frameBook.size_hint_align_set(-1.0, 0.0)
                frameBook.show()

                boxBook = elementary.Box(self.window)
                boxBook.show()
                frameBook.content_set(boxBook)


                print "phoneBookInfo: "+b
                phoneBookInfo = self.simmc.GetPhonebookInfo( b )
                for i in phoneBookInfo:
                    print "phoneBookInfo: "+b+"; "+i
                    #info state
                    boxS = elementary.Box(self.window)
                    boxS.horizontal_set(True)
                    boxS.size_hint_align_set(-1.0, 0.0)
                    boxS.show()

                    labelN =elementary.Label(self.window)
                    try:
                        labelN.label_set(str(i)+":")
                    except:
                        pass
                    labelN.size_hint_align_set(-1.0, -1.0)
                    labelN.size_hint_weight_set(1.0, 1.0)
                    labelN.show()
                    boxS.pack_start(labelN)

                    labelV =elementary.Label(self.window)
                    labelV.size_hint_align_set(-1.0, 0.0)
                    try:
                        labelV.label_set( str( phoneBookInfo[i] ) )
                    except:
                        pass
                    labelV.show()
                    boxS.pack_end(labelV)

                    boxBook.pack_start( boxS )

            print "phoneBookInfo --------- DONE"

            """
            # actions
            boxS = elementary.Box(self.window)
            boxS.horizontal_set(True)
            boxS.size_hint_align_set(-1.0, 0.0)
            boxS.show()

            # backup TODO
            backupbt = elementary.Button(self.window)
            #backupbt.clicked = self.destroy2
            backupbt.label_set("backup")
            backupbt.size_hint_align_set(-1.0, 0.0)
            backupbt.show()
            boxS.pack_end(backupbt)

            # clear TODO
            cleanbt = elementary.Button(self.window)
            #backupbt.clicked = self.destroy2
            cleanbt.label_set("clean")
            cleanbt.size_hint_align_set(-1.0, 0.0)
            cleanbt.show()
            boxS.pack_end(cleanbt)

            boxBook.pack_end( boxS )
            """
            print "1"
            # message book info

            messBookInfo = self.simmc.GetMessagebookInfo()
            print "2"
            frameBook = elementary.Frame(self.window)
            print "3"
            frameBook.label_set("Message book:")
            box1.pack_end(frameBook)
            frameBook.size_hint_align_set(-1.0, 0.0)
            frameBook.show()

            boxBook = elementary.Box(self.window)
            boxBook.show()
            frameBook.content_set(boxBook)
            
            for m in messBookInfo:
                boxS = elementary.Box(self.window)
                boxS.horizontal_set(True)
                boxS.size_hint_align_set(-1.0, 0.0)
                boxS.show()

                labelN =elementary.Label(self.window)
                labelN.label_set(str(m)+":")
                labelN.size_hint_align_set(-1.0, -1.0)
                labelN.size_hint_weight_set(1.0, 1.0)
                labelN.show()
                boxS.pack_start(labelN)

                labelV =elementary.Label(self.window)
                labelV.size_hint_align_set(-1.0, 0.0)
                labelV.label_set( str( messBookInfo[m] ) )
                labelV.show()
                boxS.pack_end(labelV)

                boxBook.pack_start( boxS )


            # actions
            boxS = elementary.Box(self.window)
            boxS.horizontal_set(True)
            boxS.size_hint_align_set(-1.0, 0.0)
            boxS.show()
            """
            # backup TODO
            backupbt = elementary.Button(self.window)
            #backupbt.clicked = self.destroy2
            backupbt.label_set("backup")
            backupbt.size_hint_align_set(-1.0, 0.0)
            backupbt.show()
            boxS.pack_end(backupbt)
            """
            # clear TODO
            cleanbt = elementary.Button(self.window)
            cleanbt.clicked = self.cleanMessageBookClick
            cleanbt.label_set("clean")
            cleanbt.size_hint_align_set(-1.0, 0.0)
            cleanbt.show()
            boxS.pack_end(cleanbt)

            boxBook.pack_end( boxS )
            

            

            """
            self.toggle0 = elementary.Toggle(self.window)
            self.toggle0.label_set("Bluetooth radio:")
            self.toggle0.size_hint_align_set(-1.0, 0.0)
            self.toggle0.states_labels_set("On","Off")
            box1.pack_start(self.toggle0)
            self.toggle0.show()
            self.toggle0.changed = self.toggle0Click

            self.toggle1 = elementary.Toggle(self.window)
            self.toggle1.label_set("Visibility")
            self.toggle1.size_hint_align_set(-1.0, 0.0)
            self.toggle1.states_labels_set("On","Off")
            self.toggle1.state_set(vi)
            box1.pack_end(self.toggle1)
            self.toggle1.changed = self.toggle1Click


            
            self.toggle2 = elementary.Toggle(self.window)
            self.toggle2.label_set("Services (spi, hci):")
            self.toggle2.size_hint_align_set(-1.0, 0.0)
            self.toggle2.states_labels_set("On","Off")
            box1.pack_end(self.toggle2)
            self.toggle2.changed = self.toggle2Click


            self.toggle3 = elementary.Toggle(self.window)
            self.toggle3.label_set("Services (ObexFTPd):")
            self.toggle3.size_hint_align_set(-1.0, 0.0)
            self.toggle3.states_labels_set("On","Off")
            if os.popen("obexftpd --help | grep ObexFTPd").read().replace("\n","")!="":
                self.toggle3.show()
                box1.pack_end(self.toggle3)
                self.toggle3.changed = self.toggle3Click
            else:
                print "No obexftpd found :/ toggle disable"

            """


        #self.BtmodGUIupdate()

        return box1

    def stopUpdate(self):
        print "BT desktructor"
        self.guiUpdate = 0
