Parcels API
===========

An API for exploring parcel data in Philadelphia.

Steps to setup on OpenShift
===========================

Install the OpenShift command-line client::

    gem install rhc

Create an OpenShift application (either through the web interface or with the
command line client).  Make it a Python 2.6 application, and add a PostgreSQL
gear.

Get the git repository URL for your application and add the remote to this
repository::

    git remote add openshift ssh://<git repo address>/

Push the code up to the application::

    git push openshift

Your first push will take a long time, because it runs the 
*.openshift/action_hooks/build* script which downloads and installs Proj4, 
GEOS, and GDAL.  These take foooorreeeevverrrrr.  However, the build script
should only have to install them once.

Now, once the deploy has finished, log in to the server and run the following:

    cd $OPENSHIFT_REPO_DIR
    src/manage.py loadparcels <shapefile-URL> <path-to-shape-data>

If you want to use Philadelphia's data from January 2012, then you don't have
to provide any arguments to ``loadparcels``.  By default, it will download the
Philadelphia parcel shape file from the Pennsylvania Spacial Data Access 
(`PASDA <http://www.pasda.psu.edu/uci/MetadataDisplay.aspx?entry=PASDA&file=PhiladelphiaParcels201201.xml&dataset=462>`_)
site.  If you want to use other data, run ``src/manage.py help loadparcels`` 
to see more information on your options.

