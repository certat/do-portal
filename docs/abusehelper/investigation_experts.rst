.. _investigation_experts:

Expert bots available in the investigation room
===============================================

Experts marked (L) are local; they do not make any queries outside CERT-EU
network.

+-------------------------+----------------------------------------------------+
| Bot name                | Description                                        |
+=========================+====================================================+
| alexarankexpert         | Retrieves Alexa domain rank                        |
+-------------------------+----------------------------------------------------+
| geoip2locationexpert    | Geolocalize IPv4 using IP2Location database (L)    |
+-------------------------+----------------------------------------------------+
| geoip2location6expert   | Geolocalize IPv6 using IP2Location database (L)    |
+-------------------------+----------------------------------------------------+
| aviraexpert             | Search given domain in Avira URL cloud             |
+-------------------------+----------------------------------------------------+
| bgpexpert               | Show BGP information for given IP (L)              |
+-------------------------+----------------------------------------------------+
| blacklistexpert         | Looks up results from various url/domain/ip        |
|                         | blacklists. Available services: multi.surbl.org,   |
|                         | uri.ca2.sophosxl.com, dnsbl.mailshell.net,         |
|                         | dnsbl.ahbl.org, dnsbl.dronebl.org, bl.spamcop.net, |
|                         | dnsbl.njabl.org, b.barracudacentral.org,           |
|                         | zen.spamhaus.org, virbl.dnsbl.bit.nl,              |
|                         | multi.uribl.com, dnsbl.sorbs.net, drone.abuse.ch,  |
|                         | drone.abuse.ch, httpbl.abuse.ch, spam.abuse.ch     |
+-------------------------+----------------------------------------------------+
| clientexpert            | Check if given IP belongs to a CERT-EU constituent |
|                         | (L)                                                |
+-------------------------+----------------------------------------------------+
| csexpert                | Search CrowdStrike datasets                        |
+-------------------------+----------------------------------------------------+
| cymruexpert             | Retrieve Cymru Whois data                          |
+-------------------------+----------------------------------------------------+
| dnsexpert               | Retrieve DNS records. Requests are forwarded       |
|                         | outside only if no records are found in CERT-EU DNS|
+-------------------------+----------------------------------------------------+
| dnsptrexpert            | Get reverse DNS. Requests are forwarded to outside |
|                         | resolvers if no records are found in CERT-EU DNS   |
+-------------------------+----------------------------------------------------+
| geoipexpert             | Geolocalize IP using MaxMind database (L)          |
+-------------------------+----------------------------------------------------+
| hashtagexpert           | Identify hash type (L)                             |
+-------------------------+----------------------------------------------------+
| historyexpert           | Search AbuseHelper history (L)                     |
+-------------------------+----------------------------------------------------+
| passivedns_at           | Get passive DNS information from CERT-AT           |
+-------------------------+----------------------------------------------------+
| passivedns_lu           | Get passive DNS information from CIRCL             |
+-------------------------+----------------------------------------------------+
| passivedns_dnsdb        | Get passive DNS information from FarSight DNSDB    |
+-------------------------+----------------------------------------------------+
| passivetotalexpert      | Perform searches to PassiveTotal DB                |
+-------------------------+----------------------------------------------------+
| shodanexpert            | Query shodan for given IP                          |
+-------------------------+----------------------------------------------------+
| tldexpert               | Validate a TLD (L)                                 |
+-------------------------+----------------------------------------------------+
| whoisexpert             | Retrieve whois record for given domain             |
+-------------------------+----------------------------------------------------+
| whoisngexpert           | Retrieve whois record for given domain. (Uses a    |
|                         | different library than whoisexpert)                |
+-------------------------+----------------------------------------------------+
| wotexpert               | Returns Web Of Trust reputation for given host     |
+-------------------------+----------------------------------------------------+
| abusixexpert            | Returns abuse contact emails for a given IP        |
+-------------------------+----------------------------------------------------+
| mispeuexpert            | Searches MISP-EU (free text) and shows events (L)  |
+-------------------------+----------------------------------------------------+
| mispextexpert           | Searches MISP-DMZ (MISP-EXT) and shows events (L)  |
+-------------------------+----------------------------------------------------+
| stopforumspamexpert     | Returns forum spam information for given ip, email |
|                         | or username                                        |
+-------------------------+----------------------------------------------------+
| urlvoidexpert           | Perform searches in URLVoid dabatase               |
+-------------------------+----------------------------------------------------+
| cawsexpert              | Perform searches in NSS Labs dabatase              |
+-------------------------+----------------------------------------------------+
| dnshistoryexpert        | Get host or domain DNS history from DNSHistory     |
+-------------------------+----------------------------------------------------+
| malwarehashexpert       | Looks up malware hashes from virustotal.com and    |
|                         | the Shadowserver hash registry                     |
+-------------------------+----------------------------------------------------+
| virustotalexpert        | Looks up ip, domain, url and hashes in             |
|                         | virustotal.com database                            |
+-------------------------+----------------------------------------------------+
| passivesslluexpert      | Perform searches in CIRCL Passive SSL database     |
+-------------------------+----------------------------------------------------+
| domaintoolsexpert       | Return Domain Tools whois record for IP or domain  |
+-------------------------+----------------------------------------------------+
| ecrchashexpert          | Check if hash is in the EC Reference Configuration |
+-------------------------+----------------------------------------------------+
| goodhashexpert          | Check if hash is in the known good hashes list.    |
|                         | Hashes list includes: NIST RDS, hashsets.com,      |
|                         | Microsoft (to be added) (L)                        |
|                         | Known hash types: MD5                              |
+-------------------------+----------------------------------------------------+
