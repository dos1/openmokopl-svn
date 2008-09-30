#!/usr/bin/env python

# MokoFight 0.1 very ugly pre-alpha etc.
# by dos, GPLv3

from struct import unpack_from

import pygtk
pygtk.require('2.0')
import gtk
import os
import random
import thread

gtk.gdk.threads_init()

x = y = z = 0
obrona	  = 0
atak	  = 0
ingame	  = 0
hp	  = 100
enemyhp   = 100

class MokoFight:

	def playaudio (self, path, background = 1):
		backstr=""
		if background==1:
			backstr=" &"
		os.system("aplay -q sounds/"+path+backstr)

	def accelread (self):
		global x, y, z

		f = open("/dev/input/event3", "r")

		maxx = maxy = maxz = 0
		minx = miny = minz = 0
		i = 0;
		while (i<3):
			block = f.read(16)
			if block[8] == "\x02":
				if block[10] == "\x00":
					x = unpack_from( "@l", block[12:] )[0]
					maxx, minx = max( x, maxx ), min( x, minx )
				if block[10] == "\x01":
					y = unpack_from( "@l", block[12:] )[0]
					maxy, miny = max( y, maxy ), min( y, miny )
				if block[10] == "\x02":
					z = unpack_from( "@l", block[12:] )[0]
					maxz, minz = max( z, maxz ), min( z, minz )
				text = "x = %3d;  y = %3d;	z = %3d" % ( x, y, z )
			i=i+1

		f.close()

		return True

	def win(self):
		global ingame
		self.playaudio("death.wav",0)
		ingame=0

	def lose(self):
		global ingame
		self.playaudio("death.wav",0)
		ingame=0

	def enemy_block(self):
		randnr=random.randint(0, 1)	
		return randnr

	def update_hp(self):
		global hp
		self.hplabel.set_label("My HP: %d" % (hp))
		self.hpprogress.set_fraction(float(hp) / 100)
		if hp == 0:
			self.lose()

	def update_enemyhp(self):
		global enemyhp
		self.ehplabel.set_label("Enemy's HP: %d" % (enemyhp))
		self.ehpprogress.set_fraction(float(enemyhp) / 100)
		if enemyhp == 0:
			self.win()

	def hitted (self):
		global hp
		randnr=random.randint(1, 6)
		self.playaudio("whoosh%d.wav" % (randnr))
		hp = hp - 5
		self.update_hp()
		return True

	def defended (self):
		randnr=random.randint(1, 5)
		self.playaudio("ching%d.wav" % (randnr))
		return True

	def enemy_attack (self):
		global obrona
		if obrona == 1:
			self.defended()
		else:
			self.hitted()

	def enemy_attack_button (self, widget, data=None):
		self.enemy_attack()
		return True

	def hit (self):
		global enemyhp
		print "hit"
		randnr=random.randint(1, 6)
		self.playaudio("whoosh%d.wav" % (randnr))
		enemyhp = enemyhp - 5
		self.update_enemyhp()
		return True

	def miss (self):
		print "miss"
		randnr=random.randint(1, 5)
		self.playaudio("ching%d.wav" % (randnr))	
		return True

	def attack (self):
		global atak
		atak=1
		print "attack"
		if self.enemy_block():
			self.miss()
		else:
			self.hit()
		return True

	def stop_attack (self):
		global atak
		atak=0
		return True

	def defend (self):
		global obrona
		print "defending"
		self.labeldefend.set_label("Defending")
		obrona=1
		return True

	def stop_defend (self):
		global obrona
		print "end of defending"
		self.labeldefend.set_label("")
		obrona=0
		return True

	def proceed (self):

		global x, y, z
		global obrona,atak

		if z > 500 and atak==0 and obrona == 0 and x > -90:
			self.attack()
		elif z <= 500 and atak == 1:
			self.stop_attack()

		if x < -180 and z < 300 and obrona == 0:
			self.defend()
		elif x >= -180 and obrona == 1:
			self.stop_defend()

		return True


	def game(self,lol,lol2):
		global ingame, hp, enemyhp
		hp = 100
		enemyhp = 100
		self.vboxstatus.show()
		self.update_hp()
		self.update_enemyhp()
		self.startbutton.set_sensitive(0)
		self.separator.set_sensitive(1)
		while ingame:
			self.accelread()
			self.proceed()
		self.startbutton.set_sensitive(1)
		self.separator.set_sensitive(0)
		self.vboxstatus.hide()

	def start(self, widget, data=None):
		global ingame
		self.playaudio("start.wav",0)
		ingame=1
		thread.start_new_thread(self.game, (0,0))

	def delete_event(self, widget, event, data=None):
		print "shutting down!"
		return False

	def destroy(self, widget, data=None):
		ingame=0
		print "nap time!"
		self.playaudio("death.wav",0)
		gtk.main_quit()

	def __init__(self):
		self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
		self.window.connect("delete_event", self.delete_event)
		self.window.connect("destroy", self.destroy)
		self.window.set_border_width(10)
		self.vbox = gtk.VBox(0, 10)
		self.label = gtk.Label("MokoFight 0.1 pre-alpha")
		self.quitbutton = gtk.Button("Bye bye")
		self.startbutton = gtk.Button("Start game")
		self.startbutton.connect("clicked", self.start, None)
		self.quitbutton.connect_object("clicked", gtk.Widget.destroy, self.window)
#	self.separator = gtk.HSeparator()
		self.separator = gtk.Button("Harakiri")
		self.separator.connect("clicked", self.enemy_attack_button, None)	
		self.separator.set_sensitive(0)

		self.hbox=gtk.HBox(0,10)
		self.vboxhp=gtk.VBox(0,10)
		self.hplabel=gtk.Label("My HP: ?")
		self.hpprogress=gtk.ProgressBar()
		self.hpprogress.set_fraction(0)
		self.vboxhp.add(self.hplabel)
		self.vboxhp.add(self.hpprogress)
		self.vboxehp=gtk.VBox(0,10)
		self.ehplabel=gtk.Label("Enemy's HP: ?")
		self.ehpprogress=gtk.ProgressBar()
		self.ehpprogress.set_fraction(0)
		self.vboxehp.add(self.ehplabel)
		self.vboxehp.add(self.ehpprogress)
		self.hbox.add(self.vboxhp)
		self.hbox.add(self.vboxehp)

		self.vboxstatus=gtk.VBox(0,10)
		self.labeldefend=gtk.Label("")
		self.vboxstatus.add(self.hbox)
		self.vboxstatus.add(self.labeldefend)

		self.vboxbottom=gtk.VBox(0,10)
		self.labelurl=gtk.Label("http://openmoko.opendevice.org/mokofight/")
		self.vboxbottom.add(self.labelurl)
		self.vboxbottom.add(self.quitbutton)
		self.vbox.add(self.label)	
		self.vbox.add(self.startbutton)
		self.vbox.add(self.vboxstatus)
		self.vbox.add(self.separator)
		self.vbox.add(self.vboxbottom)
		self.window.add(self.vbox)
		self.window.set_title("MokoFight")
		self.window.show_all()
		self.vboxstatus.hide()

	def main(self):
		gtk.main()

if __name__ == "__main__":
	mokofight = MokoFight()
	mokofight.main()

# vim: ts=4
