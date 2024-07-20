# =====================================================
#        Authors Brad Heffernan and Erik Dubois
# =====================================================

import subprocess
import os
import shutil
from pathlib import Path
import configparser

# import distro

envvar = os.environ["XDG_SESSION_TYPE"]
sessionw = False
if envvar == "wayland":
    sessionw = True

home = os.path.expanduser("~")

base_dir = os.path.dirname(os.path.realpath(__file__))
# here = Path(__file__).resolve()
working_dir = "".join(
    [str(Path(__file__).parents[2]), "/share/archlinux-logout-themes/"]
)
# config = "/etc/archlinux-logout.conf"
if os.path.isfile(home + "/.config/archlinux-logout/archlinux-logout.conf"):
    config = home + "/.config/archlinux-logout/archlinux-logout.conf"
else:
    config = "".join([str(Path(__file__).parents[3]), "/etc/archlinux-logout.conf"])
root_config = "".join([str(Path(__file__).parents[3]), "/etc/archlinux-logout.conf"])


def _get_position(lists, value):
    data = [string for string in lists if value in string]
    position = lists.index(data[0])
    return position


def _get_themes():
    y = [x for x in os.listdir(working_dir + "themes")]
    y.sort()
    return y


def cache_bl(self, GLib, Gtk):
    if os.path.isfile("/usr/bin/betterlockscreen"):
        with subprocess.Popen(
            ["betterlockscreen", "-u", self.wallpaper],
            shell=False,
            stdout=subprocess.PIPE,
        ) as f:
            for line in f.stdout:
                line = str(line)
                line = line.split(maxsplit=1)[1]
                line = line[:-3]
                GLib.idle_add(
                    self.lbl_stat.set_markup,
                    '<span size="x-large"><b>' + line + "</b></span>",
                )

        GLib.idle_add(self.lbl_stat.set_text, "")
        os.unlink("/tmp/archlinux-logout.lock")
        os.system(self.cmd_lock)
        Gtk.main_quit()
    else:
        print("not installed betterlockscreen.")


def get_config(self, Gdk, Gtk, config):
    try:
        self.parser = configparser.RawConfigParser()
        self.parser.read(config)

        # Set some safe defaults
        self.opacity = 60
        self.show_on_monitor = 0  # always show on first monitor unless set in settings

        # Check if we're using HAL, and init it as required.
        if self.parser.has_section("settings"):
            if self.parser.has_option("settings", "opacity"):
                self.opacity = int(self.parser.get("settings", "opacity")) / 100
            if self.parser.has_option("settings", "buttons"):
                self.buttons = self.parser.get("settings", "buttons").split(",")
            if self.parser.has_option("settings", "icon_size"):
                self.icon = int(self.parser.get("settings", "icon_size"))
            if self.parser.has_option("settings", "font_size"):
                self.font = int(self.parser.get("settings", "font_size"))
            if self.parser.has_option("settings", "show_on_monitor"):
                self.show_on_monitor = self.parser.get("settings", "show_on_monitor")

        if self.parser.has_section("commands"):
            if self.parser.has_option("commands", "lock"):
                self.cmd_lock = str(self.parser.get("commands", "lock"))
            if self.parser.has_option("commands", "shutdown"):
                self.cmd_shutdown = str(self.parser.get("commands", "shutdown"))
            if self.parser.has_option("commands", "restart"):
                self.cmd_restart = str(self.parser.get("commands", "restart"))
            if self.parser.has_option("commands", "suspend"):
                self.cmd_suspend = str(self.parser.get("commands", "suspend"))
            if self.parser.has_option("commands", "hibernate"):
                self.cmd_hibernate = str(self.parser.get("commands", "hibernate"))

        if self.parser.has_section("binds"):
            if self.parser.has_option("binds", "lock"):
                self.binds["lock"] = self.parser.get("binds", "lock").capitalize()
            if self.parser.has_option("binds", "restart"):
                self.binds["restart"] = self.parser.get("binds", "restart").capitalize()
            if self.parser.has_option("binds", "shutdown"):
                self.binds["shutdown"] = self.parser.get(
                    "binds", "shutdown"
                ).capitalize()
            if self.parser.has_option("binds", "suspend"):
                self.binds["suspend"] = self.parser.get("binds", "suspend").capitalize()
            if self.parser.has_option("binds", "hibernate"):
                self.binds["hibernate"] = self.parser.get(
                    "binds", "hibernate"
                ).capitalize()
            if self.parser.has_option("binds", "logout"):
                self.binds["logout"] = self.parser.get("binds", "logout").capitalize()
            if self.parser.has_option("binds", "cancel"):
                self.binds["cancel"] = self.parser.get("binds", "cancel").capitalize()
            if self.parser.has_option("binds", "settings"):
                self.binds["settings"] = self.parser.get(
                    "binds", "settings"
                ).capitalize()

        if self.parser.has_section("themes"):
            if self.parser.has_option("themes", "theme"):
                self.theme = self.parser.get("themes", "theme")
            # if self.parser.has_option("themes", "hover_color"):
            #     self.hover = self.parser.get("themes", "hover_color")

        if len(self.theme) > 1:
            style_provider = Gtk.CssProvider()
            style_provider.load_from_path(
                working_dir + "themes/" + self.theme + "/theme.css"
            )

            Gtk.StyleContext.add_provider_for_screen(
                Gdk.Screen.get_default(),
                style_provider,
                Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION,
            )
    except Exception as e:
        print(e)
        os.unlink(home + "/.config/archlinux-logout/archlinux-logout.conf")
        if not os.path.isfile(home + "/.config/archlinux-logout/archlinux-logout.conf"):
            shutil.copy(
                root_config, home + "/.config/archlinux-logout/archlinux-logout.conf"
            )


def _get_logout():
    desktop = "unknown"
    try:
        out = subprocess.run(
            ["sh", "-c", "env | grep DESKTOP_SESSION"],
            shell=False,
            stdout=subprocess.PIPE,
        )
        desktop = out.stdout.decode().split("=")[1].strip()
        desktop = desktop.lower()
    except Exception as e:
        desktop = "unknown"

    # in case display manager ly is active

    status = os.system("systemctl is-active --quiet ly")
    if status == 0:
        try:
            out = subprocess.run(
                ["sh", "-c", "env | grep XDG_CURRENT_DESKTOP"],
                shell=False,
                stdout=subprocess.PIPE,
            )
            desktop = out.stdout.decode().split("=")[1].strip()
            desktop = desktop.lower()
        except Exception as e:
            desktop = "unknown"

    print("Your desktop is " + desktop)
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
    elif desktop in ("worm", "/usr/share/xsessions/worm"):
        return "pkill worm"
    elif desktop in ("berry", "/usr/share/xsessions/berry"):
        return "pkill berry"
    # for lxdm
    elif desktop in ("Xmonad", "/usr/share/xsessions/xmonad"):
        return "pkill xmonad"
    elif desktop in ("dwm", "/usr/share/xsessions/dwm"):
        return "pkill dwm"
    elif desktop in ("flexi", "/usr/share/xsessions/flexi"):
        return "pkill flexi"
    elif desktop in ("sunset", "/usr/share/xsessions/sunset"):
        return "pkill sunset"
    elif desktop in ("i3", "/usr/share/xsessions/i3"):
        return "pkill i3"
    elif desktop in ("i3-with-shmlog", "/usr/share/xsessions/i3-with-shmlog"):
        return "pkill i3-with-shmlog"
    elif desktop in ("lxqt", "/usr/share/xsessions/lxqt"):
        return "pkill lxqt"
    elif desktop in ("spectrwm", "/usr/share/xsessions/spectrwm"):
        return "pkill spectrwm"
    elif desktop in ("xfce", "/usr/share/xsessions/xfce"):
        return "xfce4-session-logout -f -l"
    elif desktop in ("icewm", "/usr/share/xsessions/icewm"):
        return "pkill icewm"
    elif desktop in ("icewm-session", "/usr/share/xsessions/icewm-session"):
        return "pkill icewm-session"
    elif desktop in ("cwm", "/usr/share/xsessions/cwm"):
        return "pkill cwm"
    elif desktop in ("fvwm3", "/usr/share/xsessions/fvwm3"):
        return "pkill fvwm3"
    elif desktop in ("stumpwm", "/usr/share/xsessions/stumpwm"):
        return "pkill stumpwm"
    elif desktop in ("leftwm", "/usr/share/xsessions/leftwm"):
        return "pkill leftwm"
    elif desktop in ("hypr", "/usr/share/xsessions/hypr"):
        return "pkill Hypr"
    elif desktop in ("dk", "/usr/share/xsessions/dk"):
        return "dkcmd exit"
    elif desktop in ("dusk", "/usr/share/xsessions/dusk"):
        return "pkill dusk"
    elif desktop in ("wmderland", "/usr/share/xsessions/wmderland"):
        return "pkill wmderland"
    elif desktop in ("gnome", "/usr/share/xsessions/gnome"):
        return "gnome-session-quit --logout --no-prompt"
    elif desktop in ("gnome-xorg", "/usr/share/xsessions/gnome-xorg"):
        return "gnome-session-quit --logout --no-prompt"
    elif desktop in ("gnome-classic", "/usr/share/xsessions/gnome-classic"):
        return "gnome-session-quit --logout --no-prompt"
    elif desktop in ("nimdow", "/usr/share/xsessions/nimdow"):
        return "pkill nimdow"

    # wayland desktops
    elif desktop in ("sway", "/usr/share/wayland-sessions/sway"):
        return "pkill sway"
    elif desktop in ("hyprland", "/usr/share/wayland-sessions/hyprland"):
        return "hyprctl dispatch exit"
    elif desktop in ("river", "/usr/share/wayland-sessions/river"):
        return "pkill river"
    elif desktop in ("wayfire", "/usr/share/wayland-sessions/wayfire"):
        return "pkill wayfire"
    elif desktop in ("newm", "/usr/share/wayland-sessions/newm"):
        return "pkill newm"
    elif desktop:
        return "pkill awesome | pkill nimdow| pkill bspwm | pkill cwm |  pkill dwm | pkill flexi | pkill dusk | pkill fvwm3 | pkill herbstluftwm | pkill i3 | pkill icewm | pkill jwm | pkill leftwm | pkill lxqt | pkill openbox | pkill qtile | pkill spectrwm | pkill wmderland | pkill xmonad | pkill worm | pkill berry | pkill Hypr | pkill hypr | pkill sway | pkill wayfire | pkill newm | pkill river"
    return None


def button_active(self, data, GdkPixbuf):
    try:
        if data == self.binds["shutdown"]:
            psh = GdkPixbuf.Pixbuf().new_from_file_at_size(
                os.path.join(
                    working_dir, "themes/" + self.theme + "/shutdown_blur.svg"
                ),
                self.icon,
                self.icon,
            )
            self.imagesh.set_from_pixbuf(psh)
            self.lbl1.set_markup('<span foreground="white">Shutdown</span>')
        elif data == self.binds["restart"]:
            pr = GdkPixbuf.Pixbuf().new_from_file_at_size(
                os.path.join(working_dir, "themes/" + self.theme + "/restart_blur.svg"),
                self.icon,
                self.icon,
            )
            self.imager.set_from_pixbuf(pr)
            self.lbl2.set_markup('<span foreground="white">Restart</span>')
        elif data == self.binds["suspend"]:
            ps = GdkPixbuf.Pixbuf().new_from_file_at_size(
                os.path.join(working_dir, "themes/" + self.theme + "/suspend_blur.svg"),
                self.icon,
                self.icon,
            )
            self.images.set_from_pixbuf(ps)
            self.lbl3.set_markup('<span foreground="white">Suspend</span>')
        elif data == self.binds["lock"]:
            plk = GdkPixbuf.Pixbuf().new_from_file_at_size(
                os.path.join(working_dir, "themes/" + self.theme + "/lock_blur.svg"),
                self.icon,
                self.icon,
            )
            self.imagelk.set_from_pixbuf(plk)
            self.lbl4.set_markup('<span foreground="white">Lock</span>')
        elif data == self.binds["logout"]:
            plo = GdkPixbuf.Pixbuf().new_from_file_at_size(
                os.path.join(working_dir, "themes/" + self.theme + "/logout_blur.svg"),
                self.icon,
                self.icon,
            )
            self.imagelo.set_from_pixbuf(plo)
            self.lbl5.set_markup('<span foreground="white">Logout</span>')
        elif data == self.binds["cancel"]:
            plo = GdkPixbuf.Pixbuf().new_from_file_at_size(
                os.path.join(working_dir, "themes/" + self.theme + "/cancel_blur.svg"),
                self.icon,
                self.icon,
            )
            self.imagec.set_from_pixbuf(plo)
            self.lbl6.set_markup('<span foreground="white">Cancel</span>')
        elif data == self.binds["hibernate"]:
            plo = GdkPixbuf.Pixbuf().new_from_file_at_size(
                os.path.join(
                    working_dir, "themes/" + self.theme + "/hibernate_blur.svg"
                ),
                self.icon,
                self.icon,
            )
            self.imageh.set_from_pixbuf(plo)
            self.lbl7.set_markup('<span foreground="white">Hibernate</span>')
    except:
        pass


def button_toggled(self, data):
    self.Esh.set_sensitive(False)
    self.Er.set_sensitive(False)
    self.Es.set_sensitive(False)
    self.Elk.set_sensitive(False)
    self.El.set_sensitive(False)
    self.Ec.set_sensitive(False)
    self.Eh.set_sensitive(False)

    if data == self.binds["shutdown"]:
        self.Esh.set_sensitive(True)
    elif data == self.binds["restart"]:
        self.Er.set_sensitive(True)
    elif data == self.binds["suspend"]:
        self.Es.set_sensitive(True)
    elif data == self.binds["lock"]:
        self.Elk.set_sensitive(True)
    elif data == self.binds["logout"]:
        self.El.set_sensitive(True)
    elif data == self.binds["cancel"]:
        self.Ec.set_sensitive(True)
    elif data == self.binds["hibernate"]:
        self.Eh.set_sensitive(True)


def file_check(file):
    if os.path.isfile(file):
        return True


# def get_distro(self):
# print(distro.id())
#    return(distro.id())
