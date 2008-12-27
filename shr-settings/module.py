#-*- coding: utf-8 -*-

import elementary

__author__="hiciu"
__date__ ="$2008-12-27 21:53:00$"

u"""
    dokumentacje to ja zaraz uzupełnię :)
"""
class AbstractModule(object):
    u"""
        To robi.. blablabla
        zwraca.. blablabla
    """
    def name(self):
        return "OhMy! I have no name!"

    u"""
        To robi.. blablabla
        zwraca.. blablabla
    """
    def icon(self):
        return 0

    def enabled(self):
        return True

    u"""
        I tak dalej.. i tak dalej..
    """
    def view(self, win):
        pass

if __name__ == "__main__":
    print "no! this shouldn't be executed like that!";