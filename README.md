# gvsig-desktop-scripting-addBasicTimeSupportToDatasource

This tool adds to a data source the information necessary for gvSIG to interpret the time values correctly and the data source can be used by the tools that wait for the data provider to provide this information.

The temporary information that is injected into the data source is the minimum necessary. This is:

* Time interval for which data is provided.
* Name of the attribute that contains the time information.
* Pattern used to recognize the date contained in the attribute.

The tool create a new virtual attribute with this information in the data source.

This tool is only able to handle times in date format. It can not work with sequences (seconds, minutes, hours, days ...).