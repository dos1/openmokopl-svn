import elementary
import edje
import evas

def load_module(mod):
    if mod.enabled():
        frame = elementary.Frame(win)
        frame.label_set(mod.name()+" settings")
        box1.pack_end(frame)
        frame.size_hint_align_set(-1.0, 0.0)
        frame.show()

        cont = mod.view(win)
        frame.content_set(cont)
        cont.show()

def destroy(obj, event, *args, **kargs):
    print "DEBUG: window destroy callback called! kabum!"
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

    quitbt = elementary.Button(win)
    quitbt.clicked = destroy
    quitbt.label_set("Quit")
    quitbt.size_hint_align_set(-1.0, 0.0)
    quitbt.show()
    box0.pack_end(quitbt)

    box1 = elementary.Box(win)
    box1.size_hint_weight_set(1.0, -1.0)
    sc.content_set(box1)
    box1.show()

    #loading modules
    import shr_gsm, shr_bt, shr_wifi, shr_clock, shr_profile, shr_misc, shr_test

    modules = [ shr_gsm.Gsm, shr_bt.Bt, shr_wifi.Wifi, shr_clock.Clock, shr_profile.Profile, shr_misc.Misc, shr_test.Test ]
    for mod in modules:
        module = mod();
        load_module(module)
    #end of loading modules

    win.show()
    elementary.run()
    elementary.shutdown()
