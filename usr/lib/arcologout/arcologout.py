# =====================================================
#                  Author Brad Heffernan
# =====================================================

import cairo
import gi
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

        self.fullscreen()
        self.set_app_paintable(True)
        GUI.GUI(self, Gtk, GdkPixbuf, fn.working_dir, fn.os, Gdk)

        if not fn.os.path.isfile("/tmp/arcologout.lock"):
            with open("/tmp/arcologout.lock", "w") as f:
                f.write("")

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
        elif data == "Escape":
            plo = GdkPixbuf.Pixbuf().new_from_file_at_size(
                fn.os.path.join(fn.working_dir, 'cancel_blur.svg'), 64, 64)
            self.imagec.set_from_pixbuf(plo)
        elif data == "H":
            plo = GdkPixbuf.Pixbuf().new_from_file_at_size(
                fn.os.path.join(fn.working_dir, 'hibernate_blur.svg'), 64, 64)
            self.imageh.set_from_pixbuf(plo)
        event.window.set_cursor(Gdk.Cursor(Gdk.CursorType.HAND2))

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
        elif data == "Escape":
            plo = GdkPixbuf.Pixbuf().new_from_file_at_size(
                fn.os.path.join(fn.working_dir, 'cancel.svg'), 64, 64)
            self.imagec.set_from_pixbuf(plo)
        elif data == "H":
            plo = GdkPixbuf.Pixbuf().new_from_file_at_size(
                fn.os.path.join(fn.working_dir, 'hibernate.svg'), 64, 64)
            self.imageh.set_from_pixbuf(plo)

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
        self.shortcut_keys = ["Escape", "S", "R", "U", "L", "K", "H"]

        for key in self.shortcut_keys:
            if event.keyval == Gdk.keyval_to_lower(Gdk.keyval_from_name(key)):
                self.click_button(widget, key)

    def click_button(self, widget, data=None):
        if (data == 'L'):
            command = fn._get_logout()
            fn.os.unlink("/tmp/arcologout.lock")
            self.__exec_cmd(command)
            Gtk.main_quit()

        elif (data == 'R'):
            fn.os.unlink("/tmp/arcologout.lock")
            self.__exec_cmd(self.cmd_restart)
            Gtk.main_quit()

        elif (data == 'S'):
            fn.os.unlink("/tmp/arcologout.lock")
            self.__exec_cmd(self.cmd_shutdown)
            Gtk.main_quit()

        elif (data == 'U'):
            fn.os.unlink("/tmp/arcologout.lock")
            self.__exec_cmd(self.cmd_suspend)
            Gtk.main_quit()

        elif (data == 'H'):
            fn.os.unlink("/tmp/arcologout.lock")
            self.__exec_cmd(self.cmd_hibernate)
            Gtk.main_quit()

        elif (data == 'K'):
            if not fn.os.path.isdir(fn.home + "/.cache/i3lock"):
                self.lbl_stat.set_markup("<span size=\"x-large\"><b>Caching lockscreen images for a faster locking next time</b></span>")  # noqa
                t = threading.Thread(target=fn.cache_bl,
                                     args=(self, GLib, Gtk,))
                t.daemon = True
                t.start()
            else:
                fn.os.unlink("/tmp/arcologout.lock")
                self.__exec_cmd(self.cmd_lock)
                Gtk.main_quit()
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
