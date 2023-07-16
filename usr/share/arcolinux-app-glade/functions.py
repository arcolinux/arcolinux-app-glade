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
import shutil
import subprocess
from os import getlogin, listdir, mkdir, path, rmdir
from pathlib import Path

# we want our logging in the functions also
import logging

import psutil
from distro import id
from gi.repository import GLib

DEBUG = False

# =====================================================
#              BEGIN DECLARATION OF VARIABLES
# =====================================================

base_dir = path.dirname(path.realpath(__file__))
distr = id()
sudo_username = getlogin()
home = "/home/" + str(sudo_username)
message = "This is the ArcoLinux App"
arcolinux_mirrorlist = "/etc/pacman.d/arcolinux-mirrorlist"
mirrorlist = "/etc/pacman.d/mirrorlist"
log_dir = "/var/log/arcolinux-app-glade/"
pacman_conf = "/etc/pacman.conf"
pacman_arch = "/usr/share/arcolinux-app-glade/data/arch/pacman.conf"
pacman_arco = "/usr/share/arcolinux-app-glade/data/arco/pacman.conf"
pacman_eos = "/usr/share/arcolinux-app-glade/data/eos/pacman.conf"
pacman_garuda = "/usr/share/arcolinux-app-glade/data/garuda/pacman.conf"

atestrepo = "#[arcolinux_repo_testing]\n\
#SigLevel = PackageRequired DatabaseNever\n\
#Include = /etc/pacman.d/arcolinux-mirrorlist"

arepo = "[arcolinux_repo]\n\
SigLevel = PackageRequired DatabaseNever\n\
Include = /etc/pacman.d/arcolinux-mirrorlist"

a3prepo = "[arcolinux_repo_3party]\n\
SigLevel = PackageRequired DatabaseNever\n\
Include = /etc/pacman.d/arcolinux-mirrorlist"

axlrepo = "[arcolinux_repo_xlarge]\n\
SigLevel = PackageRequired DatabaseNever\n\
Include = /etc/pacman.d/arcolinux-mirrorlist"

# =====================================================
#              END DECLARATION OF VARIABLES
# =====================================================


# =====================================================
#               BEGIN GLOBAL FUNCTIONS
# =====================================================

# check if file exists


def file_check(file):
    if path.isfile(file):
        return True

    return False


# Check if path exists
def path_check(path):
    if os.path.isdir(path):
        return True
    return False


# getting the content of a file
def get_lines(files):
    try:
        if path.isfile(files):
            with open(files, "r", encoding="utf-8") as f:
                lines = f.readlines()
                f.close()
            return lines
    except Exception as error:
        logging.error(error)


# getting the string in list
def __get_position(lists, string):
    data = [x for x in lists if string in x]
    pos = lists.index(data[0])
    return pos


# get position in list
def get_position(lists, value):
    data = [string for string in lists if value in string]
    if len(data) != 0:
        position = lists.index(data[0])
        return position
    return 0


# get positions in list
def get_positions(lists, value):
    data = [string for string in lists if value in string]
    position = []
    for d in data:
        position.append(lists.index(d))
    return position


# check if process is running
def check_if_process_is_running(processName):
    for proc in psutil.process_iter():
        try:
            pinfo = proc.as_dict(attrs=["pid", "name", "create_time"])
            if processName == pinfo["name"]:
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return False


# check value in list
def check_value(list, value):
    data = [string for string in list if value in string]
    return data


# check if value is true or false in file
def check_content(value, file):
    try:
        with open(file, "r", encoding="utf-8") as myfile:
            lines = myfile.readlines()
            myfile.close()

        for line in lines:
            if value in line:
                if value in line:
                    return True
                else:
                    return False
        return False
    except:
        return False


# check if package is installed or not
def check_package_installed(package):
    try:
        subprocess.check_output(
            "pacman -Qi " + package, shell=True, stderr=subprocess.STDOUT
        )
        # package is installed
        return True
    except subprocess.CalledProcessError:
        # package is not installed
        return False


# check if repo exists
def repo_exist(value):
    with open(pacman_conf, "r", encoding="utf-8") as f:
        lines = f.readlines()
        f.close()

    for line in lines:
        if value in line:
            return True
    return False


# install package
def install_package(self, package):
    command = "pacman -S " + package + " --noconfirm --needed"
    # if more than one package - checf fails and will install
    if check_package_installed(package):
        logging.info("The package %s is already installed - nothing to do", package)

    else:
        try:
            logging.info("Applying this command: %s", command)
            subprocess.run(
                command.split(" "),
                shell=False,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
            )
            logging.info("The package %sis now installed", package)
        except Exception as error:
            logging.error(error)


# install ArcoLinux Spices Application
def install_arcolinux_spices_application(self):
    base_dir = path.dirname(path.realpath(__file__))
    pathway = base_dir + "/packages/asa/"
    file = listdir(pathway)

    try:
        command1 = "pacman -U " + pathway + str(file).strip("[]'") + " --noconfirm"
        logging.info("Applying this command: %s", command1)
        subprocess.run(
            command1.split(" "),
            shell=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )
        logging.info("ArcoLinux Spices Application(ASA) is now installed")
    except Exception as error:
        logging.error(error)

    if file_check("/usr/share/arcolinux-spices/scripts/get-the-keys-and-repos.sh"):
        try:
            command1 = (
                "pkexec /usr/share/arcolinux-spices/scripts/get-the-keys-and-repos.sh"
            )
            logging.info("Applying this command: %s", command1)
            subprocess.run(
                command1.split(" "),
                shell=False,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
            )
            logging.info("ArcoLinux keys and mirrorlist have been installed")
        except Exception as error:
            logging.error(error)
    else:
        print("Path to ArcoLinux Spices script does not exist")

    if file_check("/usr/bin/arcolinux-spices"):
        try:
            command1 = "pacman -Sy"
            logging.info("Applying this command: %s", command1)
            subprocess.run(
                command1.split(" "),
                shell=False,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
            )
            logging.info("ArcoLinux repos have been downloaded")
        except Exception as error:
            logging.error(error)
    else:
        print("Path to ArcoLinux Spices does not exist")


# install ArchLinux Tweak Tool
def install_archlinux_tweak_tool(self):
    base_dir = path.dirname(path.realpath(__file__))
    pathway = base_dir + "/packages/att/"
    file = listdir(pathway)

    try:
        command1 = "pacman -U " + pathway + str(file).strip("[]'") + " --noconfirm"
        logging.info("Applying this command: %s", command1)
        subprocess.run(
            command1.split(" "),
            shell=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )
        logging.info("ArchLinux Tweak Tool (ATT) is now installed")
    except Exception as error:
        logging.error(error)


# install ArcoLinux mirrorlist and key package
def install_arcolinux_key_mirror(self):
    base_dir = path.dirname(path.realpath(__file__))
    pathway = base_dir + "/packages/arcolinux-keyring/"
    file = listdir(pathway)

    try:
        command1 = "pacman -U " + pathway + str(file).strip("[]'") + " --noconfirm"
        logging.info("Applying this command: %s", command1)
        subprocess.run(
            command1.split(" "),
            shell=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )
        logging.info("ArcoLinux keyring is now installed")
    except Exception as error:
        logging.error(error)

    pathway = base_dir + "/packages/arcolinux-mirrorlist/"
    file = listdir(pathway)
    try:
        command2 = "pacman -U " + pathway + str(file).strip("[]'") + " --noconfirm"
        logging.info("Applying this command: %s", command2)
        subprocess.run(
            command2.split(" "),
            shell=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )
        logging.info("ArcoLinux mirrorlist is now installed")
    except Exception as error:
        logging.error(error)


# remove ArcoLinux mirrorlist and key package
def remove_arcolinux_key_mirror(self):
    try:
        command1 = "pacman -Rdd arcolinux-keyring --noconfirm"
        logging.info("Applying this command: %s", command1)
        subprocess.run(
            command1.split(" "),
            shell=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )
        logging.info("ArcoLinux keyring is now removed")
    except Exception as error:
        logging.error(error)

    try:
        command2 = "pacman -Rdd arcolinux-mirrorlist-git --noconfirm"
        logging.info("Applying this command: %s", command2)
        subprocess.run(
            command2.split(" "),
            shell=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )
        logging.info("ArcoLinux mirrorlist is now removed")
    except Exception as error:
        logging.error(error)


# Ensuring that pacman does not crash - installing/removing keys and mirrors
def pacman_safeguard():
    package = "arcolinux-mirrorlist-git"
    if not check_package_installed(package):
        logging.info("Removing the lines referring to the ArcoLinux repos")
        remove_repos()


# Running a script from the Application App
def run_script(self, command):
    logging.info("Running the following script: %s", command)
    try:
        subprocess.run(
            command, shell=False, stdout=subprocess.PIPE, stderr=subprocess.STDOUT
        )
    except Exception as error:
        logging.error(error)


# Running an Arch Linux command
def run_command(command):
    logging.info("Applying this command %s", command)
    try:
        subprocess.run(
            command.split(" "),
            shell=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )
    except Exception as error:
        logging.error(error)


# Running command in Alacritty with --hold option
def run_script_alacritty_hold(self, command):
    logging.info("Applying this command %s", command)
    try:
        subprocess.run(
            "alacritty --hold -e" + command,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )
    except Exception as error:
        logging.error(error)


# Running command in Alacritty without --hold option
def run_script_alacritty(self, command):
    self.logging.info("Applying this command %s", command)
    try:
        subprocess.run(
            "alacritty -e" + command,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )
    except Exception as error:
        self.logging.error(error)


# Remove directory
def remove_dir(self, directory):
    if path_check(directory):
        try:
            shutil.rmtree(directory)
        except Exception as error:
            logging.error(error)


# Change permissions
def permissions(dst):
    try:
        groups = subprocess.run(
            ["sh", "-c", "id " + sudo_username],
            check=True,
            shell=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )
        for x in groups.stdout.decode().split(" "):
            if "gid" in x:
                g = x.split("(")[1]
                group = g.replace(")", "").strip()
        subprocess.run(["chown", "-R", sudo_username + ":" + group, dst], shell=False)
    except Exception as error:
        logging.error(error)


# append repositories - anything not ArcoLinux
def append_repo(text):
    try:
        with open(pacman_conf, "a", encoding="utf-8") as f:
            f.write("\n\n")
            f.write(text)
    except Exception as error:
        logging.error(error)


# add repositories
def add_repos():
    if not repo_exist("[arcolinux_repo]"):
        if distr == "arcolinux":
            logging.info("Adding ArcoLinux repos on ArcoLinux")
            try:
                with open(pacman_conf, "r", encoding="utf-8") as f:
                    lines = f.readlines()
                    f.close()
            except Exception as error:
                logging.error(error)

            text = (
                "\n\n"
                + atestrepo
                + "\n\n"
                + arepo
                + "\n\n"
                + a3prepo
                + "\n\n"
                + axlrepo
                + "\n\n"
            )

            pos = get_position(lines, "#[testing]")
            lines.insert(pos - 2, text)

            try:
                with open(pacman_conf, "w", encoding="utf-8") as f:
                    f.writelines(lines)
            except Exception as error:
                logging.error(error)
        else:
            if not repo_exist("[arcolinux_repo_testing]"):
                logging.info("Adding ArcoLinux test repo (not used)")
                append_repo(atestrepo)
            if not repo_exist("[arcolinux_repo]"):
                logging.info("Adding ArcoLinux repo")
                append_repo(arepo)
            if not repo_exist("[arcolinux_repo_3party]"):
                logging.info("Adding ArcoLinux 3th party repo")
                append_repo(a3prepo)
            if not repo_exist("[arcolinux_repo_xlarge]"):
                logging.info("Adding ArcoLinux XL repo")
                append_repo(axlrepo)
            if repo_exist("[arcolinux_repo]"):
                logging.info("ArcoLinux repos have been installed")


# Removing repos
def remove_repos():
    try:
        with open(pacman_conf, "r", encoding="utf-8") as f:
            lines = f.readlines()
            f.close()

        if repo_exist("[arcolinux_repo_testing]"):
            pos = get_position(lines, "[arcolinux_repo_testing]")
            del lines[pos + 3]
            del lines[pos + 2]
            del lines[pos + 1]
            del lines[pos]

        if repo_exist("[arcolinux_repo]"):
            pos = get_position(lines, "[arcolinux_repo]")
            del lines[pos + 3]
            del lines[pos + 2]
            del lines[pos + 1]
            del lines[pos]

        if repo_exist("[arcolinux_repo_3party]"):
            pos = get_position(lines, "[arcolinux_repo_3party]")
            del lines[pos + 3]
            del lines[pos + 2]
            del lines[pos + 1]
            del lines[pos]

        if repo_exist("[arcolinux_repo_xlarge]"):
            pos = get_position(lines, "[arcolinux_repo_xlarge]")
            del lines[pos + 2]
            del lines[pos + 1]
            del lines[pos]

        with open(pacman_conf, "w", encoding="utf-8") as f:
            f.writelines(lines)
            f.close()

    except Exception as error:
        logging.error(error)


# Install packages from a path + filename
def install_packages_path(self, path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            lines = f.readlines()
            f.close()
    except Exception as error:
        logging.error(error)

    for line in lines:
        line = line.strip("\n")
        if not line.find("#") != -1:
            install_package(self, line)


# Show the in-app notification
def show_in_app_notification(self, message, err):
    if self.timeout_id is not None:
        GLib.source_remove(self.timeout_id)
        self.timeout_id = None
    self.statusbar.push(0, message)

    self.timeout_id = GLib.timeout_add(3000, timeOut, self)


# Timeout for the in-app message
def timeOut(self):
    close_in_app_notification(self)


# Do not show the in-app message
def close_in_app_notification(self):
    self.statusbar.pop(0)
    self.timeout_id = None


def run_as_user(script):
    subprocess.run(["su - " + sudo_username + " -c " + script], shell=False)
