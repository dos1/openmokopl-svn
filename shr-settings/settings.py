import elementary
import edje
import evas

def load_module(mod):
    frame = elementary.Frame(win)
    frame.label_set(mod.name()+" settings")
    box1.pack_end(frame)
    frame.size_hint_align_set(-1.0, 0.0)
    frame.show()

    cont = mod.view(win)
    frame.content_set(cont)
    cont.size_hint_align_set(-1.0, 0.0)
    cont.show()

def destroy(obj, event, *args, **kargs):
    print "DEBUG: window destroy callback called!"
    elementary.exit()

if __name__ == "__main__":
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
    fr.size_hint_align_set(-1.0, 0.0)
    box0.pack_end(fr)
    fr.show()

    lb = elementary.Label(win)
    lb.label_set("Here will be toolbar.")
    fr.content_set(lb)
    lb.show()

    sc = elementary.Scroller(win)
    sc.size_hint_weight_set(1.0, 1.0)
    sc.size_hint_align_set(-1.0, -1.0)
    box0.pack_end(sc)
    sc.show()

    box1 = elementary.Box(win)
    box1.size_hint_weight_set(1.0, -1.0)
    sc.content_set(box1)
    box1.show()

    #loading modules
    import shr_gsm, shr_bt, shr_wifi, shr_test

    modules = [ shr_gsm, shr_bt, shr_wifi, shr_test ]
    for mod in modules:
        load_module(mod)
    #end of loading modules

    win.show()
    elementary.run()
    elementary.shutdown()

