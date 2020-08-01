import requests                
import json
from requestRiot import requestRiot

with open('Constant/riotAPIurl.json') as f:
  riotAPIurl = json.load(f)

class LeagueAPI:
    # Default 
    def __init__(self, region, key):
        self.region = region
        self.key = key

    # Method 1: Get all league entries 
    def ByEntries(self, queue, tier, division ):
        url = riotAPIurl['LEAGUE']['Entries']
        page = 1
        dataTotal = []
        while True:
            formatted_url = url.format(region = self.region, key = self.key, queue = queue, tier = tier, division = division, page = page)
            dataPerPage = requestRiot(formatted_url).request()
            dataTotal = dataTotal + dataPerPage
            if( len(dataPerPage) == 0 ):
                break        
            page += 1

        return dataTotal

    # Method 2: Get league entries in all queues for a given summoner ID
    def BySmmnrId(self, smmnrId ):
        url = riotAPIurl['LEAGUE']['SummonerId']
        formatted_url = url.format(region = self.region, key = self.key, summonerId = smmnrId)
        data = requestRiot(formatted_url).request()
        return data

    # Method 3: Get league with given ID, including inactive entries
    def ByLeagueId(self, leagueId ):
        url = riotAPIurl['LEAGUE']['LeagueId']
        formatted_url = url.format(region = self.region, key = self.key, leagueId = leagueId)
        data = requestRiot(formatted_url).request()
        return data

    # Method 4: Get the master league for given queue
    def GetMasters(self, queue ):
        url = riotAPIurl['LEAGUE']['Master']
        formatted_url = url.format(region = self.region, key = self.key, queue = queue)
        data = requestRiot(formatted_url).request()
        return data
    
    # Method 5: Get the grandmaster league of a specific queue
    def GetGrandmasters(self, queue ):
        url = riotAPIurl['LEAGUE']['Grandmaster']
        formatted_url = url.format(region = self.region, key = self.key, queue = queue)
        data = requestRiot(formatted_url).request()
        return data

    # Method 6: Get the challenger league for given queue
    def GetChallengers(self, queue ):
        url = riotAPIurl['LEAGUE']['Challenger']
        formatted_url = url.format(region = self.region, key = self.key, queue = queue)
        data = requestRiot(formatted_url).request()
        return data
