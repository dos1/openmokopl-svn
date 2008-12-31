import elementary, module

class Misc(module.AbstractModule):
    def name(self):
        return "Miscellaneous"
    
    def view(self, win):
        la = elementary.Label(win)
        la.label_set("Suspend, dim time and etc.")
        return la

