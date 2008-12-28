import module, elementary

class Usb(module.AbstractModule):

    def mode_handle(self, obj, event):
        if obj.state_get():
            self.toggle1.label_set("Device mode:")
            self.toggle1.states_labels_set("Ethernet","Mass storage")
            self.toggle1.state_set(1)
        else:
            self.toggle1.label_set("Host powered:")
            self.toggle1.states_labels_set("Yes","No")
            self.toggle1.state_set(1)

    def name(self):
        return "USB"

    def view(self, win):
        box1 = elementary.Box(win)
        self.toggle0 = elementary.Toggle(win)
        self.toggle0.label_set("USB mode:")
        self.toggle0.size_hint_align_set(-1.0, 0.0)
        self.toggle0.states_labels_set("Device","Host")
	self.toggle0.state_set(1)
        self.toggle0.changed = self.mode_handle
        box1.pack_start(self.toggle0)
        self.toggle0.show()

	self.toggle1 = elementary.Toggle(win)
	self.toggle1.label_set("Device mode:")
	self.toggle1.size_hint_align_set(-1.0, 0.0)
        self.toggle1.states_labels_set("Ethernet","Mass storage")
	self.toggle1.state_set(1)
        box1.pack_end(self.toggle1)
        self.toggle1.show()

        return box1
        
if __name__ == "__main__":
    print "This is "+name()+" module for shr-settings."
    exit(0)    
