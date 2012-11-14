Parcels API
===========

An API for exploring parcel data in Philadelphia.

Steps to Reproduce
==================

These steps assume that you have the dependencies for GeoDjango correctly 
installed and configured.

First, get the data.  This process is based on that described in the GeoDjango
documentation at https://docs.djangoproject.com/en/dev/ref/contrib/gis/tutorial/#geographic-data
* Download the Philadelphia parcel shape file zip archive data from Pennsylvania Spacial Data Access (`PASDA <http://www.pasda.psu.edu/uci/MetadataDisplay.aspx?entry=PASDA&file=PhiladelphiaParcels201201.xml&dataset=462>`_).
* Create a folder named *data* and unzip the archive into it.
* 

::

    mkdir data
    cd data
    cp <PATH_TO_DOWNLOADED_ZIP> .
    unzip <PARCEL_FILE>


