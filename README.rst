====================================
ZenPacks.ssv.InstalledSoftwareReport
====================================


Description
===========
This ZenPack was originally written by Serge Sergeev; see https://github.com/sergevs/ZenPacks.ssv.InstalledSoftwareReport and https://github.com/sergevs/ZenPacks.ssv.InstalledSoftwareReport/wiki .

It provides reports for software installed on devices, with installed date (assuming that software
has been collected by an appropriate modeler).  Fundamentally, it cycles through a device's os.software 
relationship in the ZODB database.

Filtering criteria are offered to select devices based on device class, Group, System, Location and 
partial device id match.  The software package can also be filtered with a partial match (which 
is case sensitive); the package must start with this filter.

The only function this ZenPack provides is the single report, Installed Software,  found under 
REPORT -> Device Reports.

Requirements & Dependencies
===========================

* Zenoss Versions Supported:  3.x, 4.x, 5.x (see no reason why it shouldn't run on 6.x)
* External Dependencies:  None
* ZenPack Dependencies:   None


Download
========
Download the appropriate package for your Zenoss version from the list
below.

* Zenoss 4.0+ `Latest Package for Python 2.7`_

ZenPack installation
======================

This ZenPack can be installed from the .egg file using either the GUI or the
zenpack command line. 

To install the egg, use::
  zenpack --install ZenPacks.ssv.InstalledSoftwareReport-1.1-py2.7.egg

Or on a Zenoss 5 / 6 to install the egg::
  serviced service run zope zenpack-manager install ZenPacks.ssv.InstalledSoftwareReport-1.1-py2.7.egg


To install in development mode, find the repository on github and use the *Download ZIP* button
(right-hand margin) to download a tgz file and unpack it to a local directory, say,
/code/ZenPacks .  Install from /code/ZenPacks with::
  zenpack --link --install ZenPacks.ssv.InstalledSoftwareReport
  Restart zenoss after installation.

After installation, zenhub and zopectl (zenwebserver on RM), will need restarting on Zenoss 4; the zenhub and zope services will need restarting on Zenoss 5+ .


Limitations and Troubleshooting
===============================

The export button does not work.



Change History
==============
* 1.0.0
   - Initial Release by Serge Sergeev
* 1.1
   - Updated by Jane Curry to add:

     - Titles for the individual device reports
     - Ability to search on partial device match
     - Tested on Zenoss 4.2.5 SUP732 and Zenoss 5.2.1  

Screenshots
===========

See the screenshots directory.


.. External References Below. Nothing Below This Line Should Be Rendered

.. _Latest Package for Python 2.7: https://github.com/jcurry/ZenPacks.community.simple1/blob/master/dist/ZenPacks.community.simple1-1.0.0-py2.7.egg?raw=true

Acknowledgements
================

Thanks to Serge for this really useful and elegant ZenPack.

