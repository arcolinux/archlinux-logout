
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
config = "/etc/arcologout.conf"
# config = ''.join([str(Path(__file__).parents[3]), "/etc/arcologout.conf"])


def cache_bl(self, GLib, Gtk):
    if os.path.isfile("/usr/bin/betterlockscreen"):
        subprocess.run(["betterlockscreen", "-u",
                        working_dir + "wallpaper.jpg"],
                       shell=False)
        GLib.idle_add(self.lbl_stat.set_text, "")
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

    if self.parser.has_section("commands"):
        if self.parser.has_option("commands", "lock"):
            self.cmd_lock = self.parser.get("commands", "lock")


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
    # elif desktop in ("xfce", "/usr/share/xsessions/xfce"):
    #     return "xfce4-session-logout --logout"

    return None


def file_check(file):
    if os.path.isfile(file):
        return True
