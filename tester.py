from summoner import *
from match import *
from league import *
import pandas as pd
import numpy as np
import time

region = "kr"
api_key = "RGAPI-900446e2-89da-4baa-95cb-de6c38f90b2c"

with open('Constant/champion.json', encoding='UTF8') as f:
  championPool = json.load(f)

championDict = {}
for champ in championPool["data"]:
    championDict[ championPool["data"][champ]["key"] ] = championPool["data"][champ]["name"]
    
# print( championPool["data"]["Ahri"])
# for champ in championPool["data"]:
#     print( champ )

# Region (Platform ID)
# regions = ["br1", "eun1", "euw1", "jp1", "kr", "la1", "la2", "na1", "oc1", "tr1", "ru"]
#

regions = ["euw1", "jp1", "kr", "la1", "la2", "na1", "oc1", "tr1", "ru"]


# API key (Add multiple keys)
# []
#

def GetChallengers(region, queue, key):
    # Get Challenger League Entries
    ChallengerEntries = LeagueAPI(region, key).GetChallengers(queue)

    # Create empty dataframe with column names
    ChallengerDF = pd.DataFrame(columns = SummonerAPI(region, key).returnKey )
        
    # Get summonerDTO from all entries
    for entry in ChallengerEntries["entries"]:
        data = SummonerAPI(region, key).BySmmnrID(entry["summonerId"])
        ChallengerDF = ChallengerDF.append( data, ignore_index=True )

    ChallengerDF.to_csv( 'Data/' + region + '/Challengers.csv', encoding="utf-8-sig")


def GetGrandmasters(region, queue, key):
    # Get Challenger League Entries
    GrandmasterEntries = LeagueAPI(region, key).GetGrandmasters(queue)

    # Create empty dataframe with column names
    GrandmasterDF = pd.DataFrame(columns = SummonerAPI(region, key).returnKey )
        
    # Get summonerDTO from all entries
    for entry in GrandmasterEntries["entries"]:
        data = SummonerAPI(region, key).BySmmnrID(entry["summonerId"])
        GrandmasterDF = GrandmasterDF.append( data, ignore_index=True )

    GrandmasterDF.to_csv( 'Data/' + region + '/Grandmasters.csv', encoding="utf-8-sig")


def GetUsers(region, key, queue, tier, division):
    # Get League Entries with parameters
    LeagueEntries = LeagueAPI(region, key).ByEntries(queue, tier, division)
    LeagueDF = pd.DataFrame(columns = SummonerAPI(region, key).returnKey )

    for index, entry in enumerate(LeagueEntries):
        data = SummonerAPI(region, key).BySmmnrID(entry["summonerId"])
        LeagueDF = LeagueDF.append( data, ignore_index=True )
        # Manually set the number of users to get
        if( index == 100 ):
            break

    LeagueDF.to_csv( 'Data/' + region + "/" + tier + "/" + division + '.csv', encoding="utf-8-sig")


for region in regions:
    GetChallengers(region, "RANKED_SOLO_5x5" , api_key)
    GetGrandmasters(region, "RANKED_SOLO_5x5", api_key)


def GetMatchIdList(region, key, accountId, weeks):
    # Get Matchlist of user with accountID starting from weeks before
    matchList = MatchAPI(region, key).ByAccountId(accountId, weeks)  
    for match in matchList:
        print( match )


def GetMatchTimeline(region, key, gameId):
    matchTimeline = MatchAPI(region, key).Timeline(gameId)

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

# "ITEM_DESTROYED : 아이템 합칠때 사라지는 아이템들을 나타냄"


def GetMatchInfo(region, key, gameId):
    matchInfo = MatchAPI(region, key).MatchInfo(gameId)
    DF_column = [ "gameId", "platformId", "gameCreation", "gameDuration", "queueId", 
                  "mapId", "seasonId", "gameVersion", "gameMode", "gameType" ]

    teamDTOColumn = ["teamId", "win", "firstBlood", "firstTower", "firstInhibitor", "firstBaron", "firstDragon", "firstRiftHerald",
                     "towerKills", "inhibitorKills", "baronKills", "dragonKills", "vilemawKills", "riftHeraldKills", "dominionVictoryScore",
                     "ban1", "ban2", "ban3", "ban4", "ban5"]

    participantDTOColumn = ["blue_support_total_damage_dealt", "blue_adc_total_damage_dealt",
                            "blue_top_total_damage_dealt", "blue_mid_total_damage_dealt", "blue_jungle_total_damage_dealt",
                            "red_support_total_damage_dealt", "red_adc_total_damage_dealt",
                            "red_top_total_damage_dealt", "red_mid_total_damage_dealt", "red_jungle_total_damage_dealt"
                            ]

    blue_team = {}
    red_team = {}

    DF_column = DF_column + participantDTOColumn

    

    for participant in matchInfo["participants"]:
        # blue team member info
        if( participant["teamId"] == 100):
            if( participant["timeline"]["role"] == "DUO_SUPPORT"):
                blue_team["blue_support_total_damage_dealt"] = participant["stats"]["totalDamageDealt"]
                
            elif( participant["timeline"]["role"] == "DUO_CARRY"):
                blue_team["blue_adc_total_damage_dealt"] = participant["stats"]["totalDamageDealt"]

            elif( participant["timeline"]["lane"] == "TOP"):
                blue_team["blue_top_total_damage_dealt"] = participant["stats"]["totalDamageDealt"]

            elif( participant["timeline"]["lane"] == "MIDDLE"):
                blue_team["blue_mid_total_damage_dealt"] = participant["stats"]["totalDamageDealt"]

            elif( participant["timeline"]["lane"] == "JUNGLE"):
                blue_team["blue_jungle_total_damage_dealt"] = participant["stats"]["totalDamageDealt"]

            else:
                continue

        # red team member info
        else:
            if( participant["timeline"]["role"] == "DUO_SUPPORT"):
                red_team["red_support_total_damage_dealt"] = participant["stats"]["totalDamageDealt"]
                
            elif( participant["timeline"]["role"] == "DUO_CARRY"):
                red_team["red_adc_total_damage_dealt"] = participant["stats"]["totalDamageDealt"]

            elif( participant["timeline"]["lane"] == "TOP"):
                red_team["red_top_total_damage_dealt"] = participant["stats"]["totalDamageDealt"]

            elif( participant["timeline"]["lane"] == "MIDDLE"):
                red_team["red_mid_total_damage_dealt"] = participant["stats"]["totalDamageDealt"]

            elif( participant["timeline"]["lane"] == "JUNGLE"):
                red_team["red_jungle_total_damage_dealt"] = participant["stats"]["totalDamageDealt"]

            else:
                continue

    # print( blue_team )
    # print( red_team )

    for team in matchInfo["teams"]:
        if( team["teamId"] == 100):                
            blue_bans = dict( (key + "_blue", value) for (key, value) in team.items() )
            
            for i, ban in enumerate( blue_bans["bans_blue"] ):
                if( ban["championId"] == -1 ):
                    blue_bans["ban" + str(i + 1) + "_blue"] = "None"

                else:
                    blue_bans["ban" + str(i + 1) + "_blue"] = championDict[ str(ban["championId"]) ]

            blue_bans.pop("bans_blue")

            DF_column = DF_column + [ col + "_blue" for col in teamDTOColumn ]

        else:
            red_bans = dict( (key + "_red", value) for (key, value) in team.items() )
            for i, ban in enumerate( red_bans["bans_red"] ):
                if( ban["championId"] == -1 ):
                    red_bans["ban" + str(i + 1) + "_red"] = "None"

                else:
                    red_bans["ban" + str(i + 1) + "_red"] = championDict[ str(ban["championId"]) ]

            red_bans.pop("bans_red")

            DF_column = DF_column + [ col + "_red" for col in teamDTOColumn ]

    matchInfoDF = pd.DataFrame(columns = DF_column)

    matchInfo.pop("teams")
    matchInfo.pop("participants")
    matchInfo.pop("participantIdentities")

    matchInfo.update(blue_bans)
    matchInfo.update(blue_team)
    matchInfo.update(red_bans)
    matchInfo.update(red_team)

    matchInfoDF = matchInfoDF.append( matchInfo, ignore_index=True )

    matchInfoDF.to_csv( 'infotemp.csv', encoding="utf-8-sig")


# GetUsers(region, api_key, "RANKED_SOLO_5x5", "DIAMOND", "I")

# GetChallengers(region, "RANKED_SOLO_5x5", api_key)

# GetMatchIdList("kr", api_key, "7JjHnMpqeSbMAo3erX0PYGzxP32N17pY0oY_1-I6maXQ5BE", 3)

# GetMatchTimeline(region, api_key, 4535837312 )

# GetMatchInfo(region, api_key, 4535837312 )

# print( championDict )