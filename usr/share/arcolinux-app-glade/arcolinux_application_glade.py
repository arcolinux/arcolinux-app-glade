#!/usr/bin/env python3

# ArcoLinux App - https://www.arcolinuxiso.com/arcolinux-app/
# Copyright (C) 2023 EriK Dubois
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

import os
import logging
from datetime import datetime
from time import sleep

import functions as fn

# Importing gi
import gi
import splash
import about

# https://docs.gtk.org/gtk3/
gi.require_version("Gtk", "3.0")
# https://docs.gtk.org/gdk3/
from gi.repository import Gdk, GdkPixbuf, GLib, Gtk  # noqa

# constant values
BASE_DIR = fn.path.dirname(fn.path.realpath(__file__))
GUI_UI_FILE = os.path.join(BASE_DIR + "/gGui.ui")
LOGGING_FORMAT = "%Y-%m-%d-%H-%M-%S"
LOGGING_LEVEL = logging.DEBUG
LOG_FILE = "/var/log/arcolinux-app-glade/arcolinux-app-{}.log".format(
    datetime.now().strftime(LOGGING_FORMAT)
)

if not fn.path.exists(fn.log_dir):
    fn.mkdir(fn.log_dir)


# https://docs.python.org/3/tutorial/classes.html
# https://realpython.com/python-main-function/
class Main:
    choice = "arconet"
    enabled_hold = False

    def __init__(self):
        # Setup intialization for logging and Gui
        self.splash()
        self.setup_logging()
        self.back_ups()
        self.cleanup()
        self.versioning()
        self.setup_gui()

    def splash(self):
        # splash screen
        splScr = splash.splashScreen()
        while Gtk.events_pending():
            Gtk.main_iteration()
        sleep(1)
        splScr.destroy()

    def setup_logging(self):
        # defining handlers for terminal and log file
        self.handlers = [
            logging.FileHandler(LOG_FILE),
            logging.StreamHandler(),
        ]

        # basic configuration
        # https://docs.python.org/3/howto/logging.html (debug,info,warning,error,critical)
        logging.basicConfig(
            level=LOGGING_LEVEL,
            format="%(asctime)s:%(levelname)s : %(message)s",
            datefmt=LOGGING_FORMAT,
            handlers=self.handlers,
        )

    def back_ups(self):
        # making sure the tool follows a dark or light theme
        if not fn.path.isdir("/root/.config/"):
            try:
                fn.mkdir("/root/.config", 0o766)
            except Exception as error:
                logging.error(error)

        if not fn.path.isdir("/root/.config/gtk-3.0"):
            try:
                fn.mkdir("/root/.config/gtk-3.0", 0o766)
            except Exception as error:
                logging.error(error)

        if not fn.path.isdir("/root/.config/gtk-4.0"):
            try:
                fn.mkdir("/root/.config/gtk-4.0", 0o766)
            except Exception as error:
                logging.error(error)

        if not fn.path.isdir("/root/.config/xsettingsd"):
            try:
                fn.mkdir("/root/.config/xsettingsd", 0o766)
            except Exception as error:
                logging.error(error)

        # make backup of /etc/pacman.conf
        if fn.path.isfile(fn.pacman_conf):
            if not fn.path.isfile(fn.pacman_conf + ".bak"):
                try:
                    fn.shutil.copy(fn.pacman_conf, fn.pacman_conf + ".bak")
                    logging.info("Making a backup of /etc/pacman.conf")
                except Exception as error:
                    logging.error(error)

        # ensuring we have a backup or the arcolinux mirrorlist
        if fn.path.isfile(fn.mirrorlist):
            if not fn.path.isfile(fn.mirrorlist + ".bak"):
                try:
                    fn.shutil.copy(fn.mirrorlist, fn.mirrorlist + ".bak")
                    logging.info("Making a backup of /etc/pacman.d/mirrorlist")

                except Exception as error:
                    logging.error(error)

    def cleanup(self):
        # making sure /root is clean
        # arconet
        if fn.path.isdir("/root/arconet-build/"):
            try:
                fn.remove_dir(self, "/root/arconet-build/")
                logging.info("Removing old builds")
                logging.info("This may take a while - be patient")
            except Exception as error:
                logging.error(error)

        if fn.path.isdir("/root/arconet-Out/"):
            try:
                fn.remove_dir(self, "/root/arconet-Out/")
                logging.info("Removing old builds")
                logging.info("This may take a while - be patient")
            except Exception as error:
                logging.error(error)

        # arcopro
        if fn.path.isdir("/root/arcopro-build/"):
            try:
                fn.remove_dir(self, "/root/arcopro-build/")
                logging.info("Removing old builds")
                logging.info("This may take a while - be patient")
            except Exception as error:
                logging.error(error)

        if fn.path.isdir("/root/arcopro-Out/"):
            try:
                fn.remove_dir(self, "/root/arcopro-Out/")
                logging.info("Removing old builds")
                logging.info("This may take a while - be patient")
            except Exception as error:
                logging.error(error)

        # arcoplasma
        if fn.path.isdir("/root/arcoplasma-build/"):
            try:
                fn.remove_dir(self, "/root/arcoplasma-build/")
                logging.info("Removing old builds")
                logging.info("This may take a while - be patient")
            except Exception as error:
                logging.error(error)

        if fn.path.isdir("/root/arcoplasma-Out/"):
            try:
                fn.remove_dir(self, "/root/arcoplasma-Out/")
                logging.info("Removing old builds")
                logging.info("This may take a while - be patient")
            except Exception as error:
                logging.error(error)

        if fn.path.isdir("/root/Ariser-build/"):
            try:
                fn.remove_dir(self, "/root/Ariser-build/")
                logging.info("Removing old builds")
                logging.info("This may take a while - be patient")
            except Exception as error:
                logging.error(error)

        if fn.path.isdir("/root/Ariser-Out/"):
            try:
                fn.remove_dir(self, "/root/Ariser-Out/")
                logging.info("Removing old builds")
                logging.info("This may take a while - be patient")
            except Exception as error:
                logging.error(error)

    def versioning(self):
        logging.info("App Started")
        logging.info(
            "---------------------------------------------------------------------------"
        )
        logging.info("pkgver = pkgversion")
        logging.info("pkgrel = pkgrelease")
        logging.info(
            "---------------------------------------------------------------------------"
        )
        logging.info("Distro = " + fn.distr)
        logging.info(
            "---------------------------------------------------------------------------"
        )

    def setup_gui(self):
        self.timeout_id = None

        # https://python-gtk-3-tutorial.readthedocs.io/en/latest/builder.html
        logging.info("Building the Gui from the glade file")
        self.builder = Gtk.Builder()
        self.builder.add_from_file(GUI_UI_FILE)

        logging.info("Connecting the glade signals")
        self.builder.connect_signals(self)

        logging.info("Referencing the Gtk window 'hwindow' ID")
        window = self.builder.get_object("hWindow")
        window.connect("delete-event", Gtk.main_quit)

        self.statusbar = self.builder.get_object("statusbar")

        message = Gtk.Label(label="We will show all the messages here")

        context_id = self.statusbar.get_context_id("example")
        self.statusbar.push(context_id, message.get_text())

        combobox = self.builder.get_object("iso_choices")
        combobox.set_wrap_width(1)

        logging.info("Display main window")
        window.show()

    def on_close_clicked(self, widget):
        Gtk.main_quit()

    ############################################################################
    ############################################################################
    ############################################################################
    # Start application
    ############################################################################
    ############################################################################
    ############################################################################

    def on_iso_choices_changed(self, widget):
        # Here we select the ArcoLinux iso in the dropdown
        self.choice = widget.get_active_text()
        logging.info("You selected = " + self.choice)

    def on_hold_toggled(self, widget):
        # We might need this option to keep alacritty open to see errors
        self.enabled_hold = widget.get_active()
        if self.enabled_hold:
            logging.info("--hold for Alacritty is on")
        else:
            logging.info("--hold for Alacritty is off")

    def on_create_arco_clicked(self, widget):
        # Creation of the ArcoLinux iso
        logging.info("ArcoLinux iso selection is: %s", self.choice)

        # installing archiso if needed
        package = "archiso"
        fn.install_package(self, package)

        # if arcolinux mirror and key not installed
        if not fn.check_package_installed(
            "arcolinux-keyring"
        ) or not fn.check_package_installed("arcolinux-mirrorlist-git"):
            logging.info("Installing the ArcoLinux keyring and mirrorlist")

            fn.install_arcolinux_key_mirror(self)
            fn.add_repos()

        # making sure we start with a clean slate
        logging.info("Let's remove any old previous building folders")
        fn.remove_dir(self, "/root/arconet-Out")
        fn.remove_dir(self, "/root/arcopro-Out")
        fn.remove_dir(self, "/root/arcoplasma-Out")

        # git clone the iso scripts
        if "arconet" in self.choice:
            # https://github.com/arconetpro/arconet-iso
            command = (
                "git clone https://github.com/arconetpro/arconet-iso"
                + " /tmp/"
                + self.choice
            )
        if "arcopro" in self.choice:
            # https://github.com/arconetpro/arcopro-iso
            command = (
                "git clone https://github.com/arconetpro/arcopro-iso"
                + " /tmp/"
                + self.choice
            )
        if "arcoplasma" in self.choice:
            # https://github.com/arconetpro/arcoplasma-iso
            command = (
                "git clone https://github.com/arconetpro/arcoplasma-iso"
                + " /tmp/"
                + self.choice
            )
        logging.info("git cloning the build folder")
        try:
            fn.run_command(command)
        except Exception as error:
            logging.error(error)

        # launch the scripts
        # /tmp/arcopro/installation-scripts/40-build-the-iso-local-again.sh
        logging.info("Start building the iso in Alacritty")
        logging.info(
            "#################################################################"
        )
        logging.info("Sometimes you have to try and build it a second time")
        logging.info(
            "for it to work because of the special packages from AUR and repos"
        )
        logging.info(
            "##################################################################"
        )
        logging.info(
            "Changed to /tmp/" + self.choice + "/installation-scripts/" + " folder"
        )
        fn.os.chdir("/tmp/" + self.choice + "/installation-scripts/")

        # Preparing to launch the build
        command = (
            "/tmp/"
            + self.choice
            + "/installation-scripts/40-build-the-iso-local-again.sh"
        )

        logging.info("Launching the building script")

        # Checking whether switch is on
        if self.enabled_hold:
            critty = "alacritty --hold -e"
            logging.info("Using the hold option")
        else:
            logging.info("Not using the hold option")
            critty = "alacritty -e"

        # Launching the build
        try:
            fn.subprocess.call(
                critty + command,
                shell=True,
                stdout=fn.subprocess.PIPE,
                stderr=fn.subprocess.STDOUT,
            )
        except Exception as error:
            logging.error(error)

        # change the output - foldername
        if self.choice == "arconet":
            dir = "arconet-Out"
        elif self.choice == "arcopro":
            dir = "arcopro-Out"
        else:
            dir = "arcoplasma-Out"

        # Moving the iso to home directory of the user
        path_dir = "/root/" + dir
        destination = fn.home + "/" + dir
        logging.info("Move folder to home directory")
        try:
            fn.shutil.copytree(path_dir, destination, dirs_exist_ok=True)

            # Sending an in-app message
            GLib.idle_add(
                fn.show_in_app_notification,
                self,
                "The creation of the ArcoLinux iso is finished",
                False,
            )
        except Exception as error:
            logging.error(error)

        # changing permission
        fn.permissions(destination)
        logging.info("Check your home directory for the iso")

    def on_create_arch_clicked(self, widget):
        # Building the Arch Linux iso
        logging.info("Let's build an Arch Linux iso")

        # installing archiso if needed
        package = "archiso"
        fn.install_package(self, package)

        # making sure we start with a clean slate
        if fn.path_check(fn.base_dir + "/work"):
            fn.remove_dir(self, "fn.base_dir" + "/work")
            logging.info("Cleanup - Removing : " + fn.base_dir + "/work")
        if fn.path_check("/root/work"):
            fn.remove_dir(self, "/root/work")
            logging.info("Cleanup - Removing : /root/work")

        # starting the Arch Linux build script
        command = "mkarchiso -v -o " + fn.home + " /usr/share/archiso/configs/releng/"
        try:
            fn.run_command(command)
        except Exception as error:
            logging.error(error)

        # changing permission and add date
        x = datetime.now()
        year = str(x.year)
        month = str(x.strftime("%m"))
        day = str(x.strftime("%d"))
        iso_name = "/archlinux-" + year + "." + month + "." + day + "-x86_64.iso"
        destination = fn.home + iso_name
        fn.permissions(destination)
        logging.info("Check your home directory for the iso")

        # making sure we start with a clean slate
        if fn.path_check(fn.base_dir + "/work"):
            fn.remove_dir(self, "fn.base_dir" + "/work")
            logging.info("Cleanup - Removing : " + fn.base_dir + "/work")
        if fn.path_check("/root/work"):
            fn.remove_dir(self, "/root/work")
            logging.info("Cleanup - Removing : /root/work")

        # Sending an in-app message
        GLib.idle_add(
            fn.show_in_app_notification,
            self,
            "The creation of the Arch Linux iso is finished",
            False,
        )

    def on_create_ariser_clicked(self, widget):
        # Creation of the Ariser iso
        logging.info("Ariser iso selected")

        # installing archiso if needed
        package = "archiso"
        fn.install_package(self, package)

        # making sure we start with a clean slate
        logging.info("Let's remove any old previous building folders")
        fn.remove_dir(self, "/root/Ariser-Out")
        fn.remove_dir(self, "/root/Ariser-build")

        # git clone the iso scripts
        command = (
            "git clone https://github.com/ariser-installer/ariser.git" + " /tmp/ariser"
        )

        logging.info("git cloning the build folder")
        try:
            fn.run_command(command)
        except Exception as error:
            logging.error(error)

        # launch the scripts
        logging.info("Start building the iso in Alacritty")
        logging.info(
            "#################################################################"
        )
        logging.info("Sometimes you have to try and build it a second time")
        logging.info("for it to work because of servers and network connections")
        logging.info(
            "##################################################################"
        )
        logging.info("Changed to /tmp/ariser")
        fn.os.chdir("/tmp/ariser")

        # Preparing to launch the build
        command = "/tmp/ariser/build-archlinux-with-alis.sh"

        logging.info("Launching the building script")

        # Checking whether switch is on
        critty = "alacritty -e"

        # Launching the build
        try:
            fn.subprocess.call(
                critty + command,
                shell=True,
                stdout=fn.subprocess.PIPE,
                stderr=fn.subprocess.STDOUT,
            )
        except Exception as error:
            logging.error(error)

        # change the output - foldername
        dir = "Ariser-Out"

        # Moving the iso to home directory of the user
        path_dir = "/root/" + dir
        destination = fn.home + "/" + dir
        logging.info("Move folder to home directory")
        try:
            fn.shutil.copytree(path_dir, destination, dirs_exist_ok=True)

            # Sending an in-app message
            GLib.idle_add(
                fn.show_in_app_notification,
                self,
                "The creation of the Ariser iso is finished",
                False,
            )
        except Exception as error:
            logging.error(error)

        # changing permission
        fn.permissions(destination)
        logging.info("Check your home directory for the iso")

    def on_create_sierra_clicked(self, widget):
        # Creation of the Sierra iso
        logging.info("Sierra iso selected")

        # installing archiso if needed
        package = "archiso"
        fn.install_package(self, package)

        # making sure we start with a clean slate
        logging.info("Let's remove any old previous building folders")
        fn.remove_dir(self, "/root/Sierra-Out")
        fn.remove_dir(self, "/root/Sierra-build")

        # git clone the iso scripts
        command = (
            "git clone https://github.com/ariser-installer/sierra.git" + " /tmp/sierra"
        )

        logging.info("git cloning the build folder")
        try:
            fn.run_command(command)
        except Exception as error:
            logging.error(error)

        # launch the scripts
        logging.info("Start building the iso in Alacritty")
        logging.info(
            "#################################################################"
        )
        logging.info("Sometimes you have to try and build it a second time")
        logging.info("for it to work because of servers and network connections")
        logging.info(
            "##################################################################"
        )
        logging.info("Changed to /tmp/sierra")
        fn.os.chdir("/tmp/sierra")

        # Preparing to launch the build
        command = "/tmp/sierra/build-archlinux-with-alis.sh"

        logging.info("Launching the building script")

        # Checking whether switch is on
        critty = "alacritty -e"

        # Launching the build
        try:
            fn.subprocess.call(
                critty + command,
                shell=True,
                stdout=fn.subprocess.PIPE,
                stderr=fn.subprocess.STDOUT,
            )
        except Exception as error:
            logging.error(error)

        # change the output - foldername
        dir = "Sierra-Out"

        # Moving the iso to home directory of the user
        path_dir = "/root/" + dir
        destination = fn.home + "/" + dir
        logging.info("Move folder to home directory")
        try:
            fn.shutil.copytree(path_dir, destination, dirs_exist_ok=True)

            # Sending an in-app message
            GLib.idle_add(
                fn.show_in_app_notification,
                self,
                "The creation of the Sierra iso is finished",
                False,
            )
        except Exception as error:
            logging.error(error)

        # changing permission
        fn.permissions(destination)
        logging.info("Check your home directory for the iso")

    def on_clean_pacman_cache_clicked(self, widget):
        # Cleaning the /var/cache/pacman/pkg/
        logging.info("Let's clean the pacman cache")
        command = "yes | pacman -Scc"
        package = "alacritty"
        fn.install_package(self, package)
        try:
            fn.subprocess.call(
                command,
                shell=True,
                stdout=fn.subprocess.PIPE,
                stderr=fn.subprocess.STDOUT,
            )
            logging.info("Pacman cache cleaned")

            # Sending an in-app message
            GLib.idle_add(
                fn.show_in_app_notification,
                self,
                "Pacman cache cleaned",
                False,
            )
        except Exception as error:
            logging.error(error)

    def on_fix_arch_clicked(self, widget):
        # Resetting the Arch Linux keys and more
        logging.info("Let's fix the keys of Arch Linux")
        command = fn.base_dir + "/scripts/fixkey"
        package = "alacritty"
        fn.install_package(self, package)
        fn.run_script_alacritty_hold(self, command)

        # Sending an in-app message
        GLib.idle_add(
            fn.show_in_app_notification,
            self,
            "We fixed the keys of Arch Linux",
            False,
        )

    def on_probe_clicked(self, widget):
        # Gathering information with hw-probe
        logging.info("Let's create the probe link")
        command = fn.base_dir + "/scripts/probe"
        package = "hw-probe"
        fn.install_package(self, package)
        fn.run_script_alacritty_hold(self, command)

        # Sending an in-app message
        GLib.idle_add(
            fn.show_in_app_notification,
            self,
            "Creation of probe link is finished",
            False,
        )

    def on_get_nemesis_clicked(self, widget):
        # Download the ArcoLinux Nemesis scripts
        logging.info("Get the ArcoLinux nemesis scripts")
        logging.info("We create a DATA folder in your home dir")
        logging.info("We git clone the scripts in there")

        # Running the script
        command = fn.base_dir + "/scripts/get-nemesis-on-arcolinux-app"
        package = "alacritty"
        fn.install_package(self, package)
        fn.run_script(self, command)
        path_dir = "/root/DATA"
        destination = fn.home + "/DATA"

        # Move folder to home directory
        try:
            fn.shutil.copytree(path_dir, destination, dirs_exist_ok=True)
        except Exception as error:
            logging.error(error)

        logging.info("We saved the scripts to ~/DATA/arcolinux-nemesis")

        fn.permissions(destination)

        # Sending an in-app message
        GLib.idle_add(
            fn.show_in_app_notification,
            self,
            "We installed the ArcoLinux Nemesis scripts in ~/DATA",
            False,
        )

    def on_arch_server_clicked(self, widget):
        # Setting the Arch Linux mirrorlist
        logging.info("Let's change the Arch Linux mirrors")

        # Running the script
        command = fn.base_dir + "/scripts/best-arch-servers"
        package = "alacritty"
        fn.install_package(self, package)
        fn.run_script(self, command)
        logging.info("We changed the content of your /etc/pacman.d/mirrorlist")
        logging.info("Server = https://mirror.osbeck.com/archlinux/$repo/os/$arch")
        logging.info("Server = http://mirror.osbeck.com/archlinux/$repo/os/$arch")
        logging.info("Server = https://mirrors.kernel.org/archlinux/$repo/os/$arch")
        logging.info("Server = https://geo.mirror.pkgbuild.com/$repo/os/$arch")
        logging.info("Server = http://mirror.rackspace.com/archlinux/$repo/os/$arch")
        logging.info("Server = https://mirror.rackspace.com/archlinux/$repo/os/$arch")

        logging.info("Done")

        # Sending an in-app message
        GLib.idle_add(
            fn.show_in_app_notification,
            self,
            "We changed the content of your /etc/pacman.d/mirrorlist",
            False,
        )

    def on_arco_key_mirror_clicked_install(self, widget):
        # Installing the ArcoLinux keys and ArcoLinux mirrorlist
        logging.info("Let's install the ArcoLinux keys and mirrors")
        logging.info("Installing the ArcoLinux repos in /etc/pacman.conf")
        fn.install_arcolinux_key_mirror(self)
        fn.add_repos()

        # Sending an in-app message
        GLib.idle_add(
            fn.show_in_app_notification,
            self,
            "Installing the ArcoLinux repos in /etc/pacman.conf",
            False,
        )

    def on_arco_key_mirror_clicked_remove(self, widget):
        # Remove the ArcoLinux keys and ArcoLinux mirrorlist
        logging.info("Let's remove the ArcoLinux keys and mirrors")

        fn.remove_arcolinux_key_mirror(self)
        logging.info("Let's remove the ArcoLinux keys and mirrors")
        logging.info("Removing the ArcoLinux repos in /etc/pacman.conf")
        fn.remove_repos()

        # Sending an in-app message
        GLib.idle_add(
            fn.show_in_app_notification,
            self,
            "Removing the ArcoLinux repos in /etc/pacman.conf",
            False,
        )

    def on_pacman_reset_local_clicked(self, widget):
        # Using the local backup to reset /etc/pacman.conf
        if fn.path.isfile(fn.pacman_conf + ".bak"):
            fn.shutil.copy(fn.pacman_conf + ".bak", fn.pacman_conf)
            logging.info("We have used /etc/pacman.conf.bak to reset /etc/pacman.conf")

            # Ensuring that pacman does not crash - installing/removing keys and mirrors
            fn.pacman_safeguard()

        # Sending an in-app message
        GLib.idle_add(
            fn.show_in_app_notification,
            self,
            "We have used /etc/pacman.conf.bak to reset /etc/pacman.conf",
            False,
        )

    def on_pacman_reset_cached_clicked(self, widget):
        # Using the ArcoLinux cached file to reset /etc/pacman.conf
        # Depending on what distro you are - we use the original pacman.conf

        fn.shutil.copy(fn.pacman_arco, fn.pacman_conf)

        if fn.distr == "arch":
            fn.shutil.copy(fn.pacman_arch, fn.pacman_conf)
        if fn.distr == "endeavouros":
            fn.shutil.copy(fn.pacman_eos, fn.pacman_conf)
        if fn.distr == "garuda":
            fn.shutil.copy(fn.pacman_garuda, fn.pacman_conf)
        logging.info("We have used the cached pacman.conf")

        # Ensuring that pacman does not crash - installing/removing keys and mirrors
        fn.pacman_safeguard()

        # Sending an in-app message
        GLib.idle_add(
            fn.show_in_app_notification,
            self,
            "We have used the cached pacman.conf",
            False,
        )

    def on_pacman_install_packages(self, widget):
        # Install the package via file

        filechooserbutton = self.builder.get_object("install_path")
        path = filechooserbutton.get_filename()
        if len(path) > 1:
            logging.info("Installing packages from selected file")
            logging.info("You selected this file")
            logging.info("File: " + path)
            fn.install_packages_path(self, path)

            # Sending an in-app message
            GLib.idle_add(
                fn.show_in_app_notification,
                self,
                "Packages installed from selected file",
                False,
            )
        else:
            logging.info("First select a file")

    def on_asa_install_clicked(self, widget):
        fn.install_arcolinux_spices_application(self)
        # Sending an in-app message
        GLib.idle_add(
            fn.show_in_app_notification,
            self,
            "We have installed the ASA",
            False,
        )

    def on_att_install_clicked(self, widget):
        fn.install_archlinux_tweak_tool(self)
        # Sending an in-app message
        GLib.idle_add(
            fn.show_in_app_notification,
            self,
            "We have installed the ATT",
            False,
        )

    def on_about_clicked(self, widget):
        # About dialog
        aboutwin = about.About()

    def on_quit_button_clicked(self, widget):
        # Ending the application
        Gtk.main_quit()
        print(
            "---------------------------------------------------------------------------"
        )
        print("Thanks for using the ArcoLinux Application")
        print("We hope you enjoyed the Youtube tutorials")
        print(
            "https://www.youtube.com/playlist?list=PLlloYVGq5pS63vf2ksZntZmWwiJK_gtFt"
        )
        print(
            "---------------------------------------------------------------------------"
        )


if __name__ == "__main__":
    main = Main()
    Gtk.main()
