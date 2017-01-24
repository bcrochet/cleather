# cleather
A python-based CLI tool to retrieve weather, using various weather APIs

# Purpose
The purpose of this program will is/will be to:
* Allow users to quickly poll the local weather, or weather across from virtually any location in the world
* Allow users to plug in their API key of choice to pull said weather report

# Design
* The user should be able to plug in an API key for supported weather data sources.  Currently planned sources are "Dark Sky" and Open Weather.
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

