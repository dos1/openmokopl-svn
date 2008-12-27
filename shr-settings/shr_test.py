import elementary
def totest(obj, event, *argns, **kargs):
    print event
    print "it works!"
    obj.label_set("lol")
def name():
    print "name"
    return "Test"
def icon():
    return 0
def enabled():
    return True
def view(win):
    bt = elementary.Button(win)
    bt.clicked = totest
    bt.label_set("Just for fun")
    bt.size_hint_align_set(-1.0, 0.0)
    bt.show()

    return bt


if __name__ == "__main__":
    print "This is "+name()+" module for shr-settings."
    exit(0)    
