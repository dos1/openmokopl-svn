#!/usr/bin/env python
# -*- coding: utf-8 -*-

import dbus
from sys import argv
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

def destroy(obj, event, *args, **kargs):
  print "kabum"
  elementary.exit()

# define some nice dbus helper, which I really like, cause make code easier to read :)
def getDbusObject (bus, busname , objectpath , interface):
        dbusObject = bus.get_object(busname, objectpath)
        return dbus.Interface(dbusObject, dbus_interface=interface)

bus = dbus.SystemBus()

sources = getDbusObject (bus, "org.freesmartphone.opimd", "/org/freesmartphone/PIM/Sources", "org.freesmartphone.PIM.Sources")
init=False
try:
  if argv[1]=='init':
    print "Init entries..."
    sources.InitAllEntries()
except IndexError:
  pass

messages = getDbusObject (bus, "org.freesmartphone.opimd", "/org/freesmartphone/PIM/Messages", "org.freesmartphone.PIM.Messages")
contacts = getDbusObject (bus, "org.freesmartphone.opimd", "/org/freesmartphone/PIM/Contacts", "org.freesmartphone.PIM.Contacts")

print "Querying..."
x = messages.Query({})

print "Query: " + x
query = getDbusObject (bus, "org.freesmartphone.opimd", x, "org.freesmartphone.PIM.MessageQuery")
total_results = query.GetResultCount()
print "Number of results: " + str(total_results) 

elementary.init()
win = elementary.Window('pim-test', elementary.ELM_WIN_BASIC)
win.title_set('Messages - opimd')

bg = elementary.Background(win)
win.resize_object_add(bg)
bg.show()

scroll = elementary.Scroller(win)
win.resize_object_add(scroll)
scroll.show()

box = elementary.Box(win)
box.show()

box.size_hint_weight_set(1.0, 0.0)
box.size_hint_align_set(-1.0, -1.0)

scroll.content_set(box)

results = query.GetMultipleResults(total_results)

for i in results:
  #print "Result nr "+str(i+1)+":"
  #result = query.GetResult()

  bubble = elementary.Bubble(win)
  text = elementary.AnchorBlock(win)

  text.text_set(results[i]['Text'])
  text.show()

  bubble.label_set(resolve_phone(results[i]['Sender']))
  bubble.content_set(text)

  bubble.show()
  bubble.size_hint_weight_set(1.0, 0.0)
  bubble.size_hint_align_set(-1.0, -1.0)

  box.pack_start(bubble)

print "Finished" # finito, fertig, koniec etc.

win.destroy = destroy
win.show()
elementary.run()
elementary.shutdown()
