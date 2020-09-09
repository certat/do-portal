# Constituency Portal

**Important: This project is in maintenance mode and will only receive bug fixes, but no new features. A new version of this software is being developed.**

This is a web-based application for managing contact information with network information, self-administration and statistics integration.
It is used by CERT.at/GovCERT.at/Austrian Energy CERT to maintain contact information for customers and network owners

![Overview of the portal's users](docs/images/architecture-users.svg)

## Features

- organization hierarchy
- Contacts always have a specified role, e.g. Administrator, Abuse contact etc.
- automatic import and update of RIPE data
- Contacts can get login access and administrate their own organization
- RIPE-handles can be assigned to organizations, linking Autonomous Systems (AS) and Network blocks (CIDRs) to organizations and (abuse) contacts
- Grafana integration to show statistics on the data from a EventDB for the organization's linked network objects
- Data per contact: PGP key, S/MIME certificate etc.

## Architecture and Software

The portal has two disjunct parts: A frontend and a backend which is queried via a RESTful API.
The Javascript based frontend uses Angular and bootstrap and and is served by static files from the server, running in the browser of the user.
The backend is a Flask-based web application using Python, Flask and SQLAlchemy. PostgreSQL is used as database backend.
The integrated [stats-portal](https://github.com/certtools/stats-portal) uses Grafana to visualize the data stored in a PostgreSQL database.

![Overview of the portal's technical components](docs/images/architecture-technical.svg)

## Screenshots

### Organization Edit Page
![organization edit page](docs/images/screenshot1.png?raw=true "")

### Organization List Page
![organization list page](docs/images/screenshot2.png?raw=true "")

### Organization Details Page
![organization details page](docs/images/screenshot3.png?raw=true "")

### Contact Create Page
![contact create page](docs/images/screenshot4.png?raw=true "")

## Related software / tools

### IntelMQ

Can retrieve the abuse contact information from the portal

https://github.com/certtools/intelmq/

### EventDB

A database feeded by IntelMQ is the data source for the event download and for the statistics

### Stats Portal

The stats portal is integrated in this portal and shows statistics for the orgranization's related network objects.

https://github.com/certtools/stats-portal/

### Fody

Fody is an interface for IntelMQ related tools. The do-portal uses it's RIPE-Import feature.

http://github.com/Intevation/intelmq-fody/

# Documentation

All documentation can be found in the [docs](docs/) directory.

# Funded by

This project was partially funded by the CEF framework

![Co-financed by the Connecting Europe Facility of the European Union](docs/images/cef_logo.png)
