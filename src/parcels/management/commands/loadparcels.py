from django.core.management.base import BaseCommand, CommandError
import django
import optparse
import os
import sys
import zipfile


class Command(BaseCommand):
    help = "Load the parcel data from a shape file."

    def handle(self, *args, **options):
        pass

