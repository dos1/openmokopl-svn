import elementary, module

class Profile(module.AbstractModule):
    def name(self):
        return "Profile"
    
    def view(self, win):
	boxh = elementary.Box(win)
	boxh.horizontal_set(True)
        la = elementary.Label(win)
        la.label_set("Current profile:")
	la.show()
	boxh.pack_start(la)
	self.cur = elementary.Label(win)
	self.cur.label_set("default")
	boxh.pack_end(self.cur)
	self.cur.show()
        return boxh
