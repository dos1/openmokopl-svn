import elementary
def name():
    return "Profile"
def icon():
    return 0
def enabled():
    return True
def view(win):
    la = elementary.Label(win)
    la.label_set("Current profile: default")
    return la

if __name__ == "__main__":
    print "This is "+name()+" module for shr-settings."
    exit(0)    
