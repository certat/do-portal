# EventDB connection

The portal needs data from the EventDB for two purposes:

* The Eventdownload: zip-files are created per organization
* The Statistics: Grafana visualizes the EventDB per organization

# Eventdownload
In `scripts` are two scripts, a shell script and a Python script. The latter is called by the first one.
They are meant to be run on the EventDB database server and connect to the frontend (API) and backend sever of the do-portal.

Insert your paths, servers, passwords and API key in the scripts. Configure the shell script for a cron-/scheduled job. It
* deletes existing data
* Calls the Python script to
  * fetch the network objects for all organizations.
  * if objects exist, query al events from the EventDB
  * create a zipped JSON file for every orgranization
* transfers all files to the portal server

# Statistics

This is documented in the [stats-portal](https://github.com/certtools/stats-portal) repository.
