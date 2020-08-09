import requests                
import json
import time

with open('src/Constant/riotAPIurl.json') as f:
  riotAPIurl = json.load(f)

class MatchAPI:
    # Method 1: Get match by match ID 
    def MatchInfo(self, region, matchId, riotAPI ):
        url = riotAPIurl['MATCH']['Match']
        formatted_url = url.format(region = region, matchId = matchId)
        riotAPI.setURL( formatted_url )
        data = riotAPI.requestAPI()
        return data

    # Method 2: Get matchlist for games played on given account ID and platform ID 
    #           and filtered using given filter parameters, if any
    # [Maximum time period is "one week" per request]
    def ByAccountId(self, region, accntId, dsgnKeyIdx, intervalInWeek, riotAPI):
        url = riotAPIurl['MATCH']['MatchList']
        data = []

        currentTime = int(round(time.time() * 1000))
        week_in_mill = 604800000

        beginTime = currentTime - week_in_mill * intervalInWeek
        
        while beginTime < currentTime:
            endTime = beginTime + week_in_mill
            # get optional query parameter if needed,
            query = "queue=420&beginTime=" + str(beginTime) + "&endTime=" + str(endTime) + "&" 
            formatted_url = url.format(region = region, queryParam = query, accountId = accntId)
            riotAPI.setDsgnKeyIdx( dsgnKeyIdx )
            riotAPI.setURL( formatted_url )
            jsonData = riotAPI.requestMatchAPI()
            if( jsonData is not None):
                data = data + jsonData["matches"]
            beginTime = endTime

        return data

    # Method 3: Get match timeline by match ID
    def Timeline(self, region, matchId, riotAPI ):
        url = riotAPIurl['MATCH']['Timeline']
        formatted_url = url.format(region = region, matchId = matchId)
        riotAPI.setURL( formatted_url )
        data = riotAPI.requestAPI()
        return data