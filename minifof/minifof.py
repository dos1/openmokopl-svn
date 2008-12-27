#!/usr/bin/env python

import pygtk
pygtk.require('2.0')
import gtk
import os
import random
import pygame
from pygame.locals import *

if not pygame.mixer: print "Sound isn't available"

class MiniFoF:

    def playmp3 (self, path, background = 1):
	backstr=""
	if background==1:
		backstr=" &"
	os.system("madplay "+path+" -o wave:- | aplay -q - "+backstr)

    def playaudio (self, path, background = 1):
		backstr=""
		if background==1:
			backstr=" &"
		os.system("aplay -q "+path+backstr)

    def load_sound(self, name):
        class NoneSound:
            def play(self): pass
        if not pygame.mixer:
            return NoneSound()
        fullname = os.path.join('', name)
        try:
            sound = pygame.mixer.Sound(fullname)
        except pygame.error, message:
            print "Cannot load sound:", name
            raise SystemExit, message
        return sound

    def callback(self, widget, data):
	randnr=random.randint(1, 6)
	self.load_sound("sounds/bug%d.wav" % (randnr)).play()
	#self.playaudio("bug%d.wav" % (randnr))
	#self.box1.move(widget,100,100)

    # another callback
    def delete_event(self, widget, event, data=None):
        gtk.main_quit()
        return False

    def __init__(self):
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)

        self.window.set_title("MiniFoF")

        self.window.connect("delete_event", self.delete_event)

        self.box1 = gtk.Fixed()

	self.image=gtk.Image()

	self.image.set_from_file("fof.png")

        self.window.add(self.box1)

	self.box1.put(self.image,0,0)

        self.button1 = gtk.Button("Fret 1")
        self.button1.connect("pressed", self.callback, "button 1")
        self.button2 = gtk.Button("Fret 2")
        self.button2.connect("pressed", self.callback, "button 2")
	self.button3 = gtk.Button("Fret 3")
	self.button4 = gtk.Button("Fret 4")
        self.button3.connect("pressed", self.callback, "button 3")
        self.button4.connect("pressed", self.callback, "button 4")


	self.box1.put(self.button1,0,374)
	self.box1.put(self.button2,120,374)
	self.box1.put(self.button3,240,374)
	self.box1.put(self.button4,360,374)
	self.button1.set_size_request(120,146)
	self.button2.set_size_request(120,146)
	self.button3.set_size_request(120,146)
	self.button4.set_size_request(120,146)

        self.box1.show_all()
#	self.playmp3("portal_still_alive.mp3")
        self.window.show_all()

def main():
    pygame.mixer.init()
    gtk.main()

if __name__ == "__main__":
    minifof = MiniFoF()
    main()
