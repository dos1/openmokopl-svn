import elementary, module

class Profile(module.AbstractModule):
    def name(self):
        return "Profile"
    def view(self, win):
        la = elementary.Label(win)
        la.label_set("Current profile: default")
        return la

if __name__ == "__main__":
    print "This is "+name()+" module for shr-settings."
    exit(0)    
