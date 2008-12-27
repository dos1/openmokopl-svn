#-*- coding: utf-8 -*-

import elementary

__author__="hiciu"
__date__ ="$2008-12-27 21:53:00$"

u"""
    This class should be parent for all shr-settings modules.

    import module
    class MyModule(module.AbstractModule, "MyModule"):
        def view(self, win):
	  [code :P]
"""
class AbstractModule(object):
    u"constructor. param: displayed name, return: nothing"
    def __init__(self, name = "OhMy! I have no name!"):
        self._name = name

    u"this one returns displayed name. It should be set with __init__."
    def name(self):
        return self._name

    u"""
        In future, this should return an object (bitmap?) that will act as
        an icon. But for now it's return 0.
    """
    def icon(self):
        #FIXME: insert proper code here :)
        return 0

    u"""
        If module isn't enabled it shouldn't be displayed. Use it to
        check if we have wifi hardware or bluetooth dongle or something.
        Default: module is enabled
    """
    def enabled(self):
        return True

    u"""
        This should return frame (elementary.box)with will
        be displayed to user. I do not understand how it works so... :)
        Here is example code:

        def view(self, win):
            box1 = elementary.Box(win)

	  toggle0 = elementary.Toggle(win)
            toggle0.label_set("GSM antenna:")
            toggle0.size_hint_align_set(-1.0, 0.0)
            toggle0.states_labels_set("On","Off")

            box1.pack_start(toggle0)
            return box1
    """
    def view(self, win):
        pass

if __name__ == "__main__":
    print "no! this shouldn't be executed like that!";