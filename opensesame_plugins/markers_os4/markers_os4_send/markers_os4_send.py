# -*- coding:utf-8 -*-

"""
OpenSesame 4 plugin for sending markers to Leiden Univ Marker device.
"""

from libopensesame.py3compat import *
from libopensesame.item import Item
from libqtopensesame.items.qtautoplugin import QtAutoPlugin
from libopensesame.exceptions import osexception
import sys
import re
import time

class MarkersOs4Send(Item):
    """
    This class handles the basic functionality of the item.
    """

    description = 'Sends marker to Leiden Univ marker device - Markers plugin for OpenSesame 4'

    def reset(self):

        """
        desc:
            Resets plug-in to initial values.
        """
        self.var.marker_device_tag = u'marker_device_1'
        self.var.marker_value = 0
        self.var.marker_object_duration = 0
        self.var.marker_reset_to_zero = 'no'

    def get_tag_gui(self):
        return self.var.marker_device_tag

    def get_value_gui(self):
        return self.var.marker_value
    
    def get_duration_gui(self):
        return self.var.marker_object_duration
    
    def get_reset_to_zero_gui(self):
        return self.var.marker_reset_to_zero == u'yes'    

    def is_already_init(self):
        if (hasattr(self.experiment.python_workspace, "marker_managers") and 
            self.get_tag_gui() in self.experiment.python_workspace.marker_managers):
            return True
        else:
            return False

    def get_marker_manager(self):
        if self.is_already_init():
            return self.experiment.python_workspace.marker_managers.get(self.get_tag_gui())
        else:
            return None


    def prepare(self):

        """
        desc:
            Prepare phase.
        """

        # Check input of plugin (only tag and duration, the value is checked by marker_manager):
        device_tag = self.get_tag_gui()
        if not(bool(re.match("^[A-Za-z0-9_-]*$", device_tag)) and bool(re.match("^[A-Za-z]*$", device_tag[0]))):
            raise osexception("Device tag can only contain letters, numbers, underscores and dashes "
                              "and should start with a letter.")
        
        if not(isinstance(self.get_duration_gui(), int) and not(isinstance(self.get_duration_gui(), float))):
            raise osexception("Object duration should be numeric")
        elif self.get_duration_gui() < 0:
            raise osexception("Object duration must be a positive number")

        # Call the parent constructor
        Item.prepare(self)

    def run(self):

        """
        desc:
            Run phase.
        """

        # Check if the marker device is initialized
        if not self.is_already_init():
            raise osexception("You must have a markers_os4_init item before sending markers."
                              " Make sure the Device tags match.")

        # Send marker
        try:
            self.get_marker_manager().set_value(int(self.get_value_gui()))
        except:
            raise osexception(f"Error sending marker with value {self.get_value_gui()}: {sys.exc_info()[1]}")

        # Sleep for object duration (blocking)
        self.clock.sleep(int(self.get_duration_gui()))

        # Reset marker value to zero, if specified
        if self.get_reset_to_zero_gui():
            try:
                self.get_marker_manager().set_value(0)
            except:
                raise osexception(f"Error sending marker with value 0: {sys.exc_info()[1]}")
            
        self.set_item_onset()
        

class qtmarkers_os4_send(MarkersOs4Send, QtAutoPlugin):
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

        # Call the parent constructors.
        MarkersOs4Send.__init__(self, name, experiment, script)
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
        