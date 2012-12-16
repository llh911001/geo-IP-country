geo-IP-country
==============

A GeoIP lookup implementation.

Information
-----------

There are two parts of data this program using, one is [MaxMind][]'s [free downloadable GeoIPCountryCSV][1], only that country names are adapted into Chinese,
the other is CMCC's own IP alocation information(may not be complete).

Usage
-----

### lookup\_cli.py
Usage:

        lookup_cli.py ip
example:

        $ lookup_cli.py 123.123.123.123
        IP              :123.123.123.123
        Country         :中国
        Country Code    :CN
        ISP             :

### lookup\_web

LICENSE
-------
This product includes GeoLite data created by [MaxMind][], under the [Creative Commons Attribution-ShareAlike 3.0 Unported License][License].


[1]: http://geolite.maxmind.com/download/geoip/database/GeoIPCountryCSV.zip
[MaxMind]: http://www.maxmind.com
[License]: http://creativecommons.org/licenses/by-sa/3.0/
