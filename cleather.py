#!/usr/bin/env python
import sys
import argparse
import datetime
import time
import json
import urllib2
import ephem
from geoip import geolite2
from geopy.geocoders import Nominatim
from configparser import ConfigParser

CONFIG = ConfigParser()
CONFIG.read('cleather.ini')

# Determine data source:
VALID_SOURCES = []
# Eventually add 'openweather' below
VALID_SOURCES = ['darksky']
DATASOURCE = CONFIG['settings']['datasource']
MY_DATA = DATASOURCE.strip("'")
try:
    VALID_SOURCES.index(MY_DATA)
except ValueError:
    print DATASOURCE, " is not currently a valid data source."
    print "Current valid data sources are: ", VALID_SOURCES


def read_args():
    """ Get our command line arguments """
    parser = argparse.ArgumentParser()
    parser.add_argument('--location', nargs=1, help='Location Query')
    global_args = parser.parse_args()
#   Our args are...
    return global_args


def get_apikey():
    """ Get our favored API key """
# Get key for said source and error out if missing
    if MY_DATA == 'darksky':
        apikey = CONFIG['api_keys']['api_key_darksky']
#        fluff = "Powered by Dark Sky - https://darksky.net/poweredby/"
#    if MY_DATA == 'openweather':
#        apikey=CONFIG['api_keys']['api_key_openweather']
#        fluff="Surely there will be some required text here too."
# How do I get this to work??
#    if apikey.isspace():
#        print "Error: API key for data source is missing."
#        sys.exit()
    return apikey


# Default to geoip?
def get_geo_by_ip():
    """  Get an approximate geolocation by using IP address black magic... """
#   Alternate method:
#   (requires import of sockets and request)
#   ret = [(s.connect(('8.8.8.8', 53)), s.getsockname()[0], s.close()) \
#     for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]
#   match = geolite2.lookup(ret)
    match = geolite2.lookup_mine()
    location_lat, location_long = match.location
    subdivision = match.subdivisions
    country = match.country
    my_loc = iter(subdivision).next() + ", " + country + \
        " (Approximate Location)"
    return my_loc, location_lat, location_long


# Get coordinates from <location> using geopy
def get_arg_coordinates():
    """ Get a geolocation using a more traditional/accurate service. """
    my_loc = ARGS.location[0]
    geolocator = Nominatim()
    location = geolocator.geocode(my_loc)
    location_lat, location_long = location.latitude, location.longitude
    return my_loc, location_lat, location_long


def coordinates_logic():
    """ Logic dictating which geolocation method to try first. """
    # Try to default to geoip if we can, so we can provide
    # *something*.  But this won't always work, either.
    #
    # Note: Using geoip, there doesn't appear to be a way
    # to drill down to city level without downloading and
    # referencing the database.i
    geoip = get_geo_by_ip()
    if ARGS.location:
        # Using supplied Params
        arg_coords = get_arg_coordinates()
        myloc, location_lat, location_long = arg_coords[0:3]
    elif geoip:
        # No location, trying geoip
        ip_coords = get_geo_by_ip()
        myloc, location_lat, location_long = ip_coords[0:3]
    else:
        print "Sorry, I cannot detect your location, or none entered."
        sys.exit()
    return myloc, location_lat, location_long


def get_day_phase():
    """Lots of logic here simply to put a sun or moon, dependent on whether
    or not it is day or night.  Might not be worth it - and possibly
    even confusing!"""
    # Use coordinates provided by geopy to get sunrise and sunset
    # times via ephem
    llat = MY_LOCATION_DATA[1]
    current_date = time.strftime("%Y/%m/%d")
    sun = ephem.Sun()
    e_loc = ephem.Observer()
    e_loc.pressure = 0
    e_loc.horizon = '-0:34'
    e_loc.lat = str(llat)
    e_loc.date = current_date
    # prev_sunrise = e_loc.previous_rising(ephem.Sun())
    prev_sunrise = e_loc.previous_rising(sun)
    next_sunset = e_loc.next_setting(sun)
    prev_sunset = e_loc.previous_setting(sun)
    prev_sunrise = prev_sunrise.datetime()
    prev_sunset = prev_sunset.datetime()
    next_sunset = next_sunset.datetime()

    if CURRENT_TIME > next_sunset:
        day_phase = 'Night'
    if (CURRENT_TIME > prev_sunset) and (CURRENT_TIME <= prev_sunrise):
        day_phase = 'Night'
    if (CURRENT_TIME > prev_sunrise) and (CURRENT_TIME <= next_sunset):
        day_phase = 'Day'
    return prev_sunset, prev_sunrise, next_sunset, day_phase


def gen_darksky():
    """ Generate our API url to pull data from Dark Sky"""
    my_key = get_apikey().strip("'")
    llong, llat = MY_LOCATION_DATA[1:3]
    llong = str(llong)
    llat = str(llat)
    forecast_url = 'https://api.darksky.net/forecast/' + my_key \
        + '/' + llong + ',' + llat
    return forecast_url

# Add 'canned' reports here.  Eventually these should just
# return values and be abstraced through an output mechanism
# regardless of source.


def forecast_darksky():
    """ Pull data from Dark Sky """
    url = gen_darksky()
    weather = urllib2.urlopen(url)
    wjson = weather.read()
    wdata = json.loads(wjson)
    return wdata

# def current_darksky():
# def current_openweather():
# def forecast_openweather():
# ...and so forth.


# ICONS TO USE
I_DEG = u'\N{DEGREE SIGN}'
# Use sun/moon based on sunrise/sunset
I_MOON = u'\u263E'
I_SUN = u'\u2600'
# Draw sun/rain/snow/clouds, possibly?
I_CLOUDY = u'\u2601'
I_PCLOUDY = u'\u26C5'
I_RAIN = u'\u26C8'
I_SNOW = u'\u2744'

ARGS = read_args()
CURRENT_TIME = datetime.datetime.now()
MY_LOCATION_DATA = ()
MY_LOCATION_DATA = coordinates_logic()
get_day_phase()
MY_WEATHER = forecast_darksky()

if get_day_phase()[3] is 'Night':
    P_ICON = I_MOON
else:
    P_ICON = I_SUN

WHEREAMI = MY_LOCATION_DATA[0]
MY_TIME = CURRENT_TIME.strftime("%H:%M")
TEMPERATURE = MY_WEATHER['currently']['temperature']
SUMMARY = MY_WEATHER['currently']['summary']
print P_ICON + " " + MY_TIME, WHEREAMI, "-", SUMMARY \
     + ",", str(TEMPERATURE) + I_DEG
