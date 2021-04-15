# https://affiliate.itunes.apple.com/resources/documentation/itunes-store-web-service-search-api/
import requests
import json
from dataclasses import dataclass
from datetime import datetime
@dataclass
class album:
    artist: str
    album: str
    genre: str
    stream: str
    artwork: str
    date: str
    


def reload(): exec(open("api.py").read())

def genQuery(searchterm:str)->[dict]:
    base = "https://itunes.apple.com/search?term="
    genQuery = lambda term: base + searchterm.replace(" ","+")
    return requests.get(genQuery(searchterm)).json()

def parseQuery(lst:[dict]):
    def extract(entry:dict):
        if(entry.get("collectionName")):
            tmp = (album( entry["artistName"], entry["collectionName"], entry["primaryGenreName"], entry["previewUrl"], entry["artworkUrl100"], datetime.fromisoformat(entry["releaseDate"][0:-1])) )
            return tmp
        else:
            return None
    return list(filter(lambda i: i!=None, map(extract, lst["results"])))
def getRecords(query):
    tmp = genQuery(query)
    return parseQuery(tmp)
