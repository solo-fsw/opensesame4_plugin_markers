# -*- coding:utf-8 -*-

"""
OpenSesame plugin for initializing a Leiden Univ Marker device.
"""

from operator import truediv
from libopensesame.py3compat import *
from libopensesame.item import Item
from libqtopensesame.items.qtautoplugin import QtAutoPlugin
from libopensesame.exceptions import osexception
import serial
import sys
import re
import os
import pandas

from python_markers import marker_management as mark


class MarkersInit(Item):
    """
    This class handles the basic functionality of the item.
    """

    description = 'Initializes Leiden Univ marker device - Markers plugin for OpenSesame 4'

    def reset(self):
        """
        desc:
            Resets plug-in to initial values.
        """
        self.var.marker_device_tag = u'marker_device_1'
        self.var.marker_device = u'ANY'
        self.var.marker_device_addr = u'ANY'
        self.var.marker_device_serial = u'ANY'

        self.var.marker_crash_on_mark_errors = u'yes'
        self.var.marker_dummy_mode = u'no'
        self.var.marker_gen_mark_file = u'yes'
        self.var.marker_flash_255 = u'no'

    def get_device_gui(self):
        if self.var.marker_device == u'UsbParMarker':
            device = 'UsbParMarker'
        elif self.var.marker_device == u'Eva':
            device = 'Eva'
        elif self.var.marker_device == u'ANY':
            device = 'ANY'
        else:
            raise osexception(u'INTERNAL ERROR')
        return device

    def get_addr_gui(self):
        return self.var.marker_device_addr

    def get_serial_gui(self):
        return self.var.marker_device_serial

    def get_tag_gui(self):
        return self.var.marker_device_tag

    def get_dummy_mode_gui(self):
        return self.var.marker_dummy_mode == u'yes'

    def get_crash_on_mark_error_gui(self):
        return self.var.marker_crash_on_mark_errors == u'yes'
    


    def is_already_init(self):
        if (hasattr(self.experiment, "marker_managers") and 
            self.get_tag_gui() in self.experiment.marker_managers):
            return True
        else:
            return False
        
    def set_marker_manager(self, mark_man):

        if not hasattr(self.experiment, "marker_managers"):
            self.experiment.marker_managers = dict()

        self.experiment.marker_managers[self.get_tag_gui()] = mark_man

    def get_marker_manager(self):
        if self.is_already_init():
            return self.experiment.marker_managers.get(self.get_tag_gui())
        else:
            return None
        
    def set_marker_manager_tag(self):

        if not 'markers_tags' in self.experiment.python_workspace:
            self.experiment.python_workspace['markers_tags'] = list()

        self.experiment.python_workspace['markers_tags'].append(self.get_tag_gui())

    def set_marker_prop_var(self, marker_prop):
        # Save in var and in python_workspace
        print(marker_prop)
        for prop in marker_prop:
            setattr(self.experiment.var, f"markers_{prop}_{self.get_tag_gui()}", marker_prop[prop])

        self.experiment.python_workspace[f'markers_prop_{self.get_tag_gui()}'] = marker_prop

    def get_marker_prop_var(self, prop):
        try:
            return getattr(self.experiment.var, f"markers_{prop}_{self.get_tag_gui()}")
        except:
            return None
    
    def set_marker_tables(self, marker_table, summary_table, error_table):
        self.experiment.python_workspace[f'markers_marker_table_{self.get_tag_gui()}'] = marker_table
        self.experiment.python_workspace[f'markers_summary_table_{self.get_tag_gui()}'] = summary_table
        self.experiment.python_workspace[f'markers_error_table_{self.get_tag_gui()}'] = error_table


    def prepare(self):

        """
        desc:
            Prepare phase.
        """

        # Check input of plugin:
        device_tag = self.get_tag_gui()
        if not(bool(re.match("^[A-Za-z0-9_-]*$", device_tag)) and bool(re.match("^[A-Za-z]*$", device_tag[0]))):
            # Raise error, tag can only contain: letters, numbers, underscores and dashes and should start with letter.
            raise osexception(f"Incorrect device tag: {device_tag}. "
                              "Device tag can only contain letters, numbers, underscores and dashes "
                              "and should start with a letter.")

        device_address = self.get_addr_gui()
        if device_address != u'ANY' and re.match("^COM\d{1,3}", str(device_address)) is None:
            # Raise error when marker address is not a proper COM address.
            raise osexception(f"Incorrect marker device address: {device_address}")

        # Get com port and device info:
        info = self.resolve_com_port()

        # Save com port in device and save all device info
        info['device']['ComPort'] = info['com_port']
        self.set_marker_prop_var(info['device'])


        # Call the parent constructor
        Item.prepare(self)

    def run(self):

        """
        desc:
            Run phase.
        """

        # Save marker_manager tag
        self.set_marker_manager_tag()

        device = self.get_marker_prop_var('Device')
        com_port = self.get_marker_prop_var('ComPort')

        if self.is_already_init():
            # Raise error since you cannot init twice.
            raise osexception("Marker device already initialized.")


        # Build marker manager:
        marker_manager = mark.MarkerManager(device_type=device,
                                            device_address=com_port,
                                            crash_on_marker_errors=self.get_crash_on_mark_error_gui(),
                                            time_function_ms=lambda: self.clock.time())
        self.set_marker_manager(marker_manager)

        # Flash 255
        pulse_dur = 100
        if self.var.marker_flash_255 == 'yes':
            marker_manager.set_value(255)
            self.clock.sleep(pulse_dur)
            marker_manager.set_value(0)
            self.clock.sleep(pulse_dur)
            marker_manager.set_value(255)
            self.clock.sleep(pulse_dur)

        # Reset:
        marker_manager.set_value(0)
        self.clock.sleep(pulse_dur)

        # Add cleanup function:
        self.experiment.cleanup_functions.append(self.cleanup)

        self.set_item_onset()


    def cleanup(self):

        # Reset value:
        self.get_marker_manager().set_value(0)
        self.clock.sleep(100)

        # Generate and save marker file in same location as the logfile
        if self.var.marker_gen_mark_file == u'yes':
            log_location = os.path.dirname(os.path.abspath(self.experiment.logfile))
            try:
                full_filename = 'subject-' + str(self.experiment.var.subject_nr) + '_' + self.get_tag_gui() + '_marker_table'
                self.get_marker_manager().save_marker_table(filename=full_filename,
                                                            location=log_location,
                                                            more_info={'Device tag': self.get_tag_gui(),
                                                                    'Subject': self.experiment.var.subject_nr})
            except:
                print("WARNING: Could not save marker file.")


        # Close marker device:
        self.close()

        # Get marker tables and save
        marker_df, summary_df, error_df = self.get_marker_manager().gen_marker_table()
        self.set_marker_tables(marker_df, summary_df, error_df)

    def close(self):

        """
        desc:
            Closes the serial connection.
        """

        try:
            self.get_marker_manager().close()
            print("Disconnected from marker device.")
        except:
            pass

    def resolve_com_port(self):

        """
        desc:
            Resolves which com port the marker device is connected to.
        """        

        if self.get_device_gui() == 'ANY':
            device_type = ''
        else:
            device_type = self.get_device_gui()

        if self.get_addr_gui() == 'ANY':
            addr = ''
        else:
            addr = self.get_addr_gui()

        if self.get_serial_gui() == 'ANY':
            serialno = ''
        else:
            serialno = self.get_serial_gui()

        if self.get_dummy_mode_gui():
            device_info = {}
            device_info['device'] = {
                "Version": "0000000",
                "Serialno": "0000000",
                'Device':'FAKE DEVICE'}
            device_info['com_port'] = 'FAKE'

        else:
            # Find device
            try:
                device_info = mark.find_device(device_type=device_type,
                                            serial_no=serialno,
                                            com_port=addr,
                                            fallback_to_fake=False)
            except:
                raise osexception(f"Marker device init error: {sys.exc_info()[1]}")

        return device_info


class qtmarkers_init(MarkersInit, QtAutoPlugin):
    """
    This class handles the GUI aspect of the plug-in. By using qtautoplugin, we
    usually need to do hardly anything, because the GUI is defined in info.json.
    """

    def __init__(self, name, experiment, script=None):

        """
        Constructor.

        Arguments:
        name		--	The name of the plug-in.
        experiment	--	The experiment object.

        Keyword arguments:
        script		--	A definition script. (default=None)
        """

        # We don't need to do anything here, except call the parent
        # constructors.
        MarkersInit.__init__(self, name, experiment, script)
        QtAutoPlugin.__init__(self, __file__)

    def init_edit_widget(self):

        """
        Constructs the GUI controls. Usually, you can omit this function
        altogether, but if you want to implement more advanced functionality,
        such as controls that are grayed out under certain conditions, you need
        to implement this here.
        """

        # First, call the parent constructor, which constructs the GUI controls
        # based on info.json.
        QtAutoPlugin.init_edit_widget(self)
        self.custom_interactions()

    def apply_edit_changes(self):

        """
        desc:
            Applies the controls.
        """

        if not QtAutoPlugin.apply_edit_changes(self) or self.lock:
            return False
        self.custom_interactions()

    def edit_widget(self):

        """
        Refreshes the controls.

        Returns:
        The QWidget containing the controls
        """

        if self.lock:
            return
        self.lock = True
        w = QtAutoPlugin.edit_widget(self)
        self.custom_interactions()
        self.lock = False
        return w

    def custom_interactions(self):

        """
        desc:
            Activates the relevant controls for each setting.
        """
