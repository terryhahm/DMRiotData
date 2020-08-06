import json
import requests
import pandas as pd
import numpy as np
import time

from summoner import *
from league import *
from match import *

# Get Riot Constant Data 
## 1. Champion Data (from "key" to "name")
with open('Constant/champion.json', encoding='UTF8') as f:
  championPool = json.load(f)

championDict = {}
for champ in championPool["data"]:
    championDict[ championPool["data"][champ]["key"] ] = championPool["data"][champ]["name"]

## 3. Get all platform ID to iterate
REGIONS = ["br1", "eun1", "euw1", "jp1", "kr", "la1", "la2", "na1", "oc1", "tr1", "ru"]

## 4. Prepare more than one API Key to handle rate limit exceed exception
API_KEY_LIST = [
    "RGAPI-9b578760-8997-46e3-a790-867a0d729973",
    "RGAPI-9bf03034-f6da-4ad5-bd4d-89661b88c4f4",
    "RGAPI-d90edc1d-d654-407f-b1f3-7a9c9cf23271"
]

summonerDTOKey = ['accountId', 'profileIconId', 'revisionDate', 'name', 'id', 'puuid', 'summonerLevel', 'keyIdx']

class riotAPI():
    def __init__(self):
        self.url = ""
        self.curKeyIdx = 0
        self.prevKeyIdx = 0
        # gameId (encryptedAccountId diff per key)
        self.dsgnKeyIdx = 0

    def setURL(self, url):
        self.url = url

    def getURL(self):
        return self.url

    def setDsgnKeyIdx(self, fixIdx):
        self.dsgnKeyIdx = fixIdx
    
    def getDsgnKeyIdx(self):
        return self.dsgnKeyIdx

    def setCurKeyIdx(self, newIdx):
        self.curKeyIdx = newIdx

    def getCurKeyIdx(self):
        return self.curKeyIdx

    def setPrevKeyIdx(self, newIdx):
        self.prevKeyIdx = newIdx

    def getPrevKeyIdx(self):
        return self.prevKeyIdx

    def waitRateLimit(self, response):
        remain = response.headers['Retry-After']
        print("Wait for " + str(remain) + " seconds")
        time.sleep( int(remain) )
        return

    def requestMatchAPI(self):
        while True:
            try: 
                response = requests.get( self.getURL().format( key = API_KEY_LIST[ self.getDsgnKeyIdx() ] ) )
                response.raise_for_status()
            
            except requests.exceptions.HTTPError as err:
                print( err )
                if( response.status_code == 429 ):
                    self.waitRateLimit( response )
                    continue

                if( response.status_code == 404 ):
                    print("This user has not played Ranked Solo for given time period.")
                    return    
                
                else:
                    print("Unexpected Error. Return `None`")
                    return
            
            return response.json()


    def requestAPI(self):
        while True:
            try:
                response = requests.get( self.getURL().format( key = API_KEY_LIST[ self.getCurKeyIdx() ] ) )
                response.raise_for_status()

            except requests.exceptions.HTTPError as err:
                print( err )
                if( response.status_code == 429):
                    if( self.getPrevKeyIdx() == len(API_KEY_LIST) - 1 ):
                        print("You used all available api keys.")
                        self.waitRateLimit( response )
                        continue

                    else:
                        print("API_KEY '%s' at index %d exceeded rate limit." % ( API_KEY_LIST[ self.getCurKeyIdx() ], self.getCurKeyIdx() ) )
                        print("Use next available key.")

                        self.setPrevKeyIdx( self.getCurKeyIdx() )

                        if( self.getCurKeyIdx()  == len(API_KEY_LIST) - 1):
                            self.setCurKeyIdx(0)
                        else:
                            self.setCurKeyIdx( self.getCurKeyIdx() + 1 )

                    continue

                else:
                    print("Unexpected Error. Return `None`")
                    return 

            # If success,
            return response.json()

def GetChallengers( region, queue, riotAPI ):
    ChallengerEntries = LeagueAPI().GetChallengers(region, queue, riotAPI)
    ChallengerDF = pd.DataFrame(columns = summonerDTOKey )
    
    # Get summonerDTO from all entries
    for entry in ChallengerEntries["entries"]:
        summoner = SummonerAPI().BySmmnrName( region, entry["summonerName"], riotAPI)
        if( summoner is not None ):
            summoner["keyIdx"] = riotAPI.getCurKeyIdx()
        ChallengerDF = ChallengerDF.append( summoner, ignore_index=True )

    ChallengerDF.to_csv( 'Data/' + region + '/Challengers.csv', index=False, encoding="utf-8-sig")


matchDTOkey = ["platformId", "gameId", "champion", "queue", "season", "timestamp", "role", "lane"]

def GetMatchIdListByTier(region, tier, riotAPI):
    userList = pd.read_csv('Data/' + region + '/' + tier + '.csv', index_col = False )
    matchListByPlayer =  np.vectorize(  MatchAPI().ByAccountId ) ( region, userList['accountId'], userList['keyIdx'], 1, riotAPI )

    matchDict = {}

    for playerList in matchListByPlayer:
        for match in playerList: 
            if( match is not None):
                matchDict[ match["gameId"] ] = True

    matchDF = pd.DataFrame( matchDict.keys(), columns = ["gameId"] )
    matchDF.to_csv( 'Data/' + region + '/match_' + tier + '.csv', index=False, encoding="utf-8-sig")


def GetMatchTimeline(region, gameId, riotAPI):
    matchTimeline = MatchAPI().Timeline(region, gameId, riotAPI)

    matchTimelineDF = pd.DataFrame(columns = [
        "laneType", "skillSlot", "ascendedType", "creatorId", "afterId", 
        "eventType", "type", "levelUpType", "wardType", 
        "participantId", "towerType", "itemId", "beforeId", "pointCaptured", 
        "monsterType", "monsterSubType", "teamId", "position", "killerId", 
        "timestamp", "assistingParticipantIds", "buildingType", "victimId"] )

    for frame in matchTimeline["frames"]:
        for event in frame["events"]:
            matchTimelineDF = matchTimelineDF.append( event, ignore_index=True )

    matchTimelineDF.to_csv( 'temp.csv', encoding="utf-8-sig")

# # Get Challenger / Grandmaster Users in each regions for 솔랭
# for region in REGIONS: 
#     GetChallengers(region, "RANKED_SOLO_5x5", riotAPI() )
#     print( "Done collecting Challengers from region %s" %(region))

# GetMatchIdListByTier( "br1", "Challengers", riotAPI() )

# Get MatchInfo / MatchTimeline



