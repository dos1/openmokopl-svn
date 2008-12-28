import elementary, module

class Gprs(module.AbstractModule):
    def name(self):
        return "GPRS"
    
    def view(self, win):
        la = elementary.Label(win)
        la.label_set("GPRS connection configuration")
        return la

