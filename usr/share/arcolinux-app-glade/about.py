#!/usr/bin/env python3

# ArcoLinux App - https://www.arcolinuxiso.com/arcolinux-app/
# Copyright (C) 2023 EriK Dubois - Drunken Alcoholic
#
# ArcoLinux App is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# ArcoLinux App is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Gufw; if not, see http://www.gnu.org/licenses for more
# information.

import gi
import webbrowser
import functions as fn

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

# constant values
BASE_DIR = fn.path.dirname(fn.path.realpath(__file__))
GUI_UI_FILE = fn.os.path.join(BASE_DIR + "/about.ui")


class About(Gtk.Window):
    def __init__(self):
        self.builder = Gtk.Builder()
        self.builder.add_from_file(GUI_UI_FILE)

        self.win_about = self.builder.get_object("about")
        # self.win_about.set_transient_for(self.main)
        self.win_about.connect("response", lambda d, r: d.destroy())
        self.win_about.show()

    def on_website_link_activate(self, *args):
        fn.run_as_user(webbrowser.open("https://www.arcolinuxiso.com/arcolinux-app/"))
