# =====================================================
#                  Author Brad Heffernan
# =====================================================

import cairo
import gi
import shutil
import GUI
import Functions as fn
import threading

gi.require_version('Gtk', '3.0')
gi.require_version('Gdk', '3.0')
gi.require_version('Wnck', '3.0')

from gi.repository import Gtk, GdkPixbuf, Gdk, Wnck, GLib, GdkX11  # noqa


class TransparentWindow(Gtk.Window):
    cmd_shutdown = "systemctl poweroff"
    cmd_restart = "systemctl reboot"
    cmd_suspend = "systemctl suspend"
    cmd_hibernate = "systemctl hibernate"
    cmd_lock = "betterlockscreen -l dimblur"
    wallpaper = ""
    d_buttons = ['cancel',
                 'shutdown',
                 'restart',
                 'suspend',
                 'hibernate',
                 'lock',
                 'logout']
    binds = {'lock': 'K',
             'restart': 'R',
             'shutdown': 'S',
             'suspend': 'U',
             'hibernate': 'H',
             'logout': 'L',
             'cancel': 'Escape'}
    theme = "standard"
    buttons = None
    active = False

    def __init__(self):
        super(TransparentWindow, self).__init__(title="Arcolinux Logout")
        self.set_size_request(300, 220)
        self.monitor = 0
        self.connect('delete-event', self.on_close)
        self.connect('draw', self.draw)
        self.connect("key-press-event", self.on_keypress)
        self.connect("window-state-event", self.on_window_state_event)
        self.set_decorated(False)
        self.set_position(Gtk.WindowPosition.CENTER)

        if not fn.os.path.isdir(fn.home + "/.config/arcologout"):
            fn.os.mkdir(fn.home + "/.config/arcologout")

        if not fn.os.path.isfile(fn.home + "/.config/arcologout/arcologout.conf"):
            shutil.copy("/etc/arcologout.conf", fn.home + "/.config/arcologout/arcologout.conf")

        screen = self.get_screen()

        screens = Gdk.Display.get_default()
        monitor = screens.get_monitor(0)
        rect = monitor.get_geometry()

        width = rect.width
        height = rect.height

        self.resize(width, height)

        visual = screen.get_rgba_visual()
        if visual and screen.is_composited():
            self.set_visual(visual)

        fn.get_config(self, Gdk, fn.config)

        if self.buttons is None or self.buttons == ['']:
            self.buttons = self.d_buttons

        self.fullscreen()
        self.set_app_paintable(True)
        GUI.GUI(self, Gtk, GdkPixbuf, fn.working_dir, fn.os, Gdk, fn)
        if not fn.os.path.isfile("/tmp/arcologout.lock"):
            with open("/tmp/arcologout.lock", "w") as f:
                f.write("")

    def on_save_clicked(self, widget):
        with open(fn.home + "/.config/arcologout/arcologout.conf", "r") as f:
            lines = f.readlines()
            f.close()

        pos_opacity = fn._get_position(lines, "opacity")
        pos_size = fn._get_position(lines, "icon_size")
        pos_theme = fn._get_position(lines, "theme=")
        pos_wall = fn._get_position(lines, "lock_wallpaper")

        lines[pos_opacity] = "opacity=" + str(int(self.hscale.get_text())) + "\n"
        lines[pos_size] = "icon_size=" + str(int(self.icons.get_text())) + "\n"
        lines[pos_theme] = "theme=" + self.themes.get_active_text() + "\n"
        lines[pos_wall] = "lock_wallpaper=" + self.wall.get_text() + "\n"

        with open(fn.home + "/.config/arcologout/arcologout.conf", "w") as f:
            f.writelines(lines)
            f.close()
        self.popover.popdown()

    def on_mouse_in(self, widget, event, data):
        if data == self.binds.get('shutdown'):
            psh = GdkPixbuf.Pixbuf().new_from_file_at_size(
                fn.os.path.join(fn.working_dir, 'themes/' + self.theme + '/shutdown_blur.svg'), self.icon, self.icon)
            self.imagesh.set_from_pixbuf(psh)
            self.lbl1.set_markup("<span foreground=\"white\">Shutdown</span>")
        elif data == self.binds.get('restart'):
            pr = GdkPixbuf.Pixbuf().new_from_file_at_size(
                fn.os.path.join(fn.working_dir, 'themes/' + self.theme + '/restart_blur.svg'), self.icon, self.icon)
            self.imager.set_from_pixbuf(pr)
            self.lbl2.set_markup("<span foreground=\"white\">Restart</span>")
        elif data == self.binds.get('suspend'):
            ps = GdkPixbuf.Pixbuf().new_from_file_at_size(
                fn.os.path.join(fn.working_dir, 'themes/' + self.theme + '/suspend_blur.svg'), self.icon, self.icon)
            self.images.set_from_pixbuf(ps)
            self.lbl3.set_markup("<span foreground=\"white\">Suspend</span>")
        elif data == self.binds.get('lock'):
            plk = GdkPixbuf.Pixbuf().new_from_file_at_size(
                fn.os.path.join(fn.working_dir, 'themes/' + self.theme + '/lock_blur.svg'), self.icon, self.icon)
            self.imagelk.set_from_pixbuf(plk)
            self.lbl4.set_markup("<span foreground=\"white\">Lock</span>")
        elif data == self.binds.get('logout'):
            plo = GdkPixbuf.Pixbuf().new_from_file_at_size(
                fn.os.path.join(fn.working_dir, 'themes/' + self.theme + '/logout_blur.svg'), self.icon, self.icon)
            self.imagelo.set_from_pixbuf(plo)
            self.lbl5.set_markup("<span foreground=\"white\">Logout</span>")
        elif data == self.binds.get('cancel'):
            plo = GdkPixbuf.Pixbuf().new_from_file_at_size(
                fn.os.path.join(fn.working_dir, 'themes/' + self.theme + '/cancel_blur.svg'), self.icon, self.icon)
            self.imagec.set_from_pixbuf(plo)
            self.lbl6.set_markup("<span foreground=\"white\">Cancel</span>")
        elif data == self.binds.get('hibernate'):
            plo = GdkPixbuf.Pixbuf().new_from_file_at_size(
                fn.os.path.join(fn.working_dir, 'themes/' + self.theme + '/hibernate_blur.svg'), self.icon, self.icon)
            self.imageh.set_from_pixbuf(plo)
            self.lbl7.set_markup("<span foreground=\"white\">Hibernate</span>")
        elif data == self.binds.get('settings'):
            pset = GdkPixbuf.Pixbuf().new_from_file_at_size(
                fn.os.path.join(fn.working_dir, 'configure_blur.svg'), 48, 48)
            self.imageset.set_from_pixbuf(pset)
        event.window.set_cursor(Gdk.Cursor(Gdk.CursorType.HAND2))

    def on_mouse_out(self, widget, event, data):
        if not self.active:
            if data == "S":
                psh = GdkPixbuf.Pixbuf().new_from_file_at_size(
                    fn.os.path.join(fn.working_dir, 'themes/' + self.theme + '/shutdown.svg'), self.icon, self.icon)
                self.imagesh.set_from_pixbuf(psh)
                self.lbl1.set_markup("Shutdown")
            elif data == self.binds.get('restart'):
                pr = GdkPixbuf.Pixbuf().new_from_file_at_size(
                    fn.os.path.join(fn.working_dir, 'themes/' + self.theme + '/restart.svg'), self.icon, self.icon)
                self.imager.set_from_pixbuf(pr)
                self.lbl2.set_markup("Reboot")
            elif data == self.binds.get('suspend'):
                ps = GdkPixbuf.Pixbuf().new_from_file_at_size(
                    fn.os.path.join(fn.working_dir, 'themes/' + self.theme + '/suspend.svg'), self.icon, self.icon)
                self.images.set_from_pixbuf(ps)
                self.lbl3.set_markup("Suspend")
            elif data == self.binds.get('lock'):
                plk = GdkPixbuf.Pixbuf().new_from_file_at_size(
                    fn.os.path.join(fn.working_dir, 'themes/' + self.theme + '/lock.svg'), self.icon, self.icon)
                self.imagelk.set_from_pixbuf(plk)
                self.lbl4.set_markup("Lock")
            elif data == self.binds.get('logout'):
                plo = GdkPixbuf.Pixbuf().new_from_file_at_size(
                    fn.os.path.join(fn.working_dir, 'themes/' + self.theme + '/logout.svg'), self.icon, self.icon)
                self.imagelo.set_from_pixbuf(plo)
                self.lbl5.set_markup("Logout")
            elif data == self.binds.get('cancel'):
                plo = GdkPixbuf.Pixbuf().new_from_file_at_size(
                    fn.os.path.join(fn.working_dir, 'themes/' + self.theme + '/cancel.svg'), self.icon, self.icon)
                self.imagec.set_from_pixbuf(plo)
                self.lbl6.set_markup("Cancel")
            elif data == self.binds.get('hibernate'):
                plo = GdkPixbuf.Pixbuf().new_from_file_at_size(
                    fn.os.path.join(fn.working_dir, 'themes/' + self.theme + '/hibernate.svg'), self.icon, self.icon)
                self.imageh.set_from_pixbuf(plo)
                self.lbl7.set_markup("Hibernate")
            elif data == self.binds.get('settings'):
                pset = GdkPixbuf.Pixbuf().new_from_file_at_size(
                    fn.os.path.join(fn.working_dir, 'configure.svg'), 48, 48)
                self.imageset.set_from_pixbuf(pset)

    def on_click(self, widget, event, data):
        self.click_button(widget, data)

    def on_window_state_event(self, widget, ev):
        self.__is_fullscreen = bool(ev.new_window_state & Gdk.WindowState.FULLSCREEN)  # noqa

    def draw(self, widget, context):
        context.set_source_rgba(0, 0, 0, self.opacity)
        context.set_operator(cairo.OPERATOR_SOURCE)
        context.paint()
        context.set_operator(cairo.OPERATOR_OVER)

    def on_keypress(self, widget=None, event=None, data=None):
        self.shortcut_keys = [self.binds.get('cancel'), self.binds.get('shutdown'), self.binds.get('restart'), self.binds.get('suspend'), self.binds.get('logout'), self.binds.get('lock'), self.binds.get('hibernate'), self.binds.get('settings')]

        for key in self.shortcut_keys:
            if event.keyval == Gdk.keyval_to_lower(Gdk.keyval_from_name(key)):
                self.click_button(widget, key)

    def click_button(self, widget, data=None):

        if not data == self.binds.get('settings'):
            self.active = True
            fn.button_toggled(self, data)
            fn.button_active(self, data, GdkPixbuf)
        if (data == self.binds.get('logout')):
            command = fn._get_logout()
            fn.os.unlink("/tmp/arcologout.lock")
            self.__exec_cmd(command)
            Gtk.main_quit()

        elif (data == self.binds.get('restart')):
            fn.os.unlink("/tmp/arcologout.lock")
            self.__exec_cmd(self.cmd_restart)
            Gtk.main_quit()

        elif (data == self.binds.get('shutdown')):
            fn.os.unlink("/tmp/arcologout.lock")
            self.__exec_cmd(self.cmd_shutdown)
            Gtk.main_quit()

        elif (data == self.binds.get('suspend')):
            fn.os.unlink("/tmp/arcologout.lock")
            self.__exec_cmd(self.cmd_suspend)
            Gtk.main_quit()

        elif (data == self.binds.get('hibernate')):
            fn.os.unlink("/tmp/arcologout.lock")
            self.__exec_cmd(self.cmd_hibernate)
            Gtk.main_quit()

        elif (data == self.binds.get('lock')):
            if not fn.os.path.isdir(fn.home + "/.cache/i3lock"):
                if fn.os.path.isfile(self.wallpaper):
                    self.lbl_stat.set_markup("<span size=\"x-large\"><b>Caching lockscreen images for a faster locking next time</b></span>")  # noqa
                    t = threading.Thread(target=fn.cache_bl,
                                         args=(self, GLib, Gtk,))
                    t.daemon = True
                    t.start()
                else:
                    self.lbl_stat.set_markup("<span size=\"x-large\"><b>You need to set the wallpaper path in arcologout.conf</b></span>")  # noqa
                    self.Ec.set_sensitive(True)
                    self.active = False
            else:
                fn.os.unlink("/tmp/arcologout.lock")
                self.__exec_cmd(self.cmd_lock)
                Gtk.main_quit()
        elif (data == self.binds.get('settings')):
            self.themes.grab_focus()
            self.popover.set_relative_to(self.Eset)
            self.popover.show_all()
            self.popover.popup()
        else:
            fn.os.unlink("/tmp/arcologout.lock")
            Gtk.main_quit()

    def __exec_cmd(self, cmdline):
        fn.os.system(cmdline)

    def on_close(self, widget, data):
        fn.os.unlink("/tmp/arcologout.lock")
        Gtk.main_quit()


if __name__ == "__main__":
    if not fn.os.path.isfile("/tmp/arcologout.lock"):
        with open("/tmp/arcologout.pid", "w") as f:
            f.write(str(fn.os.getpid()))
            f.close()
        w = TransparentWindow()
        w.show_all()
        Gtk.main()
    else:
        print("something")
