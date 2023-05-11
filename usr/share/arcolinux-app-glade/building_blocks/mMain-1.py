#!/usr/bin/env python3

# Import gi
import gi
gi.require_version('Gtk','3.0')
from gi.repository import Gtk, Gdk

# Logging imports
import logging
import datetime

GUI_UI_FILE = "gGui.glade"

class Main:
    def __init__(self):
        logging.info('Building the Gui from the glade file')
        self.builder = Gtk.Builder()
        self.builder.add_from_file(GUI_UI_FILE)

        logging.info('Connecting the glad signals')
        self.builder.connect_signals(self)

        logging.info('create the main window')
        window = self.builder.get_object("hWindow")
        window.connect("delete-event", Gtk.main_quit)

        logging.info('Display main window')
        window.show()


    def on_cbIso_changed(self, widget):
        text = widget.get_active_text()
        if text is not None:
            logging.debug('Combobox Selction is: %s', text)


    def on_btnClickMe_clicked(self, widget):
        logging.warning('btnClickMe was clicked')

        

if __name__ == "__main__":
    now = datetime.datetime.now()

    handlers = [logging.FileHandler('ArcoLinux-App-' + now.strftime("%Y-%m-%d-%H:%M:%S") + ".log"),
                logging.StreamHandler()]

    logging.basicConfig(level = logging.DEBUG,
                        format = '%(asctime)s:%(levelname)s:%(message)s',
                        handlers = handlers)
    
    
    logging.info('Starting Application')
    main = Main()
    Gtk.main()