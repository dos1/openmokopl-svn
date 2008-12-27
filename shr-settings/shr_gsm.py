import module, os, re, sys, elementary

class Gsm(module.AbstractModule):
    def name(self):
        return "GSM"

    def destroy(self, obj, event, *args, **kargs):
        print "DEBUG: window destroy callback called! kabum!"
        
    def operatorSelect(self, obj, event, *args, **kargs):
        print "clik"

    def operatorsList(self, obj, event, *args, **kargs):
        print "Operators list\nStart query cli-framework\n-------"
        self.operatorsList = os.popen("echo \"gsmnetwork.ListProviders()\" | cli-framework", "r");
        #operatorsList = os.popen("cat /tmp/operators", "r");
        row = 1
        res = ""
        while 1:
	  row+=1
	  line = self.operatorsList.readline();
	  if not line:
	      break
	  if row>=3:
	      print str(row)+": >["+line+"]<"
	      lineParse = line.replace(" ", "").replace(">>>", "").replace("[", "").replace("]", "").replace("),", ")")
	      if len(lineParse) > 5:
		res+= lineParse
        print "-------\nEnd query cli-framework"
        print "------res-\n"
        print res
        print "------res-\n"

        winope = elementary.Window("listProviders", elementary.ELM_WIN_BASIC)
        winope.title_set("List Providers")
        winope.destroy = destroy

        box0 = elementary.Box(winope)
        box0.size_hint_weight_set(1.0, 1.0)
        winope.resize_object_add(box0)
        box0.show()

        fr = elementary.Frame(winope)
        fr.label_set("List Providers")
        fr.size_hint_align_set(-1.0, 0.0)
        box0.pack_start(fr)
        fr.show()

        resA = res.split("\n")

        for l in resA:
	  line = l.split(",")
	  if len(line)>2:
	      opeAvbt = elementary.Button(winope)
	      opeAvbt.label_set( line[0].replace("(","")+" "+line[2].replace("'","") )
	      opeAvbt.clicked = operatorSelect
	      opeAvbt.size_hint_align_set(-1.0, 0.0)
	      opeAvbt.show()
	      box0.pack_end(opeAvbt)

        bg = elementary.Background(winope)
        winope.resize_object_add(bg)
        bg.size_hint_weight_set(1.0, 1.0)
        bg.show()

        winope.show()

    def view(self, win):
        box1 = elementary.Box(win)
        toggle0 = elementary.Toggle(win)
        toggle0.label_set("GSM antenna:")
    #    toggle0.changed = totest
        toggle0.size_hint_align_set(-1.0, 0.0)
        toggle0.states_labels_set("On","Off")
        box1.pack_start(toggle0)


        opebt = elementary.Button(win)
        opebt.clicked = self.operatorsList
        opebt.label_set("Operators")
        opebt.size_hint_align_set(-1.0, 0.0)
        opebt.show()
        box1.pack_end(opebt)

        toggle0.show()

        return box1

if __name__ == "__main__":
    print "This is "+name()+" module for shr-settings."
    exit(0)    

