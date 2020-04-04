
# =====================================================
#                  Author Brad Heffernan
# =====================================================

import subprocess
import os
from pathlib import Path
import configparser

home = os.path.expanduser("~")
base_dir = os.path.dirname(os.path.realpath(__file__))
# here = Path(__file__).resolve()
working_dir = ''.join([str(Path(__file__).parents[2]), "/share/arcologout/"])
# config = "/etc/arcologout.conf"
config = ''.join([str(Path(__file__).parents[3]), "/etc/arcologout.conf"])


def cache_bl(self, GLib, Gtk):
    if os.path.isfile("/usr/bin/betterlockscreen"):
        with subprocess.Popen(["betterlockscreen", "-u",
                               self.wallpaper],
                              shell=False,
                              stdout=subprocess.PIPE) as f:
            for line in f.stdout:
                GLib.idle_add(self.lbl_stat.set_markup, "<span size=\"x-large\"><b>" + line.decode() + "</b></span>")

        GLib.idle_add(self.lbl_stat.set_text, "")
        os.unlink("/tmp/arcologout.lock")
        os.system(self.cmd_lock)
        Gtk.main_quit()
    else:
        print("not installed betterlockscreen.")


def get_config(self, Gdk, config):
    self.parser = configparser.SafeConfigParser()
    self.parser.read(config)

    # Set some safe defaults
    self.opacity = 0.6

    # Check if we're using HAL, and init it as required.
    if self.parser.has_section("settings"):
        if self.parser.has_option("settings", "opacity"):
            self.opacity = int(self.parser.get("settings", "opacity"))/100
        if self.parser.has_option("settings", "lock_wallpaper"):
            self.wallpaper = self.parser.get("settings", "lock_wallpaper")
        if self.parser.has_option("settings", "buttons"):
            self.buttons = self.parser.get("settings", "buttons").split(",")

    if self.parser.has_section("commands"):
        if self.parser.has_option("commands", "lock"):
            self.cmd_lock = self.parser.get("commands", "lock")

    if self.parser.has_section("themes"):
        if self.parser.has_option("themes", "theme"):
            self.theme = self.parser.get("themes", "theme")


def _get_logout():
    out = subprocess.run(["sh", "-c", "env | grep DESKTOP_SESSION"],
                         shell=False, stdout=subprocess.PIPE)
    desktop = out.stdout.decode().split("=")[1].strip()

    if desktop in ("herbstluftwm", "/usr/share/xsessions/herbstluftwm"):
        return "herbstclient quit"
    elif desktop in ("bspwm", "/usr/share/xsessions/bspwm"):
        return "pkill bspwm"
    elif desktop in ("jwm", "/usr/share/xsessions/jwm"):
        return "pkill jwm"
    elif desktop in ("openbox", "/usr/share/xsessions/openbox"):
        return "pkill openbox"
    elif desktop in ("awesome", "/usr/share/xsessions/awesome"):
        return "pkill awesome"
    elif desktop in ("qtile", "/usr/share/xsessions/qtile"):
        return "pkill qtile"
    elif desktop in ("xmonad", "/usr/share/xsessions/xmonad"):
        return "pkill xmonad"
    elif desktop in ("dwm", "/usr/share/xsessions/dwm"):
        return "pkill dwm"
    elif desktop in ("i3", "/usr/share/xsessions/i3"):
        return "pkill i3"
    elif desktop in ("spectrwm", "/usr/share/xsessions/spectrwm"):
        return "pkill spectrwm"
    # elif desktop in ("xfce", "/usr/share/xsessions/xfce"):
    #     return "xfce4-session-logout --logout"

    return None


def button_active(self, data, GdkPixbuf):
    if data == "S":
        psh = GdkPixbuf.Pixbuf().new_from_file_at_size(
            os.path.join(working_dir, 'themes/' + self.theme + '/shutdown_blur.svg'), 64, 64)
        self.imagesh.set_from_pixbuf(psh)
        self.lbl1.set_markup("<span foreground=\"white\">Shutdown</span>")
    elif data == "R":
        pr = GdkPixbuf.Pixbuf().new_from_file_at_size(
            os.path.join(working_dir, 'themes/' + self.theme + '/restart_blur.svg'), 64, 64)
        self.imager.set_from_pixbuf(pr)
        self.lbl2.set_markup("<span foreground=\"white\">Restart</span>")
    elif data == "U":
        ps = GdkPixbuf.Pixbuf().new_from_file_at_size(
            os.path.join(working_dir, 'themes/' + self.theme + '/suspend_blur.svg'), 64, 64)
        self.images.set_from_pixbuf(ps)
        self.lbl3.set_markup("<span foreground=\"white\">Suspend</span>")
    elif data == "K":
        plk = GdkPixbuf.Pixbuf().new_from_file_at_size(
            os.path.join(working_dir, 'themes/' + self.theme + '/lock_blur.svg'), 64, 64)
        self.imagelk.set_from_pixbuf(plk)
        self.lbl4.set_markup("<span foreground=\"white\">Lock</span>")
    elif data == "L":
        plo = GdkPixbuf.Pixbuf().new_from_file_at_size(
            os.path.join(working_dir, 'themes/' + self.theme + '/logout_blur.svg'), 64, 64)
        self.imagelo.set_from_pixbuf(plo)
        self.lbl5.set_markup("<span foreground=\"white\">Logout</span>")
    elif data == "Escape":
        plo = GdkPixbuf.Pixbuf().new_from_file_at_size(
            os.path.join(working_dir, 'themes/' + self.theme + '/cancel_blur.svg'), 64, 64)
        self.imagec.set_from_pixbuf(plo)
        self.lbl6.set_markup("<span foreground=\"white\">Cancel</span>")
    elif data == "H":
        plo = GdkPixbuf.Pixbuf().new_from_file_at_size(
            os.path.join(working_dir, 'themes/' + self.theme + '/hibernate_blur.svg'), 64, 64)
        self.imageh.set_from_pixbuf(plo)
        self.lbl7.set_markup("<span foreground=\"white\">Hibernate</span>")

def button_toggled(self, data):
    self.Esh.set_sensitive(False)
    self.Er.set_sensitive(False)
    self.Es.set_sensitive(False)
    self.Elk.set_sensitive(False)
    self.El.set_sensitive(False)
    self.Ec.set_sensitive(False)
    self.Eh.set_sensitive(False)

    if data == "S":
        self.Esh.set_sensitive(True)
    elif data == "R":
        self.Er.set_sensitive(True)
    elif data == "U":
        self.Es.set_sensitive(True)
    elif data == "K":
        self.Elk.set_sensitive(True)
    elif data == "L":
        self.El.set_sensitive(True)
    elif data == "Escape":
        self.Ec.set_sensitive(True)
    elif data == "H":
        self.Eh.set_sensitive(True)


def file_check(file):
    if os.path.isfile(file):
        return True
