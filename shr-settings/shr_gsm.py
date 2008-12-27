import elementary
def totest(obj, event, *argns, **kargs):
    print "it works!"
def name():
    print "name"
    return "GSM"
def icon():
    return 0
def view(win):
    box0 = elementary.Box(win)
    box0.size_hint_weight_set(1.0, 1.0)
    box0.show()
    sc = elementary.Scroller(win)
    sc.size_hint_weight_set(1.0, 1.0)
    sc.size_hint_align_set(-1.0, -1.0)
    box0.pack_end(sc)
    sc.show()

    box1 = elementary.Box(win)
    box1.size_hint_weight_set(1.0, 1.0)
    sc.content_set(box1)
    box1.show()

    bt = elementary.Button(win)
    bt.label_set("Just for fun")
    bt.size_hint_align_set(-1.0, 0.0)
    box1.pack_end(bt)
    bt.show()

    toggle0 = elementary.Toggle(win)
    toggle0.label_set("GSM antenna:")
    toggle0.changed = totest
    toggle0.states_labels_set("On","Off")
    box1.pack_start(toggle0)
    toggle0.show()

    return box0

        
    

if __name__ == "__main__":
    print "This is "+name()+" module for shr-settings."
    exit(0)    
