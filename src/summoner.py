import requests                
import json

with open('src/Constant/riotAPIurl.json') as f:
  riotAPIurl = json.load(f)

class SummonerAPI:
    # Method 1: Get a summoner by account ID
    def ByAccntID(self, region, accntId, riotAPI ):
        url = riotAPIurl['SUMMONER']['AccountId']
        formatted_url = url.format(region = region, accountId = accntId)
        riotAPI.setURL( formatted_url )
        data = riotAPI.requestAPI()
        return data

    # Method 2: Get a summoner by summoner name
    def BySmmnrName(self, region, smmnrName, riotAPI ):
        url = riotAPIurl['SUMMONER']['SummonerName']
        formatted_url = url.format(region = region, summonerName = smmnrName)
        riotAPI.setURL( formatted_url )
        data = riotAPI.requestAPI()
        return data

    # Method 3: Get a summoner by PUUID
    def ByPUUID(self, region, puuid, riotAPI ):
        url = riotAPIurl['SUMMONER']['PUUID']
        formatted_url = url.format(region = region, puuid = puuid)
        riotAPI.setURL( formatted_url )
        data = riotAPI.requestAPI()
        return data

    # Method 4: Get a summoner by summoner ID.
    def BySmmnrID(self, region, smmnrId, riotAPI ):
        url = riotAPIurl['SUMMONER']['SummonerId']
        formatted_url = url.format(region = region, summonerId = smmnrId)
        riotAPI.setURL( formatted_url )
        data = riotAPI.requestAPI()
        return data



