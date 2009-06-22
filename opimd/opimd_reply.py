import elementary, dbus
from functools import partial

def getDbusObject (bus, busname , objectpath , interface):
        dbusObject = bus.get_object(busname, objectpath)
        return dbus.Interface(dbusObject, dbus_interface=interface)


def send_msg(bus, to, entry, inwin, func, *args, **kwargs):
  ogsmd = getDbusObject (bus, "org.freesmartphone.ogsmd", "/org/freesmartphone/GSM/Device", "org.freesmartphone.GSM.SMS")
  msg = entry.entry_get().replace('<br>','')
  ogsmd.SendMessage(to[0].replace('tel:','') ,msg, {})
  messages = getDbusObject (bus, "org.freesmartphone.opimd", "/org/freesmartphone/PIM/Messages", "org.freesmartphone.PIM.Messages")
  func(messages.Add({'Recipient':to[0],'Direction':'out','Folder':'SMS','Text':msg}))
  inwin.delete()

def inwindelete(win, *args, **kwargs):
  win.delete()

def reply(bus, to, win, func, *args, **kwargs):
  inwin = elementary.InnerWindow(win)
  win.resize_object_add(inwin)
  inwin.show()
#  inwin.style_set("minimal")
  box = elementary.Box(inwin)
  box.show()
  label = elementary.Label(inwin)
  label.label_set("To: "+to[1])
  label.show()
  box.pack_start(label)
  scroll = elementary.Scroller(inwin)
  entry = elementary.Entry(inwin)
  entry.size_hint_weight_set(1.0, 1.0)
  entry.size_hint_align_set(-1.0, -1.0)
  entry.show()
  scroll.content_set(entry)
  scroll.size_hint_weight_set(1.0, 1.0)
  scroll.size_hint_align_set(-1.0, -1.0)
  scroll.show()
  box.pack_end(scroll)

  hbox = elementary.Box(win)
  hbox.horizontal_set(1)
  hbox.show()

  hide = elementary.Button(inwin)
  hide.label_set("Close")
  hide.show()
  hide.clicked = partial(inwindelete, inwin)
  hbox.pack_end(hide)

  send = elementary.Button(inwin)
  send.label_set("Send")
  send.show()
  send.clicked = partial(send_msg, bus, to, entry, inwin, func)

  hbox.pack_end(send)

  box.pack_end(hbox)

  box.size_hint_weight_set(-1.0, -1.0)
  box.size_hint_align_set(-1.0, -1.0)

  inwin.content_set(box)
  box.show()
  inwin.activate()

