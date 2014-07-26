from django.contrib.gis.db import models

class Parcel (models.Model):
    """
    A Parcel corresponding to the PASDA data for Philadelphia.

    """

    objectid   = models.PositiveIntegerField(primary_key=True, help_text="Internal feature number.")
    recsub     = models.CharField(max_length=2, help_text="Submap to a registry map", null=True)
    basereg    = models.CharField(max_length=10, help_text="The registry number which there is a deed attached to", null=True)
    mapreg     = models.CharField(max_length=10, help_text="Registry number that may or may not specifically have a deed attached to it.  In cases of parcels crossing multiple maps see the BASEREG for the associated deed.", null=True)
    parcel     = models.CharField(max_length=4, help_text="Identifier for properties on the same map.", null=True)
    recmap     = models.CharField(max_length=6, help_text="Registry map name.  Department of Records tax map.", null=True)
    stcod      = models.IntegerField(help_text="Street code.  maintained by the City of Philadelphia-Department of Streets", null=True)
    house      = models.IntegerField(help_text="House number", null=True)
    suf        = models.CharField(max_length=1, help_text="The suffix to a house number", null=True)
    unit       = models.CharField(max_length=7, help_text="The address unit", null=True)
    stex       = models.IntegerField(help_text="The extension of an address accross multiple addresses", null=True)
    stdir      = models.CharField(max_length=254, help_text="Street direction", null=True)
    stnam      = models.CharField(max_length=30, help_text="Street name", null=True)
    stdes      = models.CharField(max_length=3, help_text="The designation of the street", null=True)
    stdessuf   = models.CharField(max_length=1, help_text="The suffix of the designation of the street", null=True)
    elev_flag  = models.IntegerField(help_text="The elevation flag.  Whether or not a parcel contains elevated rights", null=True)
    topelev    = models.FloatField(help_text="The topmost elevation", null=True)
    botelev    = models.FloatField(help_text="The bottom most elevation", null=True)
    condoflag  = models.IntegerField(help_text="Condominium flag", null=True)
    matchflag  = models.IntegerField(help_text="Unused", null=True)
    inactdate  = models.DateField(help_text="The date of inactivation", null=True)
    orig_date  = models.DateField(help_text="The date of origination", null=True)
    status     = models.IntegerField(help_text="The status of each parcel", null=True)
    geoid      = models.CharField(max_length=25, null=True)
    shape_area = models.FloatField(null=True)
    shape_len  = models.FloatField(null=True)

    shape = models.GeometryField(help_text="Coordinates defining the features.", null=True)
    objects = models.GeoManager()

    def __unicode__(self):
        components = []
        if self.house: components.append(unicode(self.house))
        if self.stdir: components.append(unicode(self.stdir))
        if self.stnam: components.append(unicode(self.stnam))
        if self.stdes: components.append(unicode(self.stdes))
        return u' '.join(components)
