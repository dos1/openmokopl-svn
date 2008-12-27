import elementary
def name():
    return "Date/time"
def icon():
    return 0
def enabled():
    return True
def view(win):
    cl = elementary.Clock(win)
    return cl

if __name__ == "__main__":
    print "This is "+name()+" module for shr-settings."
    exit(0)    
