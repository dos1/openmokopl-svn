import elementary, module

class Profile(module.AbstractModule):
    name = "Profile"
    
    def createView(self):
        boxh = elementary.Box(self.window)
        boxh.horizontal_set(True)
        la = elementary.Label(self.window)
        la.label_set("Current profile:")
        la.show()
        boxh.pack_start(la)
        self.cur = elementary.Label(self.window)
        self.cur.label_set("default")
        boxh.pack_end(self.cur)
        self.cur.show()
        return boxh
