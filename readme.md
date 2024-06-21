# Plugin for OpenSesame for sending markers
This is an OpenSesame plugin for sending markers with Leiden University devices. This plugin uses the marker_management module from the python markers repo: https://github.com/solo-fsw/python-markers

> **Note**
> TThis plugin is only available for OpenSesame 4. The markers plugin for OpenSesame 3 can be found here: https://github.com/>  solo-fsw/opensesame3_plugin_markers
> 
> **Note**
> This plugin is only available for Windows. 

## Installation
How the markers package can best be installed depends on the OpenSesame installation and whether it is installed system-wide (available for all users of the pc, usually through the Start menu), or whether it is installed in a Conda environment.

### OpenSesame system installation
When using a system-wide installation of OpenSesame, the plugin can be installed in the Users folder `C:\Users\%USERNAME%\AppData\Roaming\Python\Python311\site-packages`. When different users need to use the plugin on one computer, they must all install the plugin separately.

- Make sure Git is installed.

- Open the system installation of OpenSesame (e.g. from the Start menu). 

- In OpenSesame, run from the Console:

    `!pip install --user git+https://github.com/solo-fsw/opensesame4_plugin_markers`

- Restart OpenSesame. 

- The Markers items should now be visible in the Items Toolbar:

    ![markers_init](/opensesame_plugins/markers_os4/markers_os4_init/markers_os4_init_large.png)
    ![markers_send](/opensesame_plugins/markers_os4/markers_os4_send/markers_os4_send_large.png)

### OpenSesame in Conda environment
When using OpenSesame that was installed in a Conda environment, the plugin should be installed in that environment. When you use different environments, the plugin needs to be installed in each of the environments. 

- Make sure Git is installed.

- Start OpenSesame in the Conda environment.

- In OpenSesame, run from the Console:

     `!pip install git+https://github.com/solo-fsw/opensesame4_plugin_markers`

- Restart OpenSesame. 

- The Markers items should now be visible in the Items Toolbar:

    ![markers_init](/opensesame_plugins/markers_os4/markers_os4_init/markers_os4_init_large.png)
    ![markers_send](/opensesame_plugins/markers_os4/markers_os4_send/markers_os4_send_large.png)

## How to use
Help and instructions on how to use the plugin can be found [here](/opensesame_plugins/markers_os4/markers_os4_init/markers_os4_init.md) and in OpenSesame it can be found after inserting a markers item in your experiment by clicking on the blue questionmark in the upper right corner of the markers item tab. ![image](https://user-images.githubusercontent.com/56065641/217841460-634aee68-7b98-4154-8275-ac75337788e7.png).

In the samples folder a sample task can be found, which can also be downloaded [here](https://downgit.github.io/#/home?url=https://github.com/solo-fsw/opensesame4_plugin_markers/tree/main/samples) (download starts immediately using DownGit).

## Timing
The timing of the plugin was tested by comparing the onset of a pulse sent with the plugin to the UsbParMarker with the onset of a pulse sent to the LPT port (the original way of sending markers). Both signals were recorded with BIOPAC in AcqKnowledge. An average difference of 179 us (range 120 us - 260 us) was found when sending a pulse first to the LPT port, then to the UsbParMarker and an average difference of 281 us (range 160 us - 440 us) was found when sending a pulse first to the UsbParMarker, then to the LPT port (20 trials each). See the timing_test folder for the experiment used and the AcqKnowledge data files. Additionally, the duration of the markers_send object was measured, with and average duration of 337 us (range 292 us - 382 us), measured over 20 trials. Note that the experiment used the PyschoPy backend (default) and was performed on a standerd FSW Leiden lab pc. Timing can probably be improved by using a different backend or using a different pc.

## References
- [SOLO wiki on markers](https://researchwiki.solo.universiteitleiden.nl/xwiki/wiki/researchwiki.solo.universiteitleiden.nl/view/Hardware/Markers%20and%20Events/)
- [Python markers github page](https://github.com/solo-fsw/python-markers)
- [OpenSesame 3 Markers plugin](https://github.com/solo-fsw/opensesame3_plugin_markers)
- [SOLO wiki on the UsbParMarker](https://researchwiki.solo.universiteitleiden.nl/xwiki/wiki/researchwiki.solo.universiteitleiden.nl/view/Hardware/Markers%20and%20Events/UsbParMarker/)
- [SOLO wiki on Eva](https://researchwiki.solo.universiteitleiden.nl/xwiki/wiki/researchwiki.solo.universiteitleiden.nl/view/Hardware/Markers%20and%20Events/EVA/)
- [UsbParMarker github page](https://github.com/solo-fsw/UsbParMarker)
- [Eva github page](https://github.com/solo-fsw/Eva)


