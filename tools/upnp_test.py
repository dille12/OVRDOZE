import upnpy

upnp = upnpy.UPnP()
devices = upnp.discover()
print(devices)
