#!/usr/bin/env python3

# Importing gi
import gi
# https://docs.gtk.org/gtk3/
gi.require_version('Gtk','3.0')
# https://docs.gtk.org/gdk3/
from gi.repository import Gtk, Gdk

# https://docs.python.org/3/howto/logging.html (debug,info,warning,error,critical)
import logging
# https://docs.python.org/3/library/datetime.html
import datetime

# https://docs.python.org/3/tutorial/classes.html
# https://realpython.com/python-main-function/
class Main:
    def __init__(self):
        logging.info('Building the Gui from the glade file')
        # https://python-gtk-3-tutorial.readthedocs.io/en/latest/builder.html
        self.builder = Gtk.Builder()
        self.builder.add_from_file("gGui.glade")

        logging.info('Connecting the glade signals')
        self.builder.connect_signals(self)

        logging.info('Create the main window')
        window = self.builder.get_object("hWindow")
        window.connect("delete-event", Gtk.main_quit)

        logging.info('Display the main window')
        window.show()


    def on_cb_iso_changed(self, widget):
        text = widget.get_active_text()
        if text is not None:
            logging.debug('Combobox Selection is: %s', text)


    def on_btn_click_me_clicked(self, widget):
        logging.warning('Button click me was clicked')

    def on_btn_grid_clicked(self, widget):
        logging.warning('Button grid was clicked')
        

if __name__ == "__main__":
    # find date and time 
    now = datetime.datetime.now()

    # defining handlers for terminal and log file
    handlers = [logging.FileHandler('ArcoLinux-App-' + now.strftime("%Y-%m-%d-%H:%M:%S") + ".log"),
                logging.StreamHandler()]

    # basic configuration
    # https://docs.python.org/3/howto/logging.html (debug,info,warning,error,critical)
    logging.basicConfig(level = logging.DEBUG,
                        format = '%(asctime)s:%(levelname)s:%(message)s', datefmt='%Y/%m/%d %H:%M:%S',
                        handlers = handlers)
    
    
    logging.info('Starting ArcoLinux Application')
    main = Main()
    Gtk.main()
