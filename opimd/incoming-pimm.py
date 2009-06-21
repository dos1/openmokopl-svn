#!/usr/bin/env python
# -*- coding: utf-8 -*-

import dbus, e_dbus
from sys import argv
from os import system
from functools import partial
import elementary

cache = {}

def resolve_phone(number):
  if number in cache:
    return cache[number]
  else:
    x = contacts.Query({'Phone':number.strip('tel:')})
    query = getDbusObject (bus, "org.freesmartphone.opimd", x, "org.freesmartphone.PIM.ContactQuery")
    if query.GetResultCount()==1:
      name = query.GetResult()['Name']
    else:
      name = number.strip('tel:')
    cache[number] = name
    return name

def destroy(win, event, *args, **kargs):
  print "kabum"
  win.hide()
  win.delete()
#  elementary.exit()

# define some nice dbus helper, which I really like, cause make code easier to read :)
def getDbusObject (bus, busname , objectpath , interface):
        dbusObject = bus.get_object(busname, objectpath)
        return dbus.Interface(dbusObject, dbus_interface=interface)

bus = dbus.SystemBus(mainloop = e_dbus.DBusEcoreMainLoop())

messages = getDbusObject (bus, "org.freesmartphone.opimd", "/org/freesmartphone/PIM/Messages", "org.freesmartphone.PIM.Messages")
contacts = getDbusObject (bus, "org.freesmartphone.opimd", "/org/freesmartphone/PIM/Contacts", "org.freesmartphone.PIM.Contacts")

elementary.init()

elementary.c_elementary.finger_size_set(80)

def show_msg(text, bubble, obj, event, *args, **kwargs):
  obj.delete()
  bubble.content_set(text)
  text.show()

def close_win(win, obj, event, *args, **kwargs):
  destroy(win, event, args, kwargs)

def delete_msg(msg, win, obj, event, *args, **kwargs):
  msg.Delete()
  destroy(win, event, args, kwargs)

def open_inbox(obj, event, win, *args, **kwargs):
  system("python /home/root/pimm-gui.py &")
  destroy(win, event, args, kwargs)

def incoming_message(x):
  print "Query: " + x
  query = getDbusObject (bus, "org.freesmartphone.opimd", x, "org.freesmartphone.PIM.Message")
  result = query.GetContent()

  win = elementary.Window('pim-test', 1)
  win.title_set('Message - opimd')

  bg = elementary.Background(win)
  win.resize_object_add(bg)
  bg.show()

  mainbox = elementary.Box(win)
  mainbox.show()

  scroll = elementary.Scroller(win)
  win.resize_object_add(mainbox)
  scroll.show()
  bg.size_hint_min_set(100, 300)
  scroll.bounce_set(0, 1)
  scroll.size_hint_weight_set(1.0, 1.0)
  scroll.size_hint_align_set(-1.0, -1.0)
  mainbox.pack_start(scroll)

  box = elementary.Box(win)
  box.show()

  box.size_hint_weight_set(1.0, 0.0)
  box.size_hint_align_set(-1.0, -1.0)

  scroll.content_set(box)

  bubble = elementary.Bubble(win)
  text = elementary.AnchorBlock(win)

  text.text_set(result['Text'])

  read = elementary.Button(win)
  read.label_set("New message arrived!")
  read.clicked = partial(show_msg, text, bubble)
  read.show()

  bubble.label_set(resolve_phone(result['Sender']))
  bubble.content_set(read)
#  bubble.info_set(result['_backend_timestamp'])

  bubble.show()
  bubble.size_hint_weight_set(1.0, 0.0)
  bubble.size_hint_align_set(-1.0, -1.0)

  box.pack_start(bubble)

  boxb = elementary.Box(win)
  boxb.show()
  mainbox.pack_end(boxb)
  boxb.size_hint_weight_set(-1.0, 0.0)
  boxb.size_hint_align_set(-1.0, -1.0)
  boxb.horizontal_set(1)

  inbox = elementary.Button(win)
  inbox.show()
  inbox._callback_add("clicked", (open_inbox, win))
  inbox.size_hint_weight_set(1.0, 0.0)
  inbox.size_hint_align_set(-1.0, 0.0)
  inbox.label_set("Inbox")
  boxb.pack_start(inbox)

  delete = elementary.Button(win)
  delete.show()
  delete.size_hint_align_set(-1.0, 0.0)
  delete.clicked = partial(delete_msg, query, win)
  delete.label_set("Delete")
  boxb.pack_end(delete)

  close = elementary.Button(win)
  close.show()
  close.size_hint_align_set(-1.0, 0.0)
  close.clicked = partial(close_win, win)
  close.label_set("Close")
  boxb.pack_end(close)

  print "Finished" # finito, fertig, koniec etc.

  win.destroy = destroy
  win.show()

messages.connect_to_signal("IncomingMessage", incoming_message)

#incoming_message("/org/freesmartphone/PIM/Messages/0")

elementary.run()
elementary.shutdown()
