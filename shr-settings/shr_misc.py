import elementary, module

class Misc(module.AbstractModule):
    def name(self):
        return "Miscellaneous"
    def enabled(self):
        return True
    def view(self, win):
        la = elementary.Label(win)
        la.label_set("Suspend, dim time and etc.")
        return la

if __name__ == "__main__":
    print "This is "+name()+" module for shr-settings."
    exit(0)    
