#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
   #openmoko.pl LogBot

   A minimal IRC log

   Written by Sebastian Krzyszkowiak
   Based on Chris Oliver work

   This program is free software; you can redistribute it and/or
   modify it under the terms of the GNU General Public License
   as published by the Free Software Foundation; either version 2
   of the License, or any later version.

   This program is distributed in the hope that it will be useful,
   but WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
   GNU General Public License for more details.

   You should have received a copy of the GNU General Public License
   along with this program; if not, write to the Free Software
   Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA   02111-1307, USA.
"""

__author__ = "Sebastian Krzyszkowiak <seba.dos1@gmail.com>, Chris Oliver <excid3@gmail.com>"
__version__ = "0.1"
__date__ = "20/06/2009"
__copyright__ = "Copyright (c) Sebastian Krzyszkowiak, Chris Oliver"
__license__ = "GPL2"

# Imports
from time import strftime, sleep
import irclib

# Connection information
network = 'irc.freenode.net'
port = 6667
channel = '#mojulubionykanal'
nick = 'mojlogbot'
name = 'Moj log bot'
password = 'moje-super-tajne-haslo'
url = 'http://moj.serwer.com/logs/'
logdir = '/var/www/logs/'

def write(string): # Writes a line to the log file
    f = open(logdir+strftime("%Y-%m-%d")+'.txt','a')
    f.write(strftime("[%H:%M] ") + string + '\n')
    f.close
    print string

def writeToChan(channel, string):
    server.privmsg(channel, string)
    write(nick + ': ' + string)

def handleJoin(connection,event): # Join notifications
    write(event.source().split('!')[0] + ' has joined ' + event.target())

def handleQuit(connection, event):
    write(event.source().split('!')[0]+ ' has left server [' + event.arguments()[0] +']')

def handlePubMessage(connection, event): # Any public message
    write(event.source().split ('!')[0] + ': ' + event.arguments()[0])
    if nick in event.arguments()[0]:
      writeToChan(channel, 'Cześć ' + event.source().split('!')[0] + '. Jestem tylko zwykłym botem logującym.')
      sleep(1)
      writeToChan(channel, 'Logi możesz znaleźć na '+url)

def handlePrivNotice(connection, event):
   if event.source()=="NickServ!NickServ@services." and event.arguments()[0]=='You are now identified for \x02'+nick+'\x02.':
     print "Identified. Joining to "+channel+"..."
     server.join(channel)
   else:
     if event.source()==None:
       source = 'server'
     else:
       source = event.source().split('!')[0]
     print "PrivNotice: " + source + ': ' + event.arguments()[0]

def handlePrivMessage(connection, event):
    print "PrivMsg: " + event.source().split('!')[0] + ': ' + event.arguments()[0]

# Create an IRC object
irc = irclib.IRC()

irc.add_global_handler('join', handleJoin)
irc.add_global_handler('pubmsg', handlePubMessage)
irc.add_global_handler('privnotice', handlePrivNotice)
irc.add_global_handler('privmsg', handlePrivMessage)
irc.add_global_handler('quit', handleQuit)

# Create a server object, connect and join the channel
server = irc.server()
server.connect(network, port, nick, ircname=name)
server.privmsg('NickServ', 'identify '+password)

# Jump into an infinite loop
irc.process_forever()
