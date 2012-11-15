from rest_framework import generics, exceptions, renderers
from django.contrib.gis import geos
from parcels import models, serializers

class ParcelList (generics.ListAPIView):
    """
    An index of the parcels.  The parcel listings are paginated with 20 parcels
    to a page by default.  This can be controlled with the `perpage` query 
    parameter.  The `page` parameter allows you to step through the pages of
    parcels.
    
    Filters
    -------
    
    The parcel listing supports the following filters:
    
    * `near`: 
      
        A comma-separeted pair of decimal numbers representing latitude and
        longitude of a reference point in degrees. Results in the parcel list
        being ordered by distance from the point.
        
            /parcels/?near=39.9489,-75.2190
            
        It is **highly recommended** that you only use a `near` query in
        conjunction with some bounds-restricting query, such as `intersecting`.
        Otherwise, the database will sort the entire parcel table by distance,
        which would be very expensive and slow.

    * `intersecting`:
      
        Either:
        
        * Four comma-separated decimal numbers representing the bounds of a box
          (lat1,lng1,lat2,lng2), or
        * A WKT string representing a POLYGON, or
        * A GeoJSON string representing a POLYGON
        
        For example:
        
            /parcels/?near=39.9488,-75.2190&intersecting=39.9463,-75.2244,39.9514,-75.2135
    
    Query parameters
    ----------------
    
    * `perpage`:
    
        The number of parcels per page.
    
    * `page`:
    
        The page of parcels to list.  The first parcel on the page should be the
        `perpage * (page-1)`-th parcel overall.
    
    * `format`:
        
        The format of the data.  This is only needed to override the `Accept`
        headers.
    
    Results
    -------
    
    An object is returned with the total number of parcels in the list (`count`)
    as well as references to the `next` and `previous` pages of the list.  The 
    list of parcels is returned in the `results` array.  For information about
    the data in the parcels, refer to the [PASDA](http://www.pasda.psu.edu/)
    documentation: 
    
    [http://www.pasda.psu.edu/uci/FullMetadataDisplay.aspx?file=PhiladelphiaParcels201201.xml](http://www.pasda.psu.edu/uci/FullMetadataDisplay.aspx?file=PhiladelphiaParcels201201.xml)
    """
    model = models.Parcel
    serializer_class = serializers.ParcelSerializer
    renderer_classes = (renderers.JSONRenderer, 
                        renderers.JSONPRenderer, 
                        renderers.BrowsableAPIRenderer)
    paginate_by = 20
    
    def apply_near_filter(self, queryset):
        coords = self.request.GET['near'].split(',')
        try:
            lat, lng = map(float, coords)
        except ValueError:
            raise exceptions.ParseError(
                ('Expecting exactly two comma-separated decimal '
                'numbers, not "{near}"').format(**self.request.GET))
        
        center = geos.Point(lng, lat)
        return queryset.distance(center).order_by('distance')
    
    def apply_intersecting_filter(self, queryset):
        coords = self.request.GET['intersecting'].split(',')
        try:
            lat1, lng1, lat2, lng2 = map(float, coords)
        except ValueError:
            # If the bounding coordinates parsing didn't work out, try parsing
            # the parameter as a Polygon string representation.
            return self._apply_intersecting_filter_as_string(queryset)
        
        box = geos.Polygon([(lng1, lat1), (lng1, lat2), (lng2, lat2), 
                            (lng2, lat1), (lng1, lat1)])
        return queryset.filter(shape__bboverlaps=box)
    
    def get_queryset(self):
        queryset = super(ParcelList, self).get_queryset()
        
        if 'intersecting' in self.request.GET:
            queryset = self.apply_intersecting_filter(queryset)

        if 'near' in self.request.GET:
            queryset = self.apply_near_filter(queryset)
        
        if 'perpage' in self.request.GET:
            self.paginate_by = int(self.request.GET['perpage'])
        
        return queryset

parcel_list = ParcelList.as_view()
