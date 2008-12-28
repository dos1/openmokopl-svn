import elementary, module

class Gprs(module.AbstractModule):
    def name(self):
        return "GPRS"
    
    def view(self, win):
        la = elementary.Label(win)
        la.label_set("GPRS connection configuration")
        return la

if __name__ == "__main__":
    print "This is "+name()+" module for shr-settings."
    exit(0)    
