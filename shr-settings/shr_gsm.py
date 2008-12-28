import module, os, re, sys, elementary

class Button2( elementary.Button ):
    mOpeNr = ""
    def set_opeNr( self, mOpeNr ):
        self.mOpeNr = mOpeNr

    def get_opeNr( self ):
        return self.mOpeNr

class Gsm(module.AbstractModule):
    def name(self):
        return "GSM"

    def destroy(self, obj, event, *args, **kargs):
        print "DEBUG: window destroy callback called! kabum!"
        #TODO - zamkniecie okna
        self.winope.hide()
        # to jest totalna proteza trzeba to poprawic
        
    def operatorSelect(self, obj, event, *args, **kargs):
        print "Start query cli-framework\n-------"


        os.popen("echo \"gsmnetwork.RegisterWithProvider( "+obj.get_opeNr()+" )\" | cli-framework", "r");


        print "-------\nEnd query cli-framework"
        print "set operator: "+obj.get_opeNr()
        #TODO - zamkniecie okna
        self.winope.hide()
        # to jest totalna proteza trzeba to poprawic
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

        box0 = elementary.Box(self.winope)
        box0.size_hint_weight_set(1.0, 1.0)
        self.winope.resize_object_add(box0)
        box0.show()

        fr = elementary.Frame(self.winope)
        fr.label_set("List Providers")
        fr.size_hint_align_set(-1.0, 0.0)
        box0.pack_start(fr)
        fr.show()

        box1 = elementary.Box(self.winope)
        box1.size_hint_weight_set(1.0, 1.0)
	fr.content_set(box1)
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

        opeAvbt = elementary.Button(self.winope)
        opeAvbt.label_set( "Cancel" )
        opeAvbt.clicked = self.destroy
        opeAvbt.size_hint_align_set(-1.0, 0.0)
        opeAvbt.show()
        box0.pack_end(opeAvbt)

        bg = elementary.Background(self.winope)
        self.winope.resize_object_add(bg)
        bg.size_hint_weight_set(1.0, 1.0)
        bg.show()

        self.opebt.label_set("Operators")

        self.winope.show()

    def view(self, win):
        box1 = elementary.Box(win)
        toggle0 = elementary.Toggle(win)
        toggle0.label_set("GSM antenna:")
    #    toggle0.changed = totest
        toggle0.size_hint_align_set(-1.0, 0.0)
        toggle0.states_labels_set("On","Off")
        box1.pack_start(toggle0)


        self.opebt = elementary.Button(win)
        self.opebt.clicked = self.operatorsList
        self.opebt.label_set("Operators")
        self.opebt.size_hint_align_set(-1.0, 0.0)
        self.opebt.show()
        box1.pack_end(self.opebt)

        toggle0.show()

        return box1

if __name__ == "__main__":
    print "This is "+name()+" module for shr-settings."
    exit(0)    

