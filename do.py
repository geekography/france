import json
import gzip
import os
import copy

import sys

from collections import defaultdict

def iter_archive():
	for line in gzip.open(os.path.abspath("./french_events.gz")):
		dat = json.loads(line)
		yield dat

places = json.loads(gzip.open(os.path.abspath("./french_locations.gz")).read())
genders = json.loads(gzip.open(os.path.abspath("./french_genders.gz")).read())
regions = json.loads(open(os.path.abspath("./regions.geojson")).read())

def dump_stats():
	res = defaultdict(lambda: defaultdict(int))
	reg_users = defaultdict(set)
	for event in iter_archive():
		raw_loc = event["actor_attributes"]["location"].strip()
		if raw_loc in places:
			loc = places[raw_loc.strip()]
			# city, region = None, None
			region = None
			for elem in loc["address_components"]:
				# if "locality" in elem["types"]:
				# 	city = elem["long_name"]
				if "administrative_area_level_1" in elem["types"]:
					region = elem["long_name"]
			if region:
				reg_users[region].add(event["actor_attributes"]["login"])
				res[region]["nb_events"] += 1
				if "name" in event["actor_attributes"] and\
				event["actor_attributes"]["name"] in genders:
					gender = genders[event["actor_attributes"]["name"]]
					res[region][gender] += 1
				if event["type"] in ["ForkEvent", "PullRequestEvent"]:
					res[region][event["type"]] += 1

	better_res = {}
	for region, data in res.iteritems():
		better_res[region] = {}
		better_res[region]["nb_users"] = len(reg_users[region])
		better_res[region]["nb_events"] = data["nb_events"]
		if "female" in data and "male" in data:
			better_res[region]["by_women"] = (data["female"]/float(data["female"]+data["male"]))*100.0
		if "ForkEvent" in data:
			better_res[region]["pc_forks"] = (data["ForkEvent"]/float(data["nb_events"]))*100.0
		if "PullRequestEvent" in data:
			better_res[region]["pc_pullrequests"] = (data["PullRequestEvent"]/float(data["nb_events"]))*100.0

	fo = gzip.open("simple_stats_regions.json.gz", "wb")
	fo.write(json.dumps(better_res))
	fo.close()

en_2_fr = {
	u'Poitou-Charentes': u'Poitou-Charentes',
	u'Languedoc-Roussillon': u'Languedoc-Roussillon',
	u'Lower Normandy': u'Basse-Normandie',
	u'Rhone-Alpes': u'Rh\xf4ne-Alpes',
	u'Lorraine': u'Lorraine',
	u'Picardy': u'Picardie',
	u'Midi-Pyr\xe9n\xe9es': u'Midi-Pyr\xe9n\xe9es',
	u'\xcele-de-France': u'\xcele-de-France',
	u'Nord-Pas-de-Calais': u'Nord-Pas-de-Calais',
	u'Centre': u'Centre',
	u'Aquitaine': u'Aquitaine',
	u'Auvergne': u'Auvergne',
	u'Alsace': u'Alsace',
	u'Franche-Comt\xe9': u'Franche-Comt\xe9',
	u'Upper Normandy': u'Haute-Normandie',
	u'Brittany': u'Bretagne',
	u'Pays de la Loire': u'Pays de la Loire',
	u'Limousin': u'Limousin',
	u'Champagne-Ardenne': u'Champagne-Ardenne',
	u"Provence-Alpes-C\xf4te d'Azur": u"Provence-Alpes-C\xf4te d'Azur",
	u'Burgandy': u'Bourgogne',
	u'Corsica': u'Corse'
}
fr_2_en = {v:k for k, v in en_2_fr.iteritems()}

def add_to_regions():
	stats = json.loads(gzip.open("simple_stats_regions.json.gz").read())
	print stats
	gh_regions = copy.deepcopy(regions)
	for reg in gh_regions["features"]:
		del reg["properties"]["code"]
		name_fr = reg["properties"]["nom"]
		for k, v in stats[fr_2_en[name_fr]].iteritems():
			reg["properties"][k] = v
	fo = open("github_regions.geojson", "wb")
	fo.write(json.dumps(gh_regions))
	fo.close()

if __name__ == '__main__':
	# dump_stats()
	add_to_regions()



