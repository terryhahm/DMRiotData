import requests                
import json
from requestRiot import requestRiot

with open('Constant/riotAPIurl.json') as f:
  riotAPIurl = json.load(f)

class SummonerAPI:
    # Default 
    def __init__(self, region, key):
        self.region = region
        self.key = key
        self.returnKey = ['accountId', 'profileIconId', 'revisionDate', 'name', 'id', 'puuid', 'summonerLevel']

    # Method 1: Get a summoner by account ID
    def ByAccntID(self, accntId ):
        url = riotAPIurl['SUMMONER']['AccountId']
        formatted_url = url.format(region = self.region, key = self.key, accountId = accntId)
        data = requestRiot(formatted_url).request()
        return data

    # Method 2: Get a summoner by summoner name
    def BySmmnrName(self, smmnrName ):
        url = riotAPIurl['SUMMONER']['SummonerName']
        formatted_url = url.format(region = self.region, key = self.key, summonerName = smmnrName)
        data = requestRiot(formatted_url).request()
        return data

    # Method 3: Get a summoner by PUUID
    def ByPUUID(self, puuid ):
        url = riotAPIurl['SUMMONER']['PUUID']
        formatted_url = url.format(region = self.region, key = self.key, puuid = puuid)
        data = requestRiot(formatted_url).request()
        return data

    # Method 4: Get a summoner by summoner ID.
    def BySmmnrID(self, smmnrId ):
        url = riotAPIurl['SUMMONER']['SummonerId']
        formatted_url = url.format(region = self.region, key = self.key, summonerId = smmnrId)
        data = requestRiot(formatted_url).request()
        return data
    



