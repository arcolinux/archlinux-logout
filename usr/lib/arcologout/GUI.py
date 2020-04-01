
# =====================================================
#                  Author Brad Heffernan
# =====================================================


def GUI(self, Gtk, GdkPixbuf, working_dir, os, Gdk):
    mainbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
    mainbox2 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    self.add(mainbox)

    vbox1 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
    vbox2 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
    vbox3 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
    vbox4 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
    vbox5 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)

    hbox1 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=30)

    Esh = Gtk.EventBox()
    Esh.connect("button_press_event", self.on_click, "S")
    Esh.connect("button-press-event", self.on_click)
    Esh.add_events(Gdk.EventMask.ENTER_NOTIFY_MASK)  # 1
    Esh.connect("enter-notify-event", self.on_mouse_in, "S")  # 2
    Esh.add_events(Gdk.EventMask.LEAVE_NOTIFY_MASK)  # 1
    Esh.connect("leave-notify-event", self.on_mouse_out, "S")  # 2

    Er = Gtk.EventBox()
    Er.connect("button_press_event", self.on_click, "R")
    Er.add_events(Gdk.EventMask.ENTER_NOTIFY_MASK)  # 1
    Er.connect("enter-notify-event", self.on_mouse_in, "R")  # 2
    Er.add_events(Gdk.EventMask.LEAVE_NOTIFY_MASK)  # 1
    Er.connect("leave-notify-event", self.on_mouse_out, "R")  # 2

    Es = Gtk.EventBox()
    Es.connect("button_press_event", self.on_click, "U")
    Es.add_events(Gdk.EventMask.ENTER_NOTIFY_MASK)  # 1
    Es.connect("enter-notify-event", self.on_mouse_in, "U")  # 2
    Es.add_events(Gdk.EventMask.LEAVE_NOTIFY_MASK)  # 1
    Es.connect("leave-notify-event", self.on_mouse_out, "U")  # 2

    Elk = Gtk.EventBox()
    Elk.connect("button_press_event", self.on_click, "K")
    Elk.add_events(Gdk.EventMask.ENTER_NOTIFY_MASK)  # 1
    Elk.connect("enter-notify-event", self.on_mouse_in, "K")  # 2
    Elk.add_events(Gdk.EventMask.LEAVE_NOTIFY_MASK)  # 1
    Elk.connect("leave-notify-event", self.on_mouse_out, "K")  # 2

    El = Gtk.EventBox()
    El.connect("button_press_event", self.on_click, "L")
    El.add_events(Gdk.EventMask.ENTER_NOTIFY_MASK)  # 1
    El.connect("enter-notify-event", self.on_mouse_in, "L")  # 2
    El.add_events(Gdk.EventMask.LEAVE_NOTIFY_MASK)  # 1
    El.connect("leave-notify-event", self.on_mouse_out, "L")  # 2

    psh = GdkPixbuf.Pixbuf().new_from_file_at_size(
        os.path.join(working_dir, 'shutdown.svg'), 64, 64)
    self.imagesh = Gtk.Image().new_from_pixbuf(psh)

    pr = GdkPixbuf.Pixbuf().new_from_file_at_size(
        os.path.join(working_dir, 'restart.svg'), 64, 64)
    self.imager = Gtk.Image().new_from_pixbuf(pr)

    ps = GdkPixbuf.Pixbuf().new_from_file_at_size(
        os.path.join(working_dir, 'suspend.svg'), 64, 64)
    self.images = Gtk.Image().new_from_pixbuf(ps)

    plk = GdkPixbuf.Pixbuf().new_from_file_at_size(
        os.path.join(working_dir, 'lock.svg'), 64, 64)
    self.imagelk = Gtk.Image().new_from_pixbuf(plk)

    plo = GdkPixbuf.Pixbuf().new_from_file_at_size(
        os.path.join(working_dir, 'logout.svg'), 64, 64)
    self.imagelo = Gtk.Image().new_from_pixbuf(plo)

    Esh.add(self.imagesh)
    Er.add(self.imager)
    Es.add(self.images)
    Elk.add(self.imagelk)
    El.add(self.imagelo)

    lbl1 = Gtk.Label(label="Shutdown")
    lbl2 = Gtk.Label(label="Reboot")
    lbl3 = Gtk.Label(label="Suspend")
    lbl4 = Gtk.Label(label="Lock")
    lbl5 = Gtk.Label(label="Logout")

    vbox1.pack_start(Esh, False, False, 0)
    vbox1.pack_start(lbl1, False, False, 0)
    vbox2.pack_start(Er, False, False, 0)
    vbox2.pack_start(lbl2, False, False, 0)
    vbox3.pack_start(Es, False, False, 0)
    vbox3.pack_start(lbl3, False, False, 0)
    vbox4.pack_start(Elk, False, False, 0)
    vbox4.pack_start(lbl4, False, False, 0)
    vbox5.pack_start(El, False, False, 0)
    vbox5.pack_start(lbl5, False, False, 0)

    hbox1.pack_start(vbox1, False, False, 30)
    hbox1.pack_start(vbox2, False, False, 30)
    hbox1.pack_start(vbox3, False, False, 30)
    hbox1.pack_start(vbox4, False, False, 30)
    hbox1.pack_start(vbox5, False, False, 30)

    mainbox2.pack_start(hbox1, True, False, 0)

    mainbox.pack_start(mainbox2, True, False, 0)
