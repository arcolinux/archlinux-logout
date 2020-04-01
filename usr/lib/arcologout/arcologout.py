# =====================================================
#                  Author Brad Heffernan
# =====================================================

import cairo
import gi
import GUI
import Functions as fn

gi.require_version('Gtk', '3.0')
gi.require_version('Gdk', '3.0')

from gi.repository import Gtk, GdkPixbuf
from gi.repository import Gdk, Gdk


class TransparentWindow(Gtk.Window):
    cmd_shutdown = "systemctl poweroff"
    cmd_restart = "systemctl reboot"
    cmd_suspend = "systemctl suspend"
    cmd_lock = "betterlockscreen -l dimblur"

    def __init__(self):
        Gtk.Window.__init__(self)

        self.set_size_request(300, 220)

        self.connect('destroy', Gtk.main_quit)
        self.connect('draw', self.draw)
        self.connect("key-press-event", self.on_keypress)
        self.connect("window-state-event", self.on_window_state_event)
        self.set_decorated(False)
        self.set_position(Gtk.WindowPosition.CENTER)

        screen = self.get_screen()
        visual = screen.get_rgba_visual()
        if visual and screen.is_composited():
            self.set_visual(visual)
        
        fn.get_config(self, Gdk, fn.config)

        self.fullscreen()
        self.set_app_paintable(True)
        GUI.GUI(self, Gtk, GdkPixbuf, fn.working_dir, fn.os, Gdk)
        self.show_all()

    def on_mouse_in(self, widget, event, data):
        if data == "S":
            psh = GdkPixbuf.Pixbuf().new_from_file_at_size(
                fn.os.path.join(fn.working_dir, 'shutdown_blur.svg'), 64, 64)
            self.imagesh.set_from_pixbuf(psh)
        elif data == "R":
            pr = GdkPixbuf.Pixbuf().new_from_file_at_size(
                fn.os.path.join(fn.working_dir, 'restart_blur.svg'), 64, 64)
            self.imager.set_from_pixbuf(pr)
        elif data == "U":
            ps = GdkPixbuf.Pixbuf().new_from_file_at_size(
                fn.os.path.join(fn.working_dir, 'suspend_blur.svg'), 64, 64)
            self.images.set_from_pixbuf(ps)
        elif data == "K":
            plk = GdkPixbuf.Pixbuf().new_from_file_at_size(
                fn.os.path.join(fn.working_dir, 'lock_blur.svg'), 64, 64)
            self.imagelk.set_from_pixbuf(plk)
        elif data == "L":
            plo = GdkPixbuf.Pixbuf().new_from_file_at_size(
                fn.os.path.join(fn.working_dir, 'logout_blur.svg'), 64, 64)
            self.imagelo.set_from_pixbuf(plo)

    def on_mouse_out(self, widget, event, data):
        if data == "S":
            psh = GdkPixbuf.Pixbuf().new_from_file_at_size(
                fn.os.path.join(fn.working_dir, 'shutdown.svg'), 64, 64)
            self.imagesh.set_from_pixbuf(psh)
        elif data == "R":
            pr = GdkPixbuf.Pixbuf().new_from_file_at_size(
                fn.os.path.join(fn.working_dir, 'restart.svg'), 64, 64)
            self.imager.set_from_pixbuf(pr)
        elif data == "U":
            ps = GdkPixbuf.Pixbuf().new_from_file_at_size(
                fn.os.path.join(fn.working_dir, 'suspend.svg'), 64, 64)
            self.images.set_from_pixbuf(ps)
        elif data == "K":
            plk = GdkPixbuf.Pixbuf().new_from_file_at_size(
                fn.os.path.join(fn.working_dir, 'lock.svg'), 64, 64)
            self.imagelk.set_from_pixbuf(plk)
        elif data == "L":
            plo = GdkPixbuf.Pixbuf().new_from_file_at_size(
                fn.os.path.join(fn.working_dir, 'logout.svg'), 64, 64)
            self.imagelo.set_from_pixbuf(plo)

    def on_click(self, widget, event, data):
        self.click_button(widget, data)

    def on_window_state_event(self, widget, ev):
        self.__is_fullscreen = bool(ev.new_window_state & Gdk.WindowState.FULLSCREEN)

    def draw(self, widget, context):
        context.set_source_rgba(self.r, self.g, self.b, self.opacity)
        context.set_operator(cairo.OPERATOR_SOURCE)
        context.paint()
        context.set_operator(cairo.OPERATOR_OVER)

    def on_keypress(self, widget=None, event=None, data=None):
        self.shortcut_keys = ["Escape", "S", "R", "U", "L", "K", "H"]

        for key in self.shortcut_keys:
            if event.keyval == Gdk.keyval_to_lower(Gdk.keyval_from_name(key)):
                self.click_button(widget, key)

    def click_button(self, widget, data=None):
        if (data == 'L'):
            command = fn._get_logout()
            self.__exec_cmd(command)            

        elif (data == 'R'):
            self.__exec_cmd(self.cmd_restart)

        elif (data == 'S'):
            self.__exec_cmd(self.cmd_shutdown)

        elif (data == 'U'):
            self.__exec_cmd(self.cmd_suspend)

        elif (data == 'H'):
            self.__exec_cmd(self.cmd_hibernate)

        elif (data == 'K'):
            self.__exec_cmd(self.cmd_lock)

        Gtk.main_quit()

    def __exec_cmd(self, cmdline):
        fn.os.system(cmdline)


TransparentWindow()
Gtk.main()
