# cleather
A python-based CLI tool to retrieve weather, using various weather APIs

# Usage
Currently only the following functionality exists
* `cleather.py` - will try and guess where you are based on IP geolocation.  May not be accurate
* `cleather.py --location "Apex, NC"` - enter essentially any searchable/parseable location in the world.

# Purpose
The purpose of this program will is/will be to:
* Allow users to quickly poll the local weather, or weather across from virtually any location in the world
* Allow users to plug in their API key of choice to pull said weather report

# Design
* The user should be able to plug in an API key for supported weather data sources.  Currently planned sources are "Dark Sky" and "OpenWeather".
* Regardless of API, user should be able to use a variety of "canned" reports from the command line that do not vary based on the back-end data source.  That is, the actual data source will be abstracted away from the front end.  Examples of this might be:
  * Current conditions
  * Five day forecast
  * ...
* User should be able to enter any parseable location around the world, e.g.:
  * City/State
  * Zipcode
  * Geographic coordinates (Longitude, Latitude)
* User should be able to choose Imperial or Metric units when data is displayed
* User should be able to get a forecast using approximate location (via IP geolocation) in lieu of entering a particular location.  This, however, may not always be accurate.

# Notes
* By design, this program will require users to create their own API keys for various weather sources. This also assumes users follow all guidelines put in place by the data source providers.  All efforts will be made in this program to adhere to those guidelines.
* For more information on APIs, please visit the following URLs:
  * https://darksky.net/dev/
  * https://openweathermap.org/api

