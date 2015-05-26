import Globals
from Globals import InitializeClass
from AccessControl import ClassSecurityInfo
from Products.ZenReports import Utils
from Products.ZenModel.ZenModelItem import ZenModelItem

import re
import logging
log = logging.getLogger("zen.Reports")

class Installed:

  def __init__(self, device, software):
    self.hostname = device.titleOrId
    self.devclass = device.devclass
    self.system = device.system
    self.group = device.group
    self.location = device.location
    self.software = software.id


class RDevice:
  security = ClassSecurityInfo()
  security.setDefaultAccess('allow')

  def __init__(self, device, reFilter):
    self.titleOrId=device.titleOrId()
    self.filteredSoftware = [e for e in device.os.software() if reFilter.match(e.id)]
    self.software = None
    self.kernel = device.getOSProductName().replace('Linux ','')
    self.collected = device.getSnmpLastCollectionString()
    self.deviceLink = device.getDeviceLink()
    self.devclass = device.getDeviceClassName()
    self.system = '|'.join(device.getSystemNames())
    self.group = '|'.join(device.getDeviceGroupNames())
    self.location = device.getLocationName()

#    def titleOrId(self): return self.t 
#    def kernel(self): return self.kernel 

InitializeClass(RDevice)

class ExportInstalledSoftware:
  """
  ExportInstalled Software report
  """

  def filteredDevices(self, dmd, args):
    deviceClass = args.get('deviceClass', '/') or '/' 
    deviceGroup = args.get('deviceGroup', '/') or '/' 
    deviceSystem = args.get('deviceSystem', '/') or '/' 
    deviceLocation = args.get('deviceLocation', '/') or '/' 
    packagesFilter = args.get('packagesFilter', '') or '' 
    matchedSoftware = args.get('matchedSoftware','') or ''

    reFilter=re.compile(packagesFilter)

    for d in dmd.Devices.getOrganizer(deviceClass).getSubDevices(): 
      if not d.monitorDevice(): continue 
      dGroups = d.getDeviceGroupNames();
      if len(dGroups) == 0: dGroups.append('/')
      groupMatched = False
      for i in dGroups:
        if re.match(deviceGroup,i): 
          groupMatched = True
          break
      dSystems = d.getSystemNames();
      if len(dSystems) == 0: dSystems.append('/')
      systemMatched = False
      for i in dSystems:
        if re.match(deviceSystem,i):
          systemMatched = True
          break
      locationMatched = False
      dLocation = d.getLocationName();
      if len(dLocation) == 0: dLocation='/'
      if re.match(deviceLocation,dLocation): locationMatched = True
      if groupMatched and systemMatched and locationMatched: 
        devForReport = RDevice(d,reFilter) 
        if matchedSoftware == 'on' and len(devForReport.filteredSoftware) < 1 : continue  
        yield devForReport

  def run(self, dmd, args):
    """
    Generate the report using custom filter
    """

    report = []
#    log.info('invoking InstalledSoftware report')
    # Filter the device list down according to the
    # values from the filter widget
    for device in self.filteredDevices(dmd, args):
      for software in device.filteredSoftware:
        #yield Utils.Record(hostname=device.titleOrId, softId=software.id)
        yield Installed(device, software)
