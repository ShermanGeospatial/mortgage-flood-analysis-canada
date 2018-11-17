#A script for parsing the Canadian Disaster Database RSS feed to extract flood data including time and location.

import feedparser
import numpy as np

def averageCoordinate(cords):

    numCords = len(cords)
    avgLon = 0.0
    avgLat = 0.0

    for cord in cords:
        avgLon += cord[0]
        avgLat += cord[1]

    return np.array([avgLon/numCords,avgLat/numCords],dtype=np.float64)

def parseEntry(entry):

    entryMap = {}

    eventType, locationName = entry['title'].split(':')
    date = entry['published_parsed']
    coordinates = entry['where']['coordinates']

    eventType = eventType.rstrip(' ')
    locationName = locationName.lstrip(' ')

    entryMap['type'] = eventType
    entryMap['location'] = locationName
    entryMap['year'] = date.tm_year
    entryMap['month'] = date.tm_mon

    try:
        entryMap['longitude'] = float(coordinates[0])
        entryMap['latitude'] = float(coordinates[1])

    except TypeError:

        avgCords = averageCoordinate(entry['where']['coordinates'][0])

    return entryMap

cddFeed = feedparser.parse('http://cdd.publicsafety.gc.ca/CDDService/georssatom/EventMapLayer?cultureCode=en-Ca&provinces=1%2c2%2c3%2c4%2c5%2c6%2c7%2c8%2c9%2c10%2c11%2c12%2c13%2c14&eventTypes=%27EP%27%2c%27IN%27%2c%27PA%27%2c%27AV%27%2c%27CE%27%2c%27DR%27%2c%27FL%27%2c%27GS%27%2c%27HE%27%2c%27HU%27%2c%27SO%27%2c%27SS%27%2c%27ST%27%2c%27TO%27%2c%27WF%27%2c%27SW%27%2c%27EQ%27%2c%27LS%27%2c%27TS%27%2c%27VO%27%2c%27AI%27%2c%27AR%27%2c%27VE%27%2c%27CD%27%2c%27CR%27%2c%27HA%27%2c%27HM%27%2c%27HR%27%2c%27HV%27%2c%27TB%27%2c%27TA%27%2c%27TC%27%2c%27TF%27%2c%27TH%27%2c%27TK%27%2c%27TN%27%2c%27TR%27%2c%27TT%27%2c%27EI%27%2c%27ER%27%2c%27FI%27%2c%27FE%27%2c%27FV%27%2c%27ZD%27%2c%27ZF%27%2c%27ZL%27%2c%27ZM%27%2c%27ZV%27%2c%27IC%27%2c%27IE%27%2c%27IM%27%2c%27IT%27%2c%27IW%27%2c%27AA%27%2c%27MA%27%2c%27RA%27%2c%27VA%27%2c%27SD%27%2c%27SL%27&normalizedCostYear=1&dynamic=false')

feedEntries = cddFeed.entries

for entry in feedEntries:

    #['updated_parsed', 'updated', 'published_parsed', 'links', 'author', 'tags', 'summary', 'content', 'guidislink', 'title_detail', 'href', 'link', 'authors', 'title', 'author_detail', 'where', 'id', 'published']
    try:
        eventType, locationName = entry['title'].split(':')

        eventType = eventType.rstrip(' ')

        if eventType == "Flood" or eventType == "flood":

            entryMap = parseEntry(entry)

    except ValueError:
            
        'Do Nothing'