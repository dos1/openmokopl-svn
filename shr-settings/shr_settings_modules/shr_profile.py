import elementary, module

class Profile(module.AbstractModule):
    name = "Profile"


    def defbt_click(self, obj, event):
        os.system("echo \"preferences.SetProfile('default')\" | cli-framework")

    def silbt_click(self, obj, event):
        os.system("echo \"preferences.SetProfile('silent')\" | cli-framework")

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


        defbt = elementary.Button(self.window)
        defbt.clicked = self.defbt_click
        defbt.label_set("default" )
        defbt.size_hint_align_set(-1.0, 0.0)
        boxh.pack_end(defbt)

        silbt = elementary.Button(self.window)
        silbt.clicked = self.silbt_click
        silbt.label_set("silent" )
        silbt.size_hint_align_set(-1.0, 0.0)
        boxh.pack_end(silbt)


        return boxh
