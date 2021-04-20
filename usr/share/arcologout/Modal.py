
# =====================================================
#        Authors Brad Heffernan and Erik Dubois
# =====================================================

import gi
import subprocess
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GdkPixbuf, GLib


class ModalBox(Gtk.Window):
    def __init__(self, state):
        super(ModalBox, self).__init__(type=Gtk.WindowType.POPUP, title="NOT FOUND!")
        self.set_size_request(300, 220)
        self.set_position(Gtk.WindowPosition.CENTER_ALWAYS)
        print(state)
        lbl = Gtk.Label() 
        lbl.set_markup("<b>Arcolinux Betterlockscreen GUI</b> was not found on your system\nwould you like to install it?")
        self.add(lbl)

        if state is True:
            subprocess.run(['pkexec', 'pacman', '-S', '--noconfirm', 'arcolinux-betterlockscreen-git'], shell=False)