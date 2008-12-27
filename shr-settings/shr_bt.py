import elementary
def name():
    return "Bluetooth"
def icon():
    return 0
def enabled():
    return True
def view(win):
    box1 = elementary.Box(win)
    toggle0 = elementary.Toggle(win)
    toggle0.label_set("Bluetooth radio:")
    toggle0.size_hint_align_set(-1.0, 0.0)
    toggle0.states_labels_set("On","Off")
    box1.pack_start(toggle0)
    toggle0.show()

    return box1

if __name__ == "__main__":
    print "This is "+name()+" module for shr-settings."
    exit(0)    