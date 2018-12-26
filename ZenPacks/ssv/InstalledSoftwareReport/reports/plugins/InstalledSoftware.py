import Globals
from Globals import InitializeClass
from AccessControl import ClassSecurityInfo
from Products.ZenReports import Utils

import re
import logging
log = logging.getLogger("zen.Reports")

class RDevice:
  security = ClassSecurityInfo()
  security.setDefaultAccess('allow')

  def __init__(self, device, reFilter):
    self.titleOrId=device.titleOrId()
    self.filteredSoftware = [e for e in device.os.software() if reFilter.match(e.id)]
    self.kernel = device.getOSProductName().replace('Linux ','')
    self.collected = device.getSnmpLastCollectionString()
    self.deviceLink = device.getDeviceLink()

#    def titleOrId(self): return self.t 
#    def kernel(self): return self.kernel 

InitializeClass(RDevice)

class InstalledSoftware:
  """
  Installed Software report
  """

  def filteredDevices(self, dmd, args):
    deviceBox = args.get('deviceBox', '') or '' 
    deviceClass = args.get('deviceClass', '/') or '/' 
    deviceGroup = args.get('deviceGroup', '/') or '/' 
    deviceSystem = args.get('deviceSystem', '/') or '/' 
    deviceLocation = args.get('deviceLocation', '/') or '/' 
    packagesFilter = args.get('packagesFilter', '') or '' 
    matchedSoftware = args.get('matchedSoftware','') or ''

    reFilter=re.compile(packagesFilter)

    # Check for device match first
    #d = dmd.Devices.findDeviceByIdOrIp(deviceBox)
    #d = dmd.Devices.findDeviceByIdExact(deviceBox)
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
        # Now check the device name
        if deviceBox: 
            if d.titleOrId().find(deviceBox) != -1:
              devForReport = RDevice(d,reFilter) 
              if matchedSoftware == 'on' and len(devForReport.filteredSoftware) < 1 : continue  
              yield devForReport
        else:
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
      yield Utils.Record( device=device )
