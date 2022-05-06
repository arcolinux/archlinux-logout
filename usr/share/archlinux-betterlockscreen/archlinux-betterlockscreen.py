#!/usr/bin/env python3

# =================================================================
# =                  Author: Brad Heffernan                       =
# =================================================================

import gi
import Functions as fn
import GUI
import Support
import threading as th
import webbrowser
import Splash
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GdkPixbuf, Gdk, GLib # noqa


class Main(Gtk.Window):
    def __init__(self):
        super(Main, self).__init__(title="ArchLinux BetterLockScreen")
        self.set_border_width(10)
        self.set_default_size(700, 460)
        self.connect("delete-event", self.close)
        self.set_icon_from_file(fn.os.path.join(
            GUI.base_dir, 'images/archlinux.png'))
        self.set_position(Gtk.WindowPosition.CENTER)

        self.timeout_id = None
        self.image_path = None

        if not fn.os.path.isdir(fn.config):
            fn.os.mkdir(fn.config)

        if not fn.os.path.isfile(fn.config + fn.settings):
            with open(fn.config + fn.settings, "w") as f:
                f.write("path=")
                f.close()

        self.loc = Gtk.Entry()
        self.search = Gtk.Entry()
        self.status = Gtk.Label(label="")
        self.hbox3 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL,
                             spacing=10)
        scrolled = Gtk.ScrolledWindow()
        scrolled.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)

        self.fb = Gtk.FlowBox()
        self.fb.set_valign(Gtk.Align.START)
        self.fb.set_max_children_per_line(6)
        self.fb.set_selection_mode(Gtk.SelectionMode.SINGLE)
        self.fb.connect("child-activated", self.on_item_clicked)
        # self.create_flowbox(fb)

        scrolled.add(self.fb)

        self.hbox3.pack_start(scrolled, True, True, 0)

        splScr = Splash.splashScreen()

        while Gtk.events_pending():
            Gtk.main_iteration()
        # self.create_flowbox(self.loc.get_text())
        t = th.Thread(target=self.create_flowbox,
                      args=(self.loc.get_text(), False))
        t.daemon = True
        t.start()
        t.join()

        splScr.destroy()

        GUI.GUI(self, Gtk, GdkPixbuf, Gdk, th, fn)

        with open("/tmp/archlinux-betterlock.lock", "w") as f:
            f.write("")
            f.close()

    def on_default_clicked(self, widget, fb):
        # self.fb.select_all()

        for x in self.fb.get_children():
            self.fb.remove(x)

        t = th.Thread(target=self.create_flowbox,
                      args=(self.loc.get_text(), True))
        t.daemon = True
        t.start()

    def on_support_clicked(self, widget):
        sup = Support.Support(self)
        response = sup.run()

        if response == Gtk.ResponseType.DELETE_EVENT:
            sup.destroy()

    def on_apply_clicked(self, widget):
        # print(str(int(self.blur.get_value())/100))
        if self.image_path is None:
            fn.show_in_app_notification(self,
                                        "You need to select an image first")
        else:
            self.btnset.set_sensitive(False)
            self.status.set_text("creating lockscreen images....wait for the message at the top")
            t = th.Thread(target=self.set_lockscreen, args=())
            t.daemon = True
            t.start()

    def set_lockscreen(self):
        command = ["betterlockscreen", "-u", self.image_path,
                       "--blur", str(int(self.blur.get_value())/100)]
        try:
            #with fn.subprocess.Popen(command, bufsize=1, stdout=fn.subprocess.PIPE, universal_newlines=True) as p:
            #    for line in p.stdout:
            #        GLib.idle_add(self.status.set_text, line.strip())
            fn.subprocess.call(command, shell=False)
            fn.show_in_app_notification(self, "Lockscreen set successfully")
            GLib.idle_add(self.btnset.set_sensitive, True)
            GLib.idle_add(self.status.set_text, "")
        except:  # noqa
            GLib.idle_add(self.status.set_text, "ERROR: is betterlockscreen installed?")
            GLib.idle_add(self.btnset.set_sensitive, True)

    def on_item_clicked(self, widget, data):
        for x in data:
            self.image_path = x.get_name()
        # print(widget.get_selected_children())

    def on_load_clicked(self, widget, fb):
        # self.fb.select_all()

        for x in self.fb.get_children():
            self.fb.remove(x)

        t = th.Thread(target=self.create_flowbox,
                      args=(self.loc.get_text(), False))
        t.daemon = True
        t.start()

    def on_search_clicked(self, widget):
        for x in self.fb.get_children():
            self.fb.remove(x)

        t = th.Thread(target=self.create_flowbox,
                      args=(self.loc.get_text(), False))
        t.daemon = True
        t.start()

    def on_browse_clicked(self, widget):
        dialog = Gtk.FileChooserDialog(
                                       title="Please choose a file",
                                       action=Gtk.FileChooserAction.SELECT_FOLDER,)
        dialog.set_current_folder(fn.home)
        dialog.add_buttons(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, "Open",
                           Gtk.ResponseType.OK)
        dialog.connect("response", self.open_response_browse)

        dialog.show()

    def open_response_browse(self, dialog, response):
        if response == Gtk.ResponseType.OK:
            self.loc.set_text(dialog.get_filename())
            with open(fn.config + fn.settings, "w") as f:
                f.write("path=" + dialog.get_filename())
                f.close()
            dialog.destroy()
        elif response == Gtk.ResponseType.CANCEL:
            dialog.destroy()

    def create_flowbox(self, text, default):
        if not default:
            paths = fn.get_saved_path()
            if len(paths) < 1:
                if len(text) < 1:
                    paths = "/usr/share/archlinux-betterlockscreen/wallpapers/"
                    if not fn.os.path.isdir(paths):
                        paths = "/usr/share/archlinux-betterlockscreen/wallpapers/"
                    if not fn.os.path.isdir(paths):
                        return 0
                else:
                    paths = text
        else:
            paths = "/usr/share/archlinux-betterlockscreen/wallpapers/"
            if not fn.os.path.isdir(paths):
                paths = "/usr/share/archlinux-betterlockscreen/wallpapers/"
            if not fn.os.path.isdir(paths):
                return 0

        if paths.endswith("/"):
            paths = paths[:-1]

        if not fn.os.path.isdir(paths):
            GLib.idle_add(self.status.set_text, "That directory not found!")
            return 0
        try:
            ext = [".png", ".jpg", ".jpeg"]
            images = [x for x in fn.os.listdir(paths) for j in ext if j in x.lower() if self.search.get_text() in x] # noqa
            GLib.idle_add(self.status.set_text, "Loading images...")
            for image in images:
                # fbchild = Gtk.FlowBoxChild()
                pb = GdkPixbuf.Pixbuf().new_from_file_at_size(paths + "/" + image, 328, 328) # noqa
                pimage = Gtk.Image()
                pimage.set_name(paths + "/" + image)
                pimage.set_from_pixbuf(pb)
                # print(image)
                # fbchild.add(pimage)
                GLib.idle_add(self.fb.add,pimage)
                pimage.show_all()
        except Exception as e:
            print(e)
        GLib.idle_add(self.status.set_text, "")

    def on_social_clicked(self, widget, event, link):
        t = th.Thread(target=self.weblink, args=(link,))
        t.daemon = True
        t.start()

    def weblink(self, link):
        webbrowser.open_new_tab(link)

    def tooltip_callback(self, widget, x, y, keyboard_mode, tooltip, text):
        tooltip.set_text(text)
        return True

    def MessageBox(self, title, message):
        md = Gtk.MessageDialog(parent=self, flags=0,
                               message_type=Gtk.MessageType.INFO,
                               buttons=Gtk.ButtonsType.OK, text=title)
        md.format_secondary_markup(message)
        md.run()
        md.destroy()

    def close(self, widget, data):
        fn.os.unlink("/tmp/archlinux-betterlock.lock")
        Gtk.main_quit()


if __name__ == "__main__":
    if not fn.os.path.isfile("/tmp/archlinux-betterlock.lock"):
        with open("/tmp/archlinux-betterlock.pid", "w") as f:
            f.write(str(fn.os.getpid()))
            f.close()
        w = Main()
        w.show_all()
        Gtk.main()
    else:
        md = Gtk.MessageDialog(parent=Main(),
                               flags=0,
                               message_type=Gtk.MessageType.INFO,
                               buttons=Gtk.ButtonsType.YES_NO,
                               text="Lock File Found")
        md.format_secondary_markup(
            "The lock file has been found. This indicates there is already an instance of <b>ArchLinux Betterlockscreen GUI</b> running.\n\
click yes to remove the lock file and try running again")  # noqa

        result = md.run()
        md.destroy()

        if result in (Gtk.ResponseType.OK, Gtk.ResponseType.YES):
            pid = ""
            with open("/tmp/archlinux-betterlock.pid", "r") as f:
                line = f.read()
                pid = line.rstrip().lstrip()
                f.close()

            if fn.checkIfProcessRunning(int(pid)):
                fn.MessageBox(Main(), "Application Running!",
                                     "You first need to close the existing application")  # noqa
            else:
                fn.os.unlink("/tmp/archlinux-betterlock.lock")
