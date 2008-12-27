import elementary
import edje
import evas

modtoshow = 0

def destroy(obj, event, *args, **kargs):
    print "DEBUG: window destroy callback called!"
    elementary.exit()

def show(obj, event, *argns, **kargs):
    win = elementary.Window("settings2", elementary.ELM_WIN_BASIC)
    win.title_set(shr_gsm.name()+" settings")
    win.autodel_set(True)
    bg = elementary.Background(win)
    win.resize_object_add(bg)
    bg.size_hint_weight_set(1.0, 1.0)
    bg.show()
    cont = shr_gsm.view(win)
    win.resize_object_add(cont)
    win.show()    
    
def justfortest(obj, event, *args, **kargs):
    print "hardcoded button for testing purposes"

if __name__ == "__main__":
    #  C{function(object, event_info, *args, **kargs)}
    elementary.init()
    win = elementary.Window("settings", elementary.ELM_WIN_BASIC)
    win.title_set("Settings")
    win.destroy = destroy
    
    bg = elementary.Background(win)
    win.resize_object_add(bg)
    bg.size_hint_weight_set(1.0, 1.0)
    bg.show()

    box0 = elementary.Box(win)
    box0.size_hint_weight_set(1.0, 1.0)
    win.resize_object_add(box0)
    box0.show()

    fr = elementary.Frame(win)
    fr.label_set("SHR Settings")
    box0.pack_end(fr)
    fr.show()

    lb = elementary.Label(win)
    lb.label_set("Here will be toolbar instead of buttons.")
    fr.content_set(lb)
    lb.show()

#    tb = elementary.Toolbar(win)
#    tb.show()

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
    bt.clicked = justfortest
    bt.label_set("Just for test")
    bt.size_hint_align_set(-1.0, 0.0)
    box1.pack_end(bt)
    bt.show()

    #path = 'modules/'
    #for infile in glob.glob( os.path.join(path, '*.py') ):
    #    print infile


    #TODO: handle modules automatically
    import shr_gsm

    bt = elementary.Button(win)
    bt.clicked = show
    bt.label_set(shr_gsm.name())
    bt.size_hint_align_set(-1.0, 0.0)
    box1.pack_end(bt)
    bt.show()

    win.show()
    elementary.run()
    elementary.shutdown()

