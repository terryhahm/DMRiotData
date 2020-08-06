import requests                
import json

with open('Constant/riotAPIurl.json') as f:
  riotAPIurl = json.load(f)

class LeagueAPI:
    # Method 1: Get all league entries 
    def ByEntries(self, region, queue, tier, division, riotAPI ):
        url = riotAPIurl['LEAGUE']['Entries']
        page = 1
        dataTotal = []
        while True:
            formatted_url = url.format(region = region, queue = queue, tier = tier, division = division, page = page)
            riotAPI.setURL( formatted_url )
            dataPerPage = riotAPI.requestAPI()
            dataTotal = dataTotal + dataPerPage
            if( len(dataPerPage) == 0 ):
                break        
            page += 1

        return dataTotal

    # Method 2: Get league entries in all queues for a given summoner ID
    def BySmmnrId(self, region, smmnrId, riotAPI ):
        url = riotAPIurl['LEAGUE']['SummonerId']
        formatted_url = url.format(region = region, summonerId = smmnrId)
        riotAPI.setURL( formatted_url )
        data = riotAPI.requestAPI()
        return data

    # Method 3: Get league with given ID, including inactive entries
    def ByLeagueId(self, region, leagueId, riotAPI ):
        url = riotAPIurl['LEAGUE']['LeagueId']
        formatted_url = url.format(region = region, leagueId = leagueId)
        riotAPI.setURL( formatted_url )
        data = riotAPI.requestAPI()
        return data

    # Method 4: Get the master league for given queue
    def GetMasters(self, region, queue, riotAPI ):
        url = riotAPIurl['LEAGUE']['Master']
        formatted_url = url.format(region = region, queue = queue)
        riotAPI.setURL( formatted_url )
        data = riotAPI.requestAPI()
        return data
    
    # Method 5: Get the grandmaster league of a specific queue
    def GetGrandmasters(self, region, queue, riotAPI ):
        url = riotAPIurl['LEAGUE']['Grandmaster']
        formatted_url = url.format(region = region, queue = queue)
        riotAPI.setURL( formatted_url )
        data = riotAPI.requestAPI()
        return data

    # Method 6: Get the challenger league for given queue
    def GetChallengers(self, region, queue, riotAPI ):
        url = riotAPIurl['LEAGUE']['Challenger']
        formatted_url = url.format(region = region, queue = queue)
        riotAPI.setURL( formatted_url )
        data = riotAPI.requestAPI()
        return data