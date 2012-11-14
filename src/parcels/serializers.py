import json
from rest_framework import serializers
from django.contrib.gis import geos
from parcels import models


class GeoJSONField (serializers.Field):
    def to_native(self, obj):
        """
        Convert the geometry to a string.  Note that this will produce a string
        of JSON, not a dictionary.
        """
        return obj.json
    
    def from_native(self, data):
        """
        Assume that data is a string that GEOS knows how to deal with.  See
        https://docs.djangoproject.com/en/dev/ref/contrib/gis/geos/#creating-a-geometry
        """
        return geos.GEOSGeometry(data)


class ParcelSerializer (serializers.ModelSerializer):
    shape = GeoJSONField()
    
    class Meta:
        model = models.Parcel
        
