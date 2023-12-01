# =====================================================
#        Authors Brad Heffernan, Fennec and Erik Dubois
# =====================================================

import cairo
import gi
import shutil
import GUI
import Functions as fn
import threading
import signal
import os
from distro import id

gi.require_version("Gtk", "3.0")
gi.require_version("Gdk", "3.0")
gi.require_version("Wnck", "3.0")

from gi.repository import Gtk, GdkPixbuf, Gdk, Wnck, GLib, GdkX11  # noqa


class TransparentWindow(Gtk.Window):
    distr = id()

    cmd_shutdown = "systemctl poweroff"
    cmd_restart = "systemctl reboot"
    cmd_suspend = "systemctl suspend"
    cmd_hibernate = "systemctl hibernate"

    if distr == "artix":
        if os.path.isfile("/usr/bin/loginctl"):
            cmd_shutdown = "loginctl poweroff"
            cmd_restart = "loginctl reboot"
            cmd_suspend = "loginctl suspend"
            cmd_hibernate = "loginctl hibernate"

    cmd_lock = 'betterlockscreen -l dim -- --time-str="%H:%M"'
    wallpaper = "/usr/share/archlinux-betterlockscreen/wallpapers/wallpaper.jpg"
    d_buttons = [
        "cancel",
        "shutdown",
        "restart",
        "suspend",
        "hibernate",
        "lock",
        "logout",
    ]
    binds = {
        "lock": "K",
        "restart": "R",
        "shutdown": "S",
        "suspend": "U",
        "hibernate": "H",
        "logout": "L",
        "cancel": "Escape",
        "settings": "P",
    }
    theme = "white"
    hover = "#ffffff"
    icon = 64
    font = 11
    buttons = None
    active = False
    opacity = 0.8

    def __init__(self):
        super(TransparentWindow, self).__init__(
            type=Gtk.WindowType.TOPLEVEL, title="ArchLinux Logout"
        )
        # Gtk.Window.__init__(self, type=Gtk.WindowType.TOPLEVEL)
        # self.set_type_hint(Gdk.WindowTypeHint.DOCK)
        self.set_keep_above(True)
        self.set_position(Gtk.WindowPosition.CENTER_ALWAYS)
        # self.set_size_request(1200, 300)
        self.connect("delete-event", self.on_close)
        self.connect("destroy", self.on_close)
        self.connect("draw", self.draw)
        self.connect("key-press-event", self.on_keypress)
        self.connect("window-state-event", self.on_window_state_event)
        self.set_decorated(False)

        if not fn.os.path.isdir(fn.home + "/.config/archlinux-logout"):
            fn.os.mkdir(fn.home + "/.config/archlinux-logout")

        if not fn.os.path.isfile(
            fn.home + "/.config/archlinux-logout/archlinux-logout.conf"
        ):
            shutil.copy(
                fn.root_config,
                fn.home + "/.config/archlinux-logout/archlinux-logout.conf",
            )

        self.width = 0
        self.screen = self.get_screen()

        self.display = Gdk.Display.get_default()

        seat = self.display.get_default_seat()

        self.pointer = Gdk.Seat.get_pointer(seat)

        visual = self.screen.get_rgba_visual()
        if visual and self.screen.is_composited():
            self.set_visual(visual)

        fn.get_config(self, Gdk, Gtk, fn.config)

        self.display_on_monitor()

        if self.buttons is None or self.buttons == [""]:
            self.buttons = self.d_buttons

        self.set_app_paintable(True)
        self.present()

        GUI.GUI(self, Gtk, GdkPixbuf, fn.working_dir, fn.os, Gdk, fn)
        if not fn.os.path.isfile("/tmp/archlinux-logout.lock"):
            with open("/tmp/archlinux-logout.lock", "w") as f:
                f.write("")

    def display_on_monitor(self):
        print("#### Archlinux Logout ####")
        try:
            # test to see this device is a mouse
            if self.pointer.get_has_cursor():
                screen = None
                x = 0
                y = 0
                display = None

                session_type = os.environ.get("XDG_SESSION_TYPE")

                if session_type == "wayland":
                    print(
                        "[WARN]: Session type = wayland, mouse position can't be tracked"
                    )
                elif session_type == "x11":
                    print("[DEBUG]: Session type = x11")

                # get the screen, x, y coordinates
                screen, x, y = self.pointer.get_position()

                # X11 compatibility only
                # Wayland does not allow you to get the x,y coordinates
                # defaults to showing on first monitor

                if screen is not None and x != 0 and y != 0:
                    print(f"[DEBUG]: Mouse position x={x} y={y}")

                    # Returns the GdkDisplay to which device is connected
                    display = self.pointer.get_display()

                    if display is not None:
                        # use the mouse cursor x,y coordinates
                        monitor = display.get_monitor_at_point(x, y)
                        print(
                            f"[DEBUG]: Monitor: Primary={monitor.is_primary()}, Height={monitor.get_height_mm()}, Width={monitor.get_width_mm()}"
                        )
                        geometry = monitor.get_geometry()
                        print(
                            f"[DEBUG]: Monitor: Dimension={geometry.width}x{geometry.height}"
                        )
                        self.set_size_request(geometry.width, geometry.height)
                        # move the window using the mouse pointer x,y coordinates
                        self.move(x, y)
                        self.fullscreen()
                else:
                    # default show on first monitor
                    self.display_on_default()

            else:
                # default show on first monitor
                self.display_on_default()
        except Exception as e:
            print(f"[ERROR]: Exception in display_on_monitor(): {e}")

    # fallback should only be used if the mouse position can't be captured such as when on wayland
    def display_on_default(self):
        # default show on first monitor
        monitor = self.display.get_monitor(0)
        geometry = monitor.get_geometry()
        print("[DEBUG]: Showing on first monitor")
        print(f"[DEBUG]: Dimension: {geometry.width}x{geometry.height}")
        self.set_size_request(geometry.width, geometry.height)
        self.fullscreen_on_monitor(self.screen, 0)

    def on_save_clicked(self, widget):
        try:
            with open(
                fn.home + "/.config/archlinux-logout/archlinux-logout.conf", "r"
            ) as f:
                lines = f.readlines()
                f.close()

            pos_opacity = fn._get_position(lines, "opacity")
            pos_size = fn._get_position(lines, "icon_size")
            pos_theme = fn._get_position(lines, "theme=")
            pos_font = fn._get_position(lines, "font_size=")

            lines[pos_opacity] = "opacity=" + str(int(self.hscale.get_value())) + "\n"
            lines[pos_size] = "icon_size=" + str(int(self.icons.get_value())) + "\n"
            lines[pos_theme] = "theme=" + self.themes.get_active_text() + "\n"
            lines[pos_font] = "font_size=" + str(int(self.fonts.get_value())) + "\n"

            with open(
                fn.home + "/.config/archlinux-logout/archlinux-logout.conf", "w"
            ) as f:
                f.writelines(lines)
                f.close()
            self.popover.popdown()
        except Exception as e:
            fn.os.unlink(fn.home + "/.config/archlinux-logout/archlinux-logout.conf")
            if not fn.os.path.isfile(
                fn.home + "/.config/archlinux-logout/archlinux-logout.conf"
            ):
                shutil.copy(
                    fn.root_config,
                    fn.home + "/.config/archlinux-logout/archlinux-logout.conf",
                )
            with open(
                fn.home + "/.config/archlinux-logout/archlinux-logout.conf", "r"
            ) as f:
                lines = f.readlines()
                f.close()

            pos_opacity = fn._get_position(lines, "opacity")
            pos_size = fn._get_position(lines, "icon_size")
            pos_theme = fn._get_position(lines, "theme=")
            pos_font = fn._get_position(lines, "font_size=")

            lines[pos_opacity] = "opacity=" + str(int(self.hscale.get_value())) + "\n"
            lines[pos_size] = "icon_size=" + str(int(self.icons.get_value())) + "\n"
            lines[pos_theme] = "theme=" + self.themes.get_active_text() + "\n"
            lines[pos_font] = "font_size=" + str(int(self.fonts.get_value())) + "\n"

            with open(
                fn.home + "/.config/archlinux-logout/archlinux-logout.conf", "w"
            ) as f:
                f.writelines(lines)
                f.close()
            self.popover.popdown()

    def on_mouse_in(self, widget, event, data):
        if data == self.binds.get("shutdown"):
            psh = GdkPixbuf.Pixbuf().new_from_file_at_size(
                fn.os.path.join(
                    fn.working_dir, "themes/" + self.theme + "/shutdown_blur.svg"
                ),
                self.icon,
                self.icon,
            )
            self.imagesh.set_from_pixbuf(psh)
            self.lbl1.set_markup(
                '<span size="'
                + str(self.font)
                + '000" foreground="'
                + self.hover
                + '">Shutdown (S)</span>'
            )
        elif data == self.binds.get("restart"):
            pr = GdkPixbuf.Pixbuf().new_from_file_at_size(
                fn.os.path.join(
                    fn.working_dir, "themes/" + self.theme + "/restart_blur.svg"
                ),
                self.icon,
                self.icon,
            )
            self.imager.set_from_pixbuf(pr)
            self.lbl2.set_markup(
                '<span size="'
                + str(self.font)
                + '000" foreground="'
                + self.hover
                + '">Reboot (R)</span>'
            )
        elif data == self.binds.get("suspend"):
            ps = GdkPixbuf.Pixbuf().new_from_file_at_size(
                fn.os.path.join(
                    fn.working_dir, "themes/" + self.theme + "/suspend_blur.svg"
                ),
                self.icon,
                self.icon,
            )
            self.images.set_from_pixbuf(ps)
            self.lbl3.set_markup(
                '<span size="'
                + str(self.font)
                + '000" foreground="'
                + self.hover
                + '">Suspend (U)</span>'
            )
        elif data == self.binds.get("lock"):
            plk = GdkPixbuf.Pixbuf().new_from_file_at_size(
                fn.os.path.join(
                    fn.working_dir, "themes/" + self.theme + "/lock_blur.svg"
                ),
                self.icon,
                self.icon,
            )
            self.imagelk.set_from_pixbuf(plk)
            self.lbl4.set_markup(
                '<span size="'
                + str(self.font)
                + '000" foreground="'
                + self.hover
                + '">Lock (K)</span>'
            )
        elif data == self.binds.get("logout"):
            plo = GdkPixbuf.Pixbuf().new_from_file_at_size(
                fn.os.path.join(
                    fn.working_dir, "themes/" + self.theme + "/logout_blur.svg"
                ),
                self.icon,
                self.icon,
            )
            self.imagelo.set_from_pixbuf(plo)
            self.lbl5.set_markup(
                '<span size="'
                + str(self.font)
                + '000" foreground="'
                + self.hover
                + '">Logout (L)</span>'
            )
        elif data == self.binds.get("cancel"):
            plo = GdkPixbuf.Pixbuf().new_from_file_at_size(
                fn.os.path.join(
                    fn.working_dir, "themes/" + self.theme + "/cancel_blur.svg"
                ),
                self.icon,
                self.icon,
            )
            self.imagec.set_from_pixbuf(plo)
            self.lbl6.set_markup(
                '<span size="'
                + str(self.font)
                + '000" foreground="'
                + self.hover
                + '">Cancel (ESC)</span>'
            )
        elif data == self.binds.get("hibernate"):
            plo = GdkPixbuf.Pixbuf().new_from_file_at_size(
                fn.os.path.join(
                    fn.working_dir, "themes/" + self.theme + "/hibernate_blur.svg"
                ),
                self.icon,
                self.icon,
            )
            self.imageh.set_from_pixbuf(plo)
            self.lbl7.set_markup(
                '<span size="'
                + str(self.font)
                + '000" foreground="'
                + self.hover
                + '">Hibernate (H)</span>'
            )
        elif data == self.binds.get("settings"):
            pset = GdkPixbuf.Pixbuf().new_from_file_at_size(
                fn.os.path.join(fn.working_dir, "configure_blur.svg"), 48, 48
            )
            self.imageset.set_from_pixbuf(pset)
        elif data == "light":
            pset = GdkPixbuf.Pixbuf().new_from_file_at_size(
                fn.os.path.join(fn.working_dir, "light_blur.svg"), 48, 48
            )
            self.imagelig.set_from_pixbuf(pset)
        event.window.set_cursor(Gdk.Cursor(Gdk.CursorType.HAND2))

    def on_mouse_out(self, widget, event, data):
        if not self.active:
            if data == self.binds.get("shutdown"):
                psh = GdkPixbuf.Pixbuf().new_from_file_at_size(
                    fn.os.path.join(
                        fn.working_dir, "themes/" + self.theme + "/shutdown.svg"
                    ),
                    self.icon,
                    self.icon,
                )
                self.imagesh.set_from_pixbuf(psh)
                self.lbl1.set_markup(
                    '<span size="' + str(self.font) + '000">Shutdown (S)</span>'
                )
            elif data == self.binds.get("restart"):
                pr = GdkPixbuf.Pixbuf().new_from_file_at_size(
                    fn.os.path.join(
                        fn.working_dir, "themes/" + self.theme + "/restart.svg"
                    ),
                    self.icon,
                    self.icon,
                )
                self.imager.set_from_pixbuf(pr)
                self.lbl2.set_markup(
                    '<span size="' + str(self.font) + '000">Reboot (R)</span>'
                )
            elif data == self.binds.get("suspend"):
                ps = GdkPixbuf.Pixbuf().new_from_file_at_size(
                    fn.os.path.join(
                        fn.working_dir, "themes/" + self.theme + "/suspend.svg"
                    ),
                    self.icon,
                    self.icon,
                )
                self.images.set_from_pixbuf(ps)
                self.lbl3.set_markup(
                    '<span size="' + str(self.font) + '000">Suspend (U)</span>'
                )
            elif data == self.binds.get("lock"):
                plk = GdkPixbuf.Pixbuf().new_from_file_at_size(
                    fn.os.path.join(
                        fn.working_dir, "themes/" + self.theme + "/lock.svg"
                    ),
                    self.icon,
                    self.icon,
                )
                self.imagelk.set_from_pixbuf(plk)
                self.lbl4.set_markup(
                    '<span size="' + str(self.font) + '000">Lock (K)</span>'
                )
            elif data == self.binds.get("logout"):
                plo = GdkPixbuf.Pixbuf().new_from_file_at_size(
                    fn.os.path.join(
                        fn.working_dir, "themes/" + self.theme + "/logout.svg"
                    ),
                    self.icon,
                    self.icon,
                )
                self.imagelo.set_from_pixbuf(plo)
                self.lbl5.set_markup(
                    '<span size="' + str(self.font) + '000">Logout (L)</span>'
                )
            elif data == self.binds.get("cancel"):
                plo = GdkPixbuf.Pixbuf().new_from_file_at_size(
                    fn.os.path.join(
                        fn.working_dir, "themes/" + self.theme + "/cancel.svg"
                    ),
                    self.icon,
                    self.icon,
                )
                self.imagec.set_from_pixbuf(plo)
                self.lbl6.set_markup(
                    '<span size="' + str(self.font) + '000">Cancel (ESC)</span>'
                )
            elif data == self.binds.get("hibernate"):
                plo = GdkPixbuf.Pixbuf().new_from_file_at_size(
                    fn.os.path.join(
                        fn.working_dir, "themes/" + self.theme + "/hibernate.svg"
                    ),
                    self.icon,
                    self.icon,
                )
                self.imageh.set_from_pixbuf(plo)
                self.lbl7.set_markup(
                    '<span size="' + str(self.font) + '000">Hibernate (H)</span>'
                )
            elif data == self.binds.get("settings"):
                pset = GdkPixbuf.Pixbuf().new_from_file_at_size(
                    fn.os.path.join(fn.working_dir, "configure.svg"), 48, 48
                )
                self.imageset.set_from_pixbuf(pset)
            elif data == "light":
                pset = GdkPixbuf.Pixbuf().new_from_file_at_size(
                    fn.os.path.join(fn.working_dir, "light.svg"), 48, 48
                )
                self.imagelig.set_from_pixbuf(pset)

    def on_click(self, widget, event, data):
        self.click_button(widget, data)

    def on_window_state_event(self, widget, ev):
        self.__is_fullscreen = bool(
            ev.new_window_state & Gdk.WindowState.FULLSCREEN
        )  # noqa

    def draw(self, widget, context):
        context.set_source_rgba(0, 0, 0, self.opacity)
        context.set_operator(cairo.OPERATOR_SOURCE)
        context.paint()
        context.set_operator(cairo.OPERATOR_OVER)

    def on_keypress(self, widget=None, event=None, data=None):
        self.shortcut_keys = [
            self.binds.get("cancel"),
            self.binds.get("shutdown"),
            self.binds.get("restart"),
            self.binds.get("suspend"),
            self.binds.get("logout"),
            self.binds.get("lock"),
            self.binds.get("hibernate"),
            self.binds.get("settings"),
        ]

        for key in self.shortcut_keys:
            if event.keyval == Gdk.keyval_to_lower(Gdk.keyval_from_name(key)):
                self.click_button(widget, key)

    def click_button(self, widget, data=None):
        if not data == self.binds.get("settings") and not data == "light":
            self.active = True
            fn.button_toggled(self, data)
            fn.button_active(self, data, GdkPixbuf)

        if data == self.binds.get("logout"):
            command = fn._get_logout()
            fn.os.unlink("/tmp/archlinux-logout.lock")
            fn.os.unlink("/tmp/archlinux-logout.pid")
            self.__exec_cmd(command)
            Gtk.main_quit()

        elif data == self.binds.get("restart"):
            fn.os.unlink("/tmp/archlinux-logout.lock")
            fn.os.unlink("/tmp/archlinux-logout.pid")
            self.__exec_cmd(self.cmd_restart)
            Gtk.main_quit()

        elif data == self.binds.get("shutdown"):
            fn.os.unlink("/tmp/archlinux-logout.lock")
            fn.os.unlink("/tmp/archlinux-logout.pid")
            self.__exec_cmd(self.cmd_shutdown)
            Gtk.main_quit()

        elif data == self.binds.get("suspend"):
            fn.os.unlink("/tmp/archlinux-logout.lock")
            fn.os.unlink("/tmp/archlinux-logout.pid")
            self.__exec_cmd(self.cmd_suspend)
            Gtk.main_quit()

        elif data == self.binds.get("hibernate"):
            fn.os.unlink("/tmp/archlinux-logout.lock")
            fn.os.unlink("/tmp/archlinux-logout.pid")
            self.__exec_cmd(self.cmd_hibernate)
            Gtk.main_quit()

        elif data == self.binds.get("lock"):
            if self.cmd_lock.startswith("betterlockscreen") and not fn.os.path.isdir(
                fn.home + "/.cache/betterlockscreen"
            ):
                if fn.os.path.isfile(self.wallpaper):
                    self.lbl_stat.set_markup(
                        '<span size="x-large"><b>Caching lockscreen images for a faster locking next time</b></span>'
                    )  # noqa
                    t = threading.Thread(
                        target=fn.cache_bl,
                        args=(
                            self,
                            GLib,
                            Gtk,
                        ),
                    )
                    t.daemon = True
                    t.start()
                else:
                    self.lbl_stat.set_markup(
                        '<span size="x-large"><b>Choose a wallpaper with archlinux-betterlockscreen</b></span>'
                    )  # noqa
                    self.Ec.set_sensitive(True)
                    self.active = False
            else:
                fn.os.unlink("/tmp/archlinux-logout.lock")
                self.__exec_cmd(self.cmd_lock)
                Gtk.main_quit()
        elif data == self.binds.get("settings"):
            self.themes.grab_focus()
            self.popover.set_relative_to(self.Eset)
            self.popover.show_all()
            self.popover.popup()
        elif data == "light":
            self.popover2.set_relative_to(self.Elig)
            self.popover2.show_all()
            self.popover2.popup()
        else:
            fn.os.unlink("/tmp/archlinux-logout.lock")
            fn.os.unlink("/tmp/archlinux-logout.pid")
            Gtk.main_quit()

    def __exec_cmd(self, cmdline):
        fn.os.system(cmdline)

    def on_close(self, widget, data):
        fn.os.unlink("/tmp/archlinux-logout.lock")
        fn.os.unlink("/tmp/archlinux-logout.pid")
        Gtk.main_quit()

    def message_box(self, message, title):
        md = Gtk.MessageDialog(
            parent=self,
            message_type=Gtk.MessageType.INFO,
            buttons=Gtk.ButtonsType.YES_NO,
            text=title,
        )
        md.format_secondary_markup(message)  # noqa

        result = md.run()
        md.destroy()

        if result in (Gtk.ResponseType.OK, Gtk.ResponseType.YES):
            return True
        else:
            return False


def signal_handler(sig, frame):
    print("\nArchLinux-Logout is Closing.")
    fn.os.unlink("/tmp/archlinux-logout.lock")
    fn.os.unlink("/tmp/archlinux-logout.pid")
    Gtk.main_quit(0)


if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)
    if not fn.os.path.isfile("/tmp/archlinux-logout.lock"):
        with open("/tmp/archlinux-logout.pid", "w") as f:
            f.write(str(fn.os.getpid()))
            f.close()
        w = TransparentWindow()
        w.show_all()
        Gtk.main()
    else:
        print(
            "ArchLinux-logout did not close properly. Remove /tmp/archlinux-logout.lock with sudo."
        )
