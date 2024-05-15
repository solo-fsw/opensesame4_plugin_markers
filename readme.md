# Plugin for OpenSesame for sending markers
This is an OpenSesame plugin for sending markers with Leiden University devices. This plugin uses the marker_management module from the python markers repo: https://github.com/solo-fsw/python-markers

> **Note**
> - This plugin is only available for OpenSesame 4. The markers plugin for OpenSesame 3 can be found here: https://github.com/solo-fsw/opensesame3_plugin_markers
> - This plugin is only available for Windows. 

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

### OpenSesame through Conda environment

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

## References
- [SOLO wiki on markers](https://researchwiki.solo.universiteitleiden.nl/xwiki/wiki/researchwiki.solo.universiteitleiden.nl/view/Hardware/Markers%20and%20Events/)
- [Python markers github page](https://github.com/solo-fsw/python-markers)
- [OpenSesame 3 Markers plugin](https://github.com/solo-fsw/opensesame3_plugin_markers)
- [SOLO wiki on the UsbParMarker](https://researchwiki.solo.universiteitleiden.nl/xwiki/wiki/researchwiki.solo.universiteitleiden.nl/view/Hardware/Markers%20and%20Events/UsbParMarker/)
- [SOLO wiki on Eva](https://researchwiki.solo.universiteitleiden.nl/xwiki/wiki/researchwiki.solo.universiteitleiden.nl/view/Hardware/Markers%20and%20Events/EVA/)
- [UsbParMarker github page](https://github.com/solo-fsw/UsbParMarker)
- [Eva github page](https://github.com/solo-fsw/Eva)


