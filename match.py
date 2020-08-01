import requests                
import json
from requestRiot import requestRiot

with open('Constant/riotAPIurl.json') as f:
  riotAPIurl = json.load(f)

class MatchAPI:
    # Default 
    def __init__(self, region, key):
        self.region = region
        self.key = key

    # Method 1: Get match by match ID 
    def ByEntries(self, matchId ):
        url = riotAPIurl['MATCH']['Match']
        formatted_url = url.format(region = self.region, key = self.key, matchId = matchId)
        data = requestRiot(formatted_url).request()
        return data

    # Method 2: Get matchlist for games played on given account ID and platform ID 
    #           and filtered using given filter parameters, if any
    def ByAccountId(self, accntId):
        url = riotAPIurl['MATCH']['MatchList']
        # get optional query parameter if needed,



        formatted_url = url.format(region = self.region, key = self.key, accountId = accntId)
        data = requestRiot(formatted_url).request()
        return data

    # Method 3: Get match timeline by match ID
    def ByLeagueId(self, matchId ):
        url = riotAPIurl['MATCH']['Timeline']
        formatted_url = url.format(region = self.region, key = self.key, matchId = matchId)
        data = requestRiot(formatted_url).request()
        return data
