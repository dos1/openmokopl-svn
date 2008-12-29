import module, elementary, os

class Clock(module.AbstractModule):
    def ntpsync(self, obj, event):
	os.system("ntpdate ntp.org")
        self.cl.edit_set(False)
        self.but.label_set("Set time")
        self.editable = False
    def clockset(self, obj, event):
	if self.editable:
	    self.cl.edit_set(False)
            obj.label_set("Set time")
	    self.editable = False
	else:
  	    self.cl.edit_set(True)
	    obj.label_set("OK")
            self.editable = True
    def name(self):
        return "Date/time"
    def view(self, win):
	self.editable = False
	box0 = elementary.Box(win)
        self.cl = elementary.Clock(win)
        self.cl.show_seconds_set(True)
	box0.pack_end(self.cl)
	self.cl.show()
	self.but = elementary.Button(win)
	self.but.label_set("Set time")
	self.but.size_hint_align_set(-1.0, 0.0)
	box0.pack_end(self.but)
	self.but.clicked = self.clockset
	self.but.show()
	ntp = elementary.Button(win)
	ntp.label_set("Synchronize with ntp")
	ntp.size_hint_align_set(-1.0, 0.0)
	ntp.clicked = self.ntpsync
	box0.pack_end(ntp)
	ntp.show()
        return box0
