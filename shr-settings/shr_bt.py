import time
import module, elementary, os

"""
- gta01
/sys/devices/platform/s3c2410-i2c/i2c-adapter/i2c-0/0-0008/neo1973-pm-bt.0/
- gta02
/sys/devices/platform/s3c2440-i2c/i2c-adapter/i2c-0/0-0073/neo1973-pm-bt.0/

"""
btModels = [ \
"/sys/devices/platform/s3c2410-i2c/i2c-adapter/i2c-0/0-0008/neo1973-pm-bt.0",
"/sys/devices/platform/s3c2440-i2c/i2c-adapter/i2c-0/0-0008/neo1973-pm-bt.0"]

class BtMstateContener:
    def __init__(self):
        self.model = ""
        self.state = 0
        self.getModel()

    def getModel(self):
        return self.model

    def getModel(self):
        try:
            open(btModels[0]+"/power_on", "r")
            self.model = "gta01"
        except:
            print "BT BtMstateContener getModel [inf] not gta01"

        try:
            open(btModels[1]+"/power_on", "r")
            self.model = "gta02"
        except:
            print "BT BtMstateContener getModel [inf] not gta02"

        print "BT BtMstateContener getModel [inf] device is ? "+self.model

    def setPower(self, b ):
        print "BT BtMstateContener setPower [inf] "+self.model
        if self.model=="gta01":
            m=0
        elif self.model=="gta02":
            m=1
        else:
            return 0

        if b==0:
            print "reset"
            os.system("echo "+str(b)+" > "+btModels[m]+"/reset")
            print "sleep"
            time.sleep(1)
            print "power_on"
            os.system("echo "+str(b)+" > "+btModels[m]+"/power_on")
        else:
            print "power_on"
            os.system("echo "+str(b)+" > "+btModels[m]+"/power_on")
            print "sleep"
            time.sleep(1)
            print "reset"
            os.system("echo "+str(b)+" > "+btModels[m]+"/reset")

        

    def getPower(self):
        if self.model=="gta01":
            f0 = open(btModels[0]+"/power_on", "r")
        elif self.model=="gta02":
            f0 = open(btModels[1]+"/power_on", "r")
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


class Bt(module.AbstractModule):
    def name(self):
        return "Bluetooth"

    def BtmodGUIupdate(self):
        self.toggle0.state_set( self.btmc.getPower() )

    def toggle0Click(self, obj, event, *args, **kargs):
        if self.btmc.getPower():
            print "Bt toggle0Click BT set OFF"
            self.btmc.setPower( 0 )
        else:
            print "Bt toggle0Click BT set ON"
            self.btmc.setPower( 1 )

        
        #self.BtmodGUIupdate()
        


    def view(self, win):
        self.btmc = BtMstateContener()
        

        box1 = elementary.Box(win)
        self.toggle0 = elementary.Toggle(win)
        self.toggle0.label_set("Bluetooth radio:")
        self.toggle0.size_hint_align_set(-1.0, 0.0)
        self.toggle0.states_labels_set("On","Off")
        box1.pack_start(self.toggle0)
        self.toggle0.show()

        if self.btmc.getModel!="":
            self.toggle0.changed = self.toggle0Click

        self.BtmodGUIupdate()

        return box1
        
