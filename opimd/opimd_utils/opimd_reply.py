
import elementary, dbus
from functools import partial

def getDbusObject (bus, busname , objectpath , interface):
        dbusObject = bus.get_object(busname, objectpath)
        return dbus.Interface(dbusObject, dbus_interface=interface)

def dbus_ok():
  pass

def dbus_err(x):
  print "notice: dbus error: "+str(x)

def dbus_sms_ok(x, bus, a, b):
  message = getDbusObject (bus, "org.freesmartphone.opimd", x, "org.freesmartphone.PIM.Message")
  data = {'MessageSent':1, 'Processing':0, 'SMS-message-reference':a}
  message.Update(data, reply_handler=dbus_ok, error_handler=dbus_err)
#  print a
#  print b

def dbus_opimd_ok(to, msg, props, bus, win, func_ok, func_err, x):
  if callable(func_ok):
    func_ok(x)
  try:
    ogsmd = getDbusObject (bus, "org.freesmartphone.ogsmd", "/org/freesmartphone/GSM/Device", "org.freesmartphone.GSM.SMS")
    ogsmd.SendMessage(to[0].replace('tel:','') ,msg, props, reply_handler=partial(dbus_sms_ok, x, bus), error_handler=partial(dbus_gsm_err, to, msg, props, x, bus, win, func_ok, func_err) )
  except dbus.exceptions.DBusException, e:
    dbus_gsm_err(to, msg, props, x, bus, win, func_ok, func_err, e)

def retry_msg(to, text, bus, win, inwin, func_ok, func_err, *args, **kwargs ):
  inwindelete(inwin)
  reply(to, text, bus, win, func_ok, func_err)

def dbus_gsm_err(to, text, props, x, bus, win, func_ok, func_err, dx):
  message = getDbusObject (bus, "org.freesmartphone.opimd", x, "org.freesmartphone.PIM.Message")
  data = {'Processing':0}
  message.Update(data, reply_handler=dbus_ok, error_handler=dbus_err)

  inwin = elementary.InnerWindow(win)
  inwin.show()
  inwin.style_set("vertical-minimal")
  win.resize_object_add(inwin)
  box = elementary.Box(inwin)
  box.show()
  inwin.content_set(box)
  label = elementary.Label(inwin)
  label.label_set("Error while sending message!")
  label.show()
  box.pack_start(label)
  sc = elementary.Scroller(inwin)
  sc.bounce_set(0, 0)
  sc.show()
  anchor = elementary.AnchorBlock(inwin)
  anchor.text_set(str(dx))
  anchor.show()
  sc.content_set(anchor)
  sc.size_hint_weight_set(1.0, 1.0)
  sc.size_hint_align_set(-1.0, -1.0)
  box.pack_end(sc)

  hbox = elementary.Box(inwin)
  hbox.horizontal_set(1)
  hbox.show()

  retry = elementary.Button(inwin)
  retry.label_set("Retry")
  retry.show()
  retry.clicked = partial(retry_msg, to, text, bus, win, inwin, func_ok, func_err)
  hbox.pack_end(retry)

  hide = elementary.Button(inwin)
  hide.label_set("Close")
  hide.show()
  hide.clicked = partial(inwindelete, inwin)
  hbox.pack_end(hide)  

  box.pack_end(hbox)

  if callable(func_err):
    func_err()

  inwin.activate()

def dbus_opimd_err(to, msg, props, bus, win, func_ok, func_err, x):
  # TODO: call the same code, as dbus_gsm_err
  print "dbus error! "+str(x)

def send_msg(to, entry, bus, inwin, win, func_ok, func_err, *args, **kwargs):
  msg = entry.entry_get().replace('<br>','')
#  props = {'status-report-request':1}
  props = {}

#  ogsmd.SendMessage(to[0].replace('tel:','') ,msg, props, reply_handler=dbus_sms_ok, error_handler=partial(dbus_gsm_err, to, msg, bus, win, func_ok, func_err) )

  message = {'Recipient':to[0],'Direction':'out','Folder':'SMS','Content':msg, 'MessageSent':0, 'Processing':1}

  for field in props:
    message['SMS-'+field]=props[field]

  messages = getDbusObject (bus, "org.freesmartphone.opimd", "/org/freesmartphone/PIM/Messages", "org.freesmartphone.PIM.Messages")
  messages.Add(message, reply_handler=partial(dbus_opimd_ok, to, msg, props, bus, win, func_ok, func_err), error_handler=partial(dbus_opimd_err, to, msg, props, bus, win, func_ok, func_err))

  inwin.delete()

def inwindelete(win, *args, **kwargs):
  win.delete()

def update_chars(label, obj, event, *args, **kwargs):
  label.label_set("(%d)" % len(obj.entry_get().replace('<br>','')))

def reply(to, text, bus, win, func_ok, func_err, *args, **kwargs):
  inwin = elementary.InnerWindow(win)
  win.resize_object_add(inwin)
  inwin.show()
#  inwin.style_set("minimal")
  box = elementary.Box(inwin)
  box.show()

  tbox = elementary.Box(inwin)
  tbox.show()
  tbox.horizontal_set(1)  

  label = elementary.Label(inwin)
  label.label_set("To: "+to[1])
  label.show()
  tbox.pack_start(label)

  chars = elementary.Label(inwin)
  chars.label_set("(%d)" % len(text))
  chars.show()
  tbox.pack_end(chars)

  tbox.size_hint_weight_set(-1.0, 0.0)
  tbox.size_hint_align_set(-1.0, -1.0)

  chars.size_hint_weight_set(1.0, 0.0)
  chars.size_hint_align_set(1.0, -1.0)

  box.pack_start(tbox)
  scroll = elementary.Scroller(inwin)
  entry = elementary.Entry(inwin)
  entry.entry_set(text)
  entry.changed = partial(update_chars, chars)
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
  send.clicked = partial(send_msg, to, entry, bus, inwin, win, func_ok, func_err)

  hbox.pack_start(send)

  box.pack_end(hbox)

  box.size_hint_weight_set(-1.0, -1.0)
  box.size_hint_align_set(-1.0, -1.0)

  inwin.content_set(box)
  box.show()
  inwin.activate()

