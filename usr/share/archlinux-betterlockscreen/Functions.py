# =================================================================
# =                  Author: Brad Heffernan                       =
# =================================================================
import os
import subprocess
import threading
import psutil
import gi
from os.path import expanduser
gi.require_version('Gtk', '3.0')
from gi.repository import GLib, Gtk  # noqa


home = expanduser("~")
base_dir = os.path.dirname(os.path.realpath(__file__))
config = home + "/.config/archlinux-betterlockscreen/"
settings = "settings.conf"
resolutions = [
    "640x360",
    "800x600",
    "1024x768",
    "1280x720",
    "1280x800",
    "1280x1024",
    "1360x768",
    "1366x768",
    "1440x900",
    "1536x864",
    "1600x900",
    "1680x1050",
    "1920x1080",
    "1920x1200",
    "2048x1152",
    "2560x1080",
    "2560x1440",
    "3440x1440",
    "3840x2160"
]
# ================================================
#                   GLOBALS
# ================================================

# ================================================
#               NOTIFICATIONS
# ================================================


def _get_position(lists, string):
    nlist = [x for x in lists if string in x]
    position = lists.index(nlist[0])
    return position


def get_saved_path():
    with open(config + settings, "r") as f:
        lines = f.readlines()
        f.close()
    pos = _get_position(lines, "path=")

    return lines[pos].split("=")[1].strip()


def show_in_app_notification(self, message):
    if self.timeout_id is not None:
        GLib.source_remove(self.timeout_id)
        self.timeout_id = None

    self.notification_label.set_markup("<span foreground=\"white\">" +
                                       message + "</span>")
    self.notification_revealer.set_reveal_child(True)
    self.timeout_id = GLib.timeout_add(3000, timeOut, self)


def timeOut(self):
    close_in_app_notification(self)


def close_in_app_notification(self):
    self.notification_revealer.set_reveal_child(False)
    GLib.source_remove(self.timeout_id)
    self.timeout_id = None


def MessageBox(self, title, message):
    md2 = Gtk.MessageDialog(parent=self,
                            flags=0,
                            message_type=Gtk.MessageType.INFO,
                            buttons=Gtk.ButtonsType.OK,
                            text=title)
    md2.format_secondary_markup(message)
    md2.run()
    md2.destroy()


def checkIfProcessRunning(processName):
    for proc in psutil.process_iter():
        try:
            pinfo = proc.as_dict(attrs=['pid', 'name', 'create_time'])
            if processName == pinfo['pid']:
                return True
        except (psutil.NoSuchProcess,
                psutil.AccessDenied,
                psutil.ZombieProcess):
            pass
    return False