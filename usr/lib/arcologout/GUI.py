
# =====================================================
#                  Author Brad Heffernan
# =====================================================


def GUI(self, Gtk, GdkPixbuf, working_dir, os, Gdk):
    mainbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
    mainbox2 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)

    lblbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
    
    lbl = Gtk.Label(label="")

    self.lbl_stat = Gtk.Label()
    
    lblbox.pack_start(lbl, True, False, 0)
    lblbox.pack_start(self.lbl_stat, True, False, 0)

    overlayFrame = Gtk.Overlay()
    overlayFrame.add(lblbox)
    overlayFrame.add_overlay(mainbox)

    self.add(overlayFrame)

    vbox1 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
    vbox2 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
    vbox3 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
    vbox4 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
    vbox5 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
    vbox6 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
    vbox7 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)

    hbox1 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=30)

    self.Esh = Gtk.EventBox()
    self.Esh.connect("button_press_event", self.on_click, self.binds.get('shutdown'))
    self.Esh.connect("button-press-event", self.on_click)
    self.Esh.add_events(Gdk.EventMask.ENTER_NOTIFY_MASK)  # 1
    self.Esh.connect("enter-notify-event", self.on_mouse_in, self.binds.get('shutdown'))  # 2
    self.Esh.add_events(Gdk.EventMask.LEAVE_NOTIFY_MASK)  # 1
    self.Esh.connect("leave-notify-event", self.on_mouse_out, self.binds.get('shutdown'))  # 2

    self.Er = Gtk.EventBox()
    self.Er.connect("button_press_event", self.on_click, self.binds.get('restart'))
    self.Er.add_events(Gdk.EventMask.ENTER_NOTIFY_MASK)  # 1
    self.Er.connect("enter-notify-event", self.on_mouse_in, self.binds.get('restart'))  # 2
    self.Er.add_events(Gdk.EventMask.LEAVE_NOTIFY_MASK)  # 1
    self.Er.connect("leave-notify-event", self.on_mouse_out, self.binds.get('restart'))  # 2

    self.Es = Gtk.EventBox()
    self.Es.connect("button_press_event", self.on_click, self.binds.get('suspend'))
    self.Es.add_events(Gdk.EventMask.ENTER_NOTIFY_MASK)  # 1
    self.Es.connect("enter-notify-event", self.on_mouse_in, self.binds.get('suspend'))  # 2
    self.Es.add_events(Gdk.EventMask.LEAVE_NOTIFY_MASK)  # 1
    self.Es.connect("leave-notify-event", self.on_mouse_out, self.binds.get('suspend'))  # 2

    self.Elk = Gtk.EventBox()
    self.Elk.connect("button_press_event", self.on_click, self.binds.get('lock'))
    self.Elk.add_events(Gdk.EventMask.ENTER_NOTIFY_MASK)  # 1
    self.Elk.connect("enter-notify-event", self.on_mouse_in, self.binds.get('lock'))  # 2
    self.Elk.add_events(Gdk.EventMask.LEAVE_NOTIFY_MASK)  # 1
    self.Elk.connect("leave-notify-event", self.on_mouse_out, self.binds.get('lock'))  # 2

    self.El = Gtk.EventBox()
    self.El.connect("button_press_event", self.on_click, self.binds.get('logout'))
    self.El.add_events(Gdk.EventMask.ENTER_NOTIFY_MASK)  # 1
    self.El.connect("enter-notify-event", self.on_mouse_in, self.binds.get('logout'))  # 2
    self.El.add_events(Gdk.EventMask.LEAVE_NOTIFY_MASK)  # 1
    self.El.connect("leave-notify-event", self.on_mouse_out, self.binds.get('logout'))  # 2

    self.Ec = Gtk.EventBox()
    self.Ec.connect("button_press_event", self.on_click, self.binds.get('cancel'))
    self.Ec.add_events(Gdk.EventMask.ENTER_NOTIFY_MASK)  # 1
    self.Ec.connect("enter-notify-event", self.on_mouse_in, self.binds.get('cancel'))  # 2
    self.Ec.add_events(Gdk.EventMask.LEAVE_NOTIFY_MASK)  # 1
    self.Ec.connect("leave-notify-event", self.on_mouse_out, self.binds.get('cancel'))  # 2

    self.Eh = Gtk.EventBox()
    self.Eh.connect("button_press_event", self.on_click, self.binds.get('hibernate'))
    self.Eh.add_events(Gdk.EventMask.ENTER_NOTIFY_MASK)  # 1
    self.Eh.connect("enter-notify-event", self.on_mouse_in, self.binds.get('hibernate'))  # 2
    self.Eh.add_events(Gdk.EventMask.LEAVE_NOTIFY_MASK)  # 1
    self.Eh.connect("leave-notify-event", self.on_mouse_out, self.binds.get('hibernate'))  # 2

    for button in self.buttons:
        if button == "shutdown":
            psh = GdkPixbuf.Pixbuf().new_from_file_at_size(
                os.path.join(working_dir, 'themes/' + self.theme + '/shutdown.svg'), self.icon, self.icon)
            self.imagesh = Gtk.Image().new_from_pixbuf(psh)
            self.Esh.add(self.imagesh)
        if button == "cancel":
            pc = GdkPixbuf.Pixbuf().new_from_file_at_size(
                os.path.join(working_dir, 'themes/' + self.theme + '/cancel.svg'), self.icon, self.icon)
            self.imagec = Gtk.Image().new_from_pixbuf(pc)
            self.Ec.add(self.imagec)
        if button == "restart":
            pr = GdkPixbuf.Pixbuf().new_from_file_at_size(
                os.path.join(working_dir, 'themes/' + self.theme + '/restart.svg'), self.icon, self.icon)
            self.imager = Gtk.Image().new_from_pixbuf(pr)
            self.Er.add(self.imager)
        if button == "suspend":
            ps = GdkPixbuf.Pixbuf().new_from_file_at_size(
                os.path.join(working_dir, 'themes/' + self.theme + '/suspend.svg'), self.icon, self.icon)
            self.images = Gtk.Image().new_from_pixbuf(ps)
            self.Es.add(self.images)
        if button == "lock":
            plk = GdkPixbuf.Pixbuf().new_from_file_at_size(
                os.path.join(working_dir, 'themes/' + self.theme + '/lock.svg'), self.icon, self.icon)
            self.imagelk = Gtk.Image().new_from_pixbuf(plk)
            self.Elk.add(self.imagelk)
        if button == "logout":
            plo = GdkPixbuf.Pixbuf().new_from_file_at_size(
                os.path.join(working_dir, 'themes/' + self.theme + '/logout.svg'), self.icon, self.icon)
            self.imagelo = Gtk.Image().new_from_pixbuf(plo)
            self.El.add(self.imagelo)
        if button == "hibernate":
            ph = GdkPixbuf.Pixbuf().new_from_file_at_size(
                os.path.join(working_dir, 'themes/' + self.theme + '/hibernate.svg'), self.icon, self.icon)
            self.imageh = Gtk.Image().new_from_pixbuf(ph)
            self.Eh.add(self.imageh)

    self.lbl1 = Gtk.Label(label="Shutdown")
    self.lbl2 = Gtk.Label(label="Reboot")
    self.lbl3 = Gtk.Label(label="Suspend")
    self.lbl4 = Gtk.Label(label="Lock")
    self.lbl5 = Gtk.Label(label="Logout")
    self.lbl6 = Gtk.Label(label="Cancel")
    self.lbl7 = Gtk.Label(label="Hibernate")

    vbox1.pack_start(self.Esh, False, False, 0)
    vbox1.pack_start(self.lbl1, False, False, 0)
    vbox2.pack_start(self.Er, False, False, 0)
    vbox2.pack_start(self.lbl2, False, False, 0)
    vbox3.pack_start(self.Es, False, False, 0)
    vbox3.pack_start(self.lbl3, False, False, 0)
    vbox4.pack_start(self.Elk, False, False, 0)
    vbox4.pack_start(self.lbl4, False, False, 0)
    vbox5.pack_start(self.El, False, False, 0)
    vbox5.pack_start(self.lbl5, False, False, 0)
    vbox6.pack_start(self.Ec, False, False, 0)
    vbox6.pack_start(self.lbl6, False, False, 0)
    vbox7.pack_start(self.Eh, False, False, 0)
    vbox7.pack_start(self.lbl7, False, False, 0)

    for button in self.buttons:
        if button == "shutdown":
            hbox1.pack_start(vbox1, False, False, 20)
        if button == "cancel":
            hbox1.pack_start(vbox6, False, False, 20)
        if button == "restart":
            hbox1.pack_start(vbox2, False, False, 20)
        if button == "suspend":
            hbox1.pack_start(vbox3, False, False, 20)
        if button == "lock":
            hbox1.pack_start(vbox4, False, False, 20)
        if button == "logout":
            hbox1.pack_start(vbox5, False, False, 20)
        if button == "hibernate":
            hbox1.pack_start(vbox7, False, False, 20)

    mainbox2.pack_start(hbox1, True, False, 0)

    mainbox.pack_start(mainbox2, True, False, 0)
    # mainbox.pack_start(overlayFrame, False, False, 50)
