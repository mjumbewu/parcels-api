from __future__ import division

# From within a manage.py shell, run::
#
#   from parcels.loader import ParcelFileLoader
#   loader = ParcelFileLoader()
#   loader.load_data()

import os
import tempfile
import zipfile
from django.contrib.gis.gdal import DataSource
from django.contrib.gis.gdal.error import OGRException
from urllib2 import urlopen
import logging
from models import Parcel

logger = logging.getLogger(__name__)
logger.setLevel('DEBUG')

class ParcelFileLoader:
    """
    Load a parcel shapefile into the database.
    """
    
    # url = 'http://www.pasda.psu.edu/philacity/data/PhiladelphiaParcels201201.zip'
#    rel_shp = '../../data/Philadelphia Parcels/PhiladelphiaParcels201201.shp'
#    shp = os.path.abspath(os.path.join(os.path.dirname(__file__), rel_shp))
    
    def get_field_mapping(self, layer):
        self.mapping = dict([
            (field.lower(), field)
            for field in layer.fields
        ])
        return self.mapping

    def get_data_source(self, sourcename):
        self.ds = DataSource(sourcename)
        return self.ds
    
    def get_parcel_layer(self, ds):
        assert(len(ds) == 1)
        self.layer = ds[0]
        return self.layer

    def load_from_url(self, shpfileurl, shpdatafilename):
        outfile, shpfilename = tempfile.mkstemp()
        os.close(outfile)

        with open(shpfilename, 'w') as outfile:
            shpfile = urlopen(shpfileurl)
            totalbytes = int(shpfile.info().getheader('content-length'))
            print 'Downloading the shapefile (%.2f MB)' % (totalbytes / 1024 / 1024)
            print '  from ' + shpfileurl
            print '  into ' + shpfilename
            
            bytesread = 0
            print '  0.0% Complete',
            while shpfile:
                data = shpfile.read(1024)
                outfile.write(data)
                bytesread += len(data)
                print '\r  %.1f%% Complete' % (bytesread * 100 / totalbytes),
            print 'Done'
        
        self.load_from_zipfile(shpfilename, shpdatafilename)
    
    def load_from_zipfile(self, shpfilename, shpdatafilename):
        tmpdir = tempfile.mkdtemp()
        with zipfile.ZipFile(shpfilename) as shpfile:
            print 'Extracting the shapefile to ' + tmpdir
            shpfile.extractall(tmpdir)
        self.load_data(os.path.join(tmpdir, shpdatafilename))
        
    def load_data(self, shpdatafilename):
        ds = self.get_data_source(shpdatafilename)
        layer = self.get_parcel_layer(ds)
        mapping = self.get_field_mapping(layer)
        mapping_items = mapping.items()
        
        self.parcels = []
        self.count = 0
        total = 0
        
        for feature in layer:
            total += 1
            self.count += 1

            parcel_args = {
                field: feature[orig_field].value
                for field, orig_field in mapping_items
            }
            
            try:
                parcel_args['shape'] = feature.geom.transform(4326, clone=True).wkt
            except OGRException:
                print '  ...skipping because of OGR exception.'
                continue
            
            print('{0}: Loaded data for {house} {stnam} into memory'.format(
                total, **parcel_args))
            
            parcel = Parcel(**parcel_args)
            self.parcels.append(parcel)
            
            if self.count >= 25000:
                print('Flushing...')
                self.flush_loaded_parcels()
    
    def flush_loaded_parcels(self):
        Parcel.objects.bulk_create(self.parcels)
        self.parcels = []
        self.count = 0


if __name__ == '__main__':
    loader = ParcelFileLoader()
    loader.load_from_url('http://www.pasda.psu.edu/philacity/data/PhiladelphiaParcels201201.zip', 'Philadelphia Parcels/PhiladelphiaParcels201201.shp')
