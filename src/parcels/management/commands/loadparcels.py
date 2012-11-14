from django.core.management.base import BaseCommand, CommandError
import django
from optparse import make_option
import os
import sys

from parcels.loader import ParcelFileLoader

class Command(BaseCommand):
    help = "Load the parcel data from a shape file."
    option_list = BaseCommand.option_list + (
        make_option('--shapefile',
            dest='shapefile',
            default='http://www.pasda.psu.edu/philacity/data/PhiladelphiaParcels201201.zip',
            help='The source shape file from which to load.  Can either be a local file path or an HTTP URL.'),
        make_option('--datapath',
            dest='datapath',
            default='Philadelphia Parcels/PhiladelphiaParcels201201.shp',
            help='The path within the shapefile to the geometry data file.'),
        )

    def handle(self, *args, **options):
        loader = ParcelFileLoader()
        shapefile = options['shapefile']
        datapath = options['datapath']
        if shapefile.startswith('http:') or shapefile.startswith('https:'):
            loader.load_from_url(shapefile, datapath)
        else:
            loader.load_from_zipfile(shapefile, datapath)
