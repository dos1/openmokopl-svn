#!/usr/bin/env python
import elementary, os,time, sys
import edje,ecore
import evas
import dbus
import e_dbus







class MainWindow:

    def destroy(self, obj, event, *args, **kargs):
        print "DEBUG: window destroy callback called! kabum!"
        f = open("/tmp/OSMupdate_state", "w")
        f.write("KILL")
        f.close()
        elementary.exit()


    def updateStatus(self):

        try:
            
            print "updateStatus iter"
            hand = open("/tmp/OSM_log","r")
            #print "updateStatus open"
            line = hand.readlines()
            hand.close()
            #print "updateStatus close"
            state = line[len(line)-1].replace("\n","")
            #print "updateStatus last line:"+state
            self.label.label_set( str(state) )
            #print "updateStatus 1"
            if state == "DONE":
                #print "updateStatus DONE"
                f = open("/tmp/OSMupdate_state", "w")
                f.write("KILL")
                f.close()
            else:
                #print "updateStatus timer_add"
                ecore.timer_add( 1.4, self.updateStatus)

                
        except:
            self.updatebt.show()
            print "updateStatus no log file found"

        
        #print "updateStatus end-----------"

    def updatebtClick(self, obj,event):
        print "bt update click"
        f = open("/tmp/OSMupdate_state", "w")
        f.write("START")
        f.close()
        time.sleep(2)
        self.updatebt.hide()
        self.updateStatus()
        
        
    def __init__(self):
        elementary.init()


        self.win = elementary.Window("osm", elementary.ELM_WIN_BASIC)
        self.win.title_set("OSM updater")
        self.win.destroy = self.destroy

        self.bg = elementary.Background(self.win)
        self.win.resize_object_add(self.bg)
        self.bg.size_hint_weight_set(1.0, 1.0)
        self.bg.show()

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




        boxAct = elementary.Box(self.win)
        boxAct.size_hint_weight_set(-1.0, -1.0)
        boxAct.show()

        fo = elementary.Frame(self.win)
        fo.label_set( "Local files:" )
        fo.size_hint_align_set(-1.0, -1.0)
        fo.show()
        fo.content_set( boxAct )

        self.updatebt = elementary.Button(self.win)
        self.updatebt.clicked = self.updatebtClick
        self.updatebt.label_set("update")
        self.updatebt.size_hint_align_set(-1.0, -1.0)
        self.updatebt.show()
        boxAct.pack_end(self.updatebt)


       

       

        box1.pack_start(fo)


        icon = elementary.Icon(self.win)
        try:
            os.open("osmupdater.png").read()
            icon.file_set("osmupdater.png")
        except:
            icon.file_set("/usr/share/pixmaps/osmupdater.png")
        icon.scale_set(0, 0)
        box1.pack_end(icon)
        icon.show()



        self.label = elementary.Label(self.win)
        self.label.label_set("application for update<br>local maps from<br>www.openstreetmap.org<br>for tangegps")
        self.label.size_hint_align_set(-1.0, 0.0)
        self.label.show()
        box1.pack_end( self.label )




        self.win.show()
        

if __name__ == "__main__":

    pid = os.fork()
    if pid:
        f = open("/tmp/OSMupdate_state", "w")
        f.write("RUNNING")
        f.close()


    else:
        time.sleep(2)
        while 1:
            try:
                val = open("/tmp/OSMupdate_state").read().replace("\n","")
                if val == "RUNNING":
                    #print "fork is running "
                    time.sleep(1)
                elif val == "START":
                    f = open("/tmp/OSMupdate_state", "w")
                    f.write("OSMupdate")
                    f.close()
                    #print "os.system start"
                    os.system("osmupdater.sh > /tmp/OSM_log")
                else:
                    break
            except:
                break
        print "fork killing it self"
        sys.exit(0)
            
        
    MainWindow()
    elementary.run()
    elementary.shutdown()

    
