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
    init=True
except:
  pass

if init:
  print "Init entries"
  sources.InitAllEntries() # ATM should be called only once at one framework session, cause there is bug which causes duplicating of entries in opimd cache

messages = getDbusObject (bus, "org.freesmartphone.opimd", "/org/freesmartphone/PIM/Messages", "org.freesmartphone.PIM.Messages")
contacts = getDbusObject (bus, "org.freesmartphone.opimd", "/org/freesmartphone/PIM/Contacts", "org.freesmartphone.PIM.Contacts")

print "Querying..."
x = messages.Query({})

print "Query: " + x
query = getDbusObject (bus, "org.freesmartphone.opimd", x, "org.freesmartphone.PIM.MessageQuery")
total_results = query.GetResultCount()
print "Numer of results: " + str(total_results) 

elementary.init()
win = elementary.Window('pim-test', elementary.ELM_WIN_BASIC)
win.title_set('PIM test')

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

messages = []
msg_cache = {}

results = query.GetMultipleResults(total_results)

for i in results:
  #print "Result nr "+str(i+1)+":"
  #result = query.GetResult()

  cid = ''
  try:
    cid = results[i]['_backend_csm_id']
  except KeyError:
    pass

  if cid!='':
    if cid in msg_cache:
      messages[msg_cache[cid]].append(results[i])
    else:
      msg_cache[cid] = len(messages)
      messages.append([results[i]])
  else:
    messages.append([results[i]])
  
  #query.Skip(0) # skips one result. Skip(1) will skip two results, etc.


for message in messages:

  bubble = elementary.Bubble(win)
  text = elementary.AnchorBlock(win)
  text_msg = ''

  if len(message)>1:
    for i in range(1, len(message)+1):
      for msg in message:
        if msg['_backend_csm_seq']==i:
          text_msg += msg['Text']
  else:
    text_msg = message[0]['Text']

  text.text_set(text_msg)
  text.show()

  bubble.label_set(resolve_phone(message[0]['Sender']))
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
