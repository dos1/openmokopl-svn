import elementary, module, os

class Wifi(module.AbstractModule):
    def name(self):
        return "WiFi"

    def enabled(self):
	if os.popen("cat /proc/cpuinfo | grep Hardware").read()=="Hardware	: GTA01\n":
	    return 0
	else:
	    return 1
    
    def view(self, win):
        box1 = elementary.Box(win)
        toggle0 = elementary.Toggle(win)
        toggle0.label_set("WiFi radio:")
        toggle0.size_hint_align_set(-1.0, 0.0)
        toggle0.states_labels_set("On","Off")
        box1.pack_start(toggle0)
        toggle0.show()

        return box1
