#!/usr/bin/env python
import dbus
from sys import argv

def resolve_phone(number):
  x = contacts.Query({'Phone':number.strip('tel:')})
  query = getDbusObject (bus, "org.freesmartphone.opimd", x, "org.freesmartphone.PIM.ContactQuery")
  if query.GetResultCount()==1:
    name = query.GetResult()['Name']
  else:
    name = "nothing"
  query.Dispose()
  return name

def getDbusObject (bus, busname , objectpath , interface):
  dbusObject = bus.get_object(busname, objectpath)
  return dbus.Interface(dbusObject, dbus_interface=interface)

bus = dbus.SystemBus()

messages = getDbusObject (bus, "org.freesmartphone.opimd", "/org/freesmartphone/PIM/Messages", "org.freesmartphone.PIM.Messages")
contacts = getDbusObject (bus, "org.freesmartphone.opimd", "/org/freesmartphone/PIM/Contacts", "org.freesmartphone.PIM.Contacts")

for number in argv[1:]:
  print number+': '+resolve_phone(number)


