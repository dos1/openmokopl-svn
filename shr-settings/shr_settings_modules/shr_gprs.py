import elementary
import module

class Gprs(module.AbstractModule):
    name = "GPRS"
    
    def createView(self):
        elementary.init()
        la = elementary.Label(self.window)
        la.label_set("GPRS connection configuration")
        return la

