
# =====================================================
#        Authors Brad Heffernan and Erik Dubois
# =====================================================


def GUI(self, Gtk, GdkPixbuf, working_dir, os, Gdk, fn):
    container = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    spacer = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    mainbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
    mainbox2 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    mainbox4 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
    mainbox3 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
    lblbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)

    lbl = Gtk.Label(label="")

    self.lbl_stat = Gtk.Label()

    lblbox.pack_start(lbl, True, False, 0)
    lblbox.pack_start(self.lbl_stat, True, False, 0)

    overlayFrame = Gtk.Overlay()
    overlayFrame.add(lblbox)
    overlayFrame.add_overlay(mainbox)

    self.add(overlayFrame)

    self.Eset = Gtk.EventBox()
    self.Eset.set_name("settings")
    self.Eset.connect("button_press_event", self.on_click, self.binds['settings'])
    self.Eset.add_events(Gdk.EventMask.ENTER_NOTIFY_MASK)  # 1
    self.Eset.connect("enter-notify-event", self.on_mouse_in, self.binds['settings'])  # 2
    self.Eset.add_events(Gdk.EventMask.LEAVE_NOTIFY_MASK)  # 1
    self.Eset.connect("leave-notify-event", self.on_mouse_out, self.binds['settings'])  # 2

    pset = GdkPixbuf.Pixbuf().new_from_file_at_size(
        os.path.join(working_dir, 'configure.svg'), 48, 48)
    self.imageset = Gtk.Image().new_from_pixbuf(pset)
    self.Eset.add(self.imageset)

    self.Elig = Gtk.EventBox()
    self.Elig.set_name("light")
    self.Elig.connect("button_press_event", self.on_click, 'light')
    self.Elig.add_events(Gdk.EventMask.ENTER_NOTIFY_MASK)  # 1
    self.Elig.connect("enter-notify-event", self.on_mouse_in, 'light')
    self.Elig.add_events(Gdk.EventMask.LEAVE_NOTIFY_MASK)  # 1
    self.Elig.connect("leave-notify-event", self.on_mouse_out, 'light')

    plig = GdkPixbuf.Pixbuf().new_from_file_at_size(
        os.path.join(working_dir, 'light.svg'), 48, 48)
    self.imagelig = Gtk.Image().new_from_pixbuf(plig)
    self.Elig.add(self.imagelig)

    vbox1 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
    vbox2 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
    vbox3 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
    vbox4 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
    vbox5 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
    vbox6 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
    vbox7 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
    hbox17 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)

    hbox1 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=30)

    self.Esh = Gtk.EventBox()
    self.Esh.connect("button_press_event", self.on_click, self.binds['shutdown'])
    self.Esh.add_events(Gdk.EventMask.ENTER_NOTIFY_MASK)  # 1
    self.Esh.connect("enter-notify-event", self.on_mouse_in, self.binds['shutdown'])  # 2
    self.Esh.add_events(Gdk.EventMask.LEAVE_NOTIFY_MASK)  # 1
    self.Esh.connect("leave-notify-event", self.on_mouse_out, self.binds['shutdown'])  # 2

    self.Er = Gtk.EventBox()
    self.Er.connect("button_press_event", self.on_click, self.binds['restart'])
    self.Er.add_events(Gdk.EventMask.ENTER_NOTIFY_MASK)  # 1
    self.Er.connect("enter-notify-event", self.on_mouse_in, self.binds['restart'])  # 2
    self.Er.add_events(Gdk.EventMask.LEAVE_NOTIFY_MASK)  # 1
    self.Er.connect("leave-notify-event", self.on_mouse_out, self.binds['restart'])  # 2

    self.Es = Gtk.EventBox()
    self.Es.connect("button_press_event", self.on_click, self.binds['suspend'])
    self.Es.add_events(Gdk.EventMask.ENTER_NOTIFY_MASK)  # 1
    self.Es.connect("enter-notify-event", self.on_mouse_in, self.binds['suspend'])  # 2
    self.Es.add_events(Gdk.EventMask.LEAVE_NOTIFY_MASK)  # 1
    self.Es.connect("leave-notify-event", self.on_mouse_out, self.binds['suspend'])  # 2

    self.Elk = Gtk.EventBox()
    self.Elk.connect("button_press_event", self.on_click, self.binds['lock'])
    self.Elk.add_events(Gdk.EventMask.ENTER_NOTIFY_MASK)  # 1
    self.Elk.connect("enter-notify-event", self.on_mouse_in, self.binds['lock'])  # 2
    self.Elk.add_events(Gdk.EventMask.LEAVE_NOTIFY_MASK)  # 1
    self.Elk.connect("leave-notify-event", self.on_mouse_out, self.binds['lock'])  # 2

    self.El = Gtk.EventBox()
    self.El.connect("button_press_event", self.on_click, self.binds['logout'])
    self.El.add_events(Gdk.EventMask.ENTER_NOTIFY_MASK)  # 1
    self.El.connect("enter-notify-event", self.on_mouse_in, self.binds['logout'])  # 2
    self.El.add_events(Gdk.EventMask.LEAVE_NOTIFY_MASK)  # 1
    self.El.connect("leave-notify-event", self.on_mouse_out, self.binds['logout'])  # 2

    self.Ec = Gtk.EventBox()
    self.Ec.connect("button_press_event", self.on_click, self.binds['cancel'])
    self.Ec.add_events(Gdk.EventMask.ENTER_NOTIFY_MASK)  # 1
    self.Ec.connect("enter-notify-event", self.on_mouse_in, self.binds['cancel'])  # 2
    self.Ec.add_events(Gdk.EventMask.LEAVE_NOTIFY_MASK)  # 1
    self.Ec.connect("leave-notify-event", self.on_mouse_out, self.binds['cancel'])  # 2

    self.Eh = Gtk.EventBox()
    self.Eh.connect("button_press_event", self.on_click, self.binds['hibernate'])
    self.Eh.add_events(Gdk.EventMask.ENTER_NOTIFY_MASK)  # 1
    self.Eh.connect("enter-notify-event", self.on_mouse_in, self.binds['hibernate'])  # 2
    self.Eh.add_events(Gdk.EventMask.LEAVE_NOTIFY_MASK)  # 1
    self.Eh.connect("leave-notify-event", self.on_mouse_out, self.binds['hibernate'])  # 2

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

    self.lbl1 = Gtk.Label()
    self.lbl1.set_markup("<span size=\"" + str(self.font) + "000\">Shutdown (S)</span>")
    self.lbl1.set_name("lbl")
    self.lbl2 = Gtk.Label()
    self.lbl2.set_markup("<span size=\"" + str(self.font) + "000\">Reboot (R)</span>")
    self.lbl2.set_name("lbl")
    self.lbl3 = Gtk.Label()
    self.lbl3.set_markup("<span size=\"" + str(self.font) + "000\">Suspend (U)</span>")
    self.lbl3.set_name("lbl")
    self.lbl4 = Gtk.Label()
    self.lbl4.set_markup("<span size=\"" + str(self.font) + "000\">Lock (K)</span>")
    self.lbl4.set_name("lbl")
    self.lbl5 = Gtk.Label()
    self.lbl5.set_markup("<span size=\"" + str(self.font) + "000\">Logout (L)</span>")
    self.lbl5.set_name("lbl")
    self.lbl6 = Gtk.Label()
    self.lbl6.set_markup("<span size=\"" + str(self.font) + "000\">Cancel (ESC)</span>")
    self.lbl6.set_name("lbl")
    self.lbl7 = Gtk.Label()
    self.lbl7.set_markup("<span size=\"" + str(self.font) + "000\">Hibernate (H)</span>")
    self.lbl7.set_name("lbl")
    
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

    # mainbox4.pack_start(self.Elig, False, False, 0)
    
    # mainbox3.pack_end(mainbox4, False, False, 0)

    # spacers
    hbox17.pack_start(self.Elig, False, False, 0)
    hbox17.pack_start(self.Eset, False, False, 0)
    mainbox.pack_start(hbox17, False, False, 0)
    # mainbox.pack_start(Gtk.Label(), False, False, 0)
    # mainbox.pack_start(Gtk.Label(), False, False, 0)

    # mainbox.pack_end(mainbox3, False, False, 0)
    mainbox.pack_start(mainbox2, True, False, 0)
    # mainbox.set_size_request(self.single_width, 0)
    # container.pack_start(mainbox, False, False, 0)
    # if self.single_width < self.width:
    #     container.pack_start(spacer, True, True, 0)
    #     spacer.pack_start(Gtk.Label(label=""), True, True, 0)

    self.popover = Gtk.Popover()
    self.popover2 = Gtk.Popover()
    vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
    hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=20)
    hbox3 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=20)
    hbox4 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=20)
    hbox5 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=20)
    hbox6 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=20)

    lbl8 = Gtk.Label(label="Opacity:")
    lbl9 = Gtk.Label(label="Icon size:")
    lbl10 = Gtk.Label(label="Theme:")
    lbl11 = Gtk.Label(label="Font size:")
    # lbl11 = Gtk.Label(label="Wallpaper:")
    try:
        vals = self.opacity*100
        ad1 = Gtk.Adjustment(vals, 0, 100, 5, 10, 0)
    except:
        ad1 = Gtk.Adjustment(60, 0, 100, 5, 10, 0)

    self.hscale = Gtk.Scale(
        orientation=Gtk.Orientation.HORIZONTAL, adjustment=ad1)
    self.hscale.set_digits(0)
    self.hscale.set_hexpand(True)
    self.hscale.set_size_request(150, 0)
    self.hscale.set_valign(Gtk.Align.START)
    # self.wall = Gtk.Entry()
    # self.wall.set_size_request(180, 0)
    # self.wall.set_width_chars(True)
    # self.wall.set_text(self.wallpaper)

    # self.hscale = Gtk.Entry()
    # self.hscale.set_size_request(80, 0)
    # self.hscale.set_width_chars(True)
    # self.hscale.set_text(str(int(self.opacity*100)))

    try:
        vals = self.font
        ad1f = Gtk.Adjustment(vals, 0, 80, 5, 10, 0)
    except:
        ad1f = Gtk.Adjustment(60, 0, 80, 5, 10, 0)

    self.fonts = Gtk.Scale(
        orientation=Gtk.Orientation.HORIZONTAL, adjustment=ad1f)
    self.fonts.set_digits(0)
    self.fonts.set_hexpand(True)
    self.fonts.set_size_request(150, 0)
    self.fonts.set_valign(Gtk.Align.START)

    try:
        valsi = self.icon
        ad1i = Gtk.Adjustment(valsi, 0, 300, 5, 10, 0)
    except:
        ad1i = Gtk.Adjustment(60, 0, 300, 5, 10, 0)

    self.icons = Gtk.Scale(
        orientation=Gtk.Orientation.HORIZONTAL, adjustment=ad1i)
    self.icons.set_digits(0)
    self.icons.set_hexpand(True)
    self.icons.set_size_request(150, 0)
    self.icons.set_valign(Gtk.Align.START)

    # self.icons = Gtk.Entry()
    # self.icons.set_size_request(80, 0)
    # self.icons.set_width_chars(True)
    # self.icons.set_text(str(self.icon))

    # self.hovers = Gtk.Entry()
    # self.hovers.set_size_request(80, 0)
    # self.hovers.set_width_chars(True)
    # self.hovers.set_text(str(self.hover))

    self.themes = Gtk.ComboBoxText()
    lists = fn._get_themes()
    active = 0
    for x in range(len(lists)):
        self.themes.append_text(lists[x])
        if lists[x] == self.theme:
            active = x
    self.themes.set_active(active)

    btn = Gtk.Button(label="Save Settings")
    btn.connect('clicked', self.on_save_clicked)

    hbox3.pack_end(btn, False, False, 10)

    hbox.pack_start(lbl8, False, False, 10)
    hbox.pack_end(self.hscale, False, False, 10)

    hbox4.pack_start(lbl9, False, False, 10)
    hbox4.pack_end(self.icons, False, False, 10)

    hbox5.pack_start(lbl10, False, False, 10)
    hbox5.pack_end(self.themes, False, False, 10)

    hbox6.pack_start(lbl11, False, False, 10)
    hbox6.pack_end(self.fonts, False, False, 10)

    vbox.pack_start(hbox, False, True, 10)
    vbox.pack_start(hbox4, False, True, 10)
    vbox.pack_start(hbox6, False, True, 10)
    vbox.pack_start(hbox5, False, True, 10)
    vbox.pack_end(hbox3, False, True, 10)

    self.popover.add(vbox)
    self.popover.set_position(Gtk.PositionType.TOP)

    hbox8 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=20)

    plbl = Gtk.Label()
    plbl.set_markup("<span size=\"large\">You can change the lockscreen wallpaper\nwith <b>Archlinux BetterLockScreen</b></span>")

    hbox8.pack_end(plbl, False, False, 10)

    self.popover2.add(hbox8)
    self.popover2.set_position(Gtk.PositionType.TOP)
