# Geekography of France

*This is a work in progress, result of one day of hackathon @ [Digital Methods Seminar](http://digitalmethods-seminar.org/barcamp/), in Paris.*

## Dataset

The dataset is available here : <http://goo.gl/G6ymfn>

It includes all events in [Github Archive](http://www.githubarchive.org/) where the involved users are self-declared living in France at the time of the event, spanning from January 2013 to april 2014. This include 2,398,529 events involving 18,640 users and 282,343 repositories.

You can find a description of the different event types available on [Github API documentation](https://developer.github.com/v3/activity/events/types/).

## Additional Features

### Locations

Around 50% of events can be geolocalized on Github Archive, through the entry "location" on users' public profiles. The file `french_locations` bind all self-declared french locations to structured data from [Google Geocoding API](https://developers.google.com/maps/documentation/geocoding/).

### Genders

We used [GenderComputer](https://github.com/tue-mdse/genderComputer) to infer users' gender from their self-declared name available on their public profile. We successfully genderized more than 60% of users.

## About

Proudly brought to you by:

+ [Antoine Mazières](http://mazier.es)
+ Pauline Gourlet
+ Sarah Garcin
+ Idir Meziani
+ Nicolas Auray

## Licences

Unless specified otherwise, all the content of this repository is under [Creative Commons Share Alike](http://creativecommons.org/licenses/by-sa/4.0/) license.