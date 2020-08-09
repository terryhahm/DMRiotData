from league import *
from summoner import *
from riotAPI import *
import pandas as pd
import numpy as np

with open('src/Constant/modifiedChampion.json', encoding='UTF8') as f:
    championDict = json.load(f)

with open('src/Constant/modifiedItem.json', encoding='UTF8') as f:
    itemDict = json.load(f)

with open('src/Constant/modifiedRunes.json', encoding='UTF8') as f:
    runeDict = json.load(f)

with open('src/Constant/modifiedSpell.json', encoding='UTF8') as f:
    spellDict = json.load(f)

summonerDTOKey = ['accountId', 'profileIconId', 'revisionDate', 'name', 'id', 'puuid', 'summonerLevel', 'keyIdx']



class method():

    def GetChallengers(self, region, queue, riotAPI ):
        ChallengerEntries = LeagueAPI().GetChallengers(region, queue, riotAPI)
        ChallengerDF = pd.DataFrame(columns = summonerDTOKey )

        # Get summonerDTO from all entries
        for entry in ChallengerEntries["entries"]:
            summoner = SummonerAPI().BySmmnrName( region, entry["summonerName"], riotAPI)
            if( summoner is not None ):
                summoner["keyIdx"] = riotAPI.getCurKeyIdx()
            if( summoner["accountId"][0] == '-'):
                summoner["accountId"] = str(summoner["accountId"])
            ChallengerDF = ChallengerDF.append( summoner, ignore_index=True )

        ChallengerDF.to_csv( 'Data/' + region + '/Challengers.csv', index=False, encoding="utf-8-sig")

    def GetGrandmasters(self, region, queue, riotAPI ):
        GrandmasterEntries = LeagueAPI().GetGrandmasters(region, queue, riotAPI)
        GrandmasterDF = pd.DataFrame(columns = summonerDTOKey )

        # Get summonerDTO from all entries
        for entry in GrandmasterEntries["entries"]:
            summoner = SummonerAPI().BySmmnrName( region, entry["summonerName"], riotAPI)
            if( summoner is not None ):
                summoner["keyIdx"] = riotAPI.getCurKeyIdx()
            if( summoner["accountId"][0] == '-'):
                summoner["accountId"] = str(summoner["accountId"])
            GrandmasterDF = GrandmasterDF.append( summoner, ignore_index=True )

        GrandmasterDF.to_csv( 'Data/' + region + '/Grandmasters.csv', index=False, encoding="utf-8-sig")

    def GetMasters(self, region, queue, riotAPI ):
        MasterEntries = LeagueAPI().GetMasters(region, queue, riotAPI)
        MasterDF = pd.DataFrame(columns = summonerDTOKey )

        # Get summonerDTO from all entries
        for entry in MasterEntries["entries"]:
            summoner = SummonerAPI().BySmmnrName( region, entry["summonerName"], riotAPI)
            if( summoner is not None ):
                summoner["keyIdx"] = riotAPI.getCurKeyIdx()
            if( summoner["accountId"][0] == '-'):
                summoner["accountId"] = str(summoner["accountId"])
            MasterDF = MasterDF.append( summoner, ignore_index=True )

        MasterDF.to_csv( 'Data/' + region + '/Masters.csv', index=False, encoding="utf-8-sig")

    def GetPlayers(self, region, queue, tier, division, riotAPI ):
        PlayerEntries = LeagueAPI().ByEntries(region, queue, tier, division, riotAPI)
        PlayerDF = pd.DataFrame(columns = summonerDTOKey )

        # Get summonerDTO from all entries
        for i, entry in enumerate( PlayerEntries ):
            summoner = SummonerAPI().BySmmnrName( region, entry["summonerName"], riotAPI)
            if( summoner is not None ):
                summoner["keyIdx"] = riotAPI.getCurKeyIdx()
            if( summoner["accountId"][0] == '-'):
                summoner["accountId"] = str(summoner["accountId"])

            PlayerDF = PlayerDF.append( summoner, ignore_index=True )

        PlayerDF.to_csv( 'Data/' + region + '/' + tier + '_' + division + '.csv', index=False, encoding="utf-8-sig")


    def GetMatchIdListByTier(self, region, tier, division, week, riotAPI):

        if( division is not None):
            readFilePath = 'Data/' + region + '/' + tier + "_" + division + '.csv'
            writeFilePath = 'Data/' + region + '/matchList_' + tier + "_" + division + '.csv'
        else:
            readFilePath = 'Data/' + region + '/' + tier + '.csv'
            writeFilePath = 'Data/' + region + '/matchList_' + tier + '.csv'

        userList = pd.read_csv(readFilePath, index_col = False )
        matchListByPlayer = [MatchAPI().ByAccountId( region, accountId, keyIdx, week, riotAPI) for (accountId, keyIdx) in zip(userList['accountId'], userList['keyIdx']) ]

        matchDict = {}

        for playerList in matchListByPlayer:
            for match in playerList: 
                if( match is not None):
                    matchDict[ match["gameId"] ] = True

        matchDF = pd.DataFrame( matchDict.keys(), columns = ["gameId"] )
        matchDF.to_csv( writeFilePath, index=False, encoding="utf-8-sig")


    def GetMatchTimeline(self, region, gameId, riotAPI, maxTrial = 3):
        if (not os.path.exists( './Data/' + region + '/matches/' + str(gameId) ) ):
            os.mkdir('./Data/' + region + '/matches/' + str(gameId) )

        matchTimeline = MatchAPI().Timeline(region, gameId, riotAPI)

        # If unexpected error occurred, retry 
        if( matchTimeline is None):
            if( maxTrial == 0 ):
                print("Data somehow not exists with unexpected error.")
                return
            return self.GetMatchTimeline(region, gameId, riotAPI, maxTrial - 1)

        matchTimelineDF = pd.DataFrame(columns = [
            "laneType", "skillSlot", "ascendedType", "creatorId", "afterId", 
            "eventType", "type", "levelUpType", "wardType", 
            "participantId", "towerType", "itemId", "beforeId", "pointCaptured", 
            "monsterType", "monsterSubType", "teamId", "position", "killerId", 
            "timestamp", "assistingParticipantIds", "buildingType", "victimId"] )

        for frame in matchTimeline["frames"]:
            for event in frame["events"]:
                matchTimelineDF = matchTimelineDF.append( event, ignore_index=True )

        matchTimelineDF.to_csv( 'Data/' + region + '/matches/' + str(gameId) + '/timeline.csv', index=False, encoding="utf-8-sig")

    def ParseParticipantStat(self, result, data, key ):
        if( key.startswith('item') ):
            if( data["stats"][key] == 0):
                result[key] = None
            else:
                result[key] = itemDict[str(data["stats"][key])]

        elif( key.startswith('perk') and (len(key) == 5 or key[-1] == 'e') ):
            result[key] = runeDict[ str(data["stats"][key])]

        else:
            result[key] = data["stats"][key]


    def ParseParticipantTimeline(self, param, data ):
        colNames = ["creepsPerMinDeltas","xpPerMinDeltas","goldPerMinDeltas","csDiffPerMinDeltas",
                "xpDiffPerMinDeltas","damageTakenPerMinDeltas","damageTakenDiffPerMinDeltas"]

        for col in colNames:
            for i in range(0, len( data["creepsPerMinDeltas"] )):
                i = i * 10
                key = [ match for match in data[col].keys() if match.startswith(str(i)) ]
                param[ col + "-" + str(i) + "_" + str(i+10) ] = data[col][key[0]]

    def GetMatchInfo(self, region, gameId, riotAPI, maxTrial = 3):
        matchInfo = MatchAPI().MatchInfo(region, gameId, riotAPI)

        matchInfoPlayerDF = pd.DataFrame(columns = usingColNames)
        matchInfoTeamDF = pd.DataFrame()

        player = {}

        if( matchInfo is None):
            if( maxTrial == 0 ):
                print("Data somehow not exists with unexpected error.")
                return
            return self.GetMatchInfo(region, gameId, riotAPI, maxTrial - 1)
        
        # Participants Identities (Participant ID - Player Info (summoner Name maybe))
        for (identity, info) in zip( matchInfo["participantIdentities"], matchInfo["participants"] ) :
            player["participantId"] = identity["participantId"]
            player["summonerName"] = identity["player"]["summonerName"]
            player["champion"] = championDict[ str(info["championId"]) ]
            player["spell1"] = spellDict[ str(info["spell1Id"]) ]
            player["spell2"] = spellDict[ str(info["spell2Id"]) ]
            player["role"] = info["timeline"]["role"] 
            player["lane"] = info["timeline"]["lane"] 

            np.vectorize( self.ParseParticipantStat ) ( player, info, [key for key in usingColNames])
            self.ParseParticipantTimeline(player, info["timeline"] )

            matchInfoPlayerDF = matchInfoPlayerDF.append( player, ignore_index=True )

        matchInfoPlayerDF.to_csv( 'Data/' + region + '/matches/' + str(gameId) + '/player.csv', index=False, encoding="utf-8-sig")

        # Team Info (Team Stat, Team Ban)
        for team in matchInfo["teams"]:
            color = "_blue" if team["teamId"] == 100 else "_red"
            bans = dict( (key + color, value) for (key, value) in team.items() )
            
            for i, ban in enumerate( bans["bans" + color] ):
                if( ban["championId"] == -1 ):
                    bans["ban" + str(i + 1) + color] = "None"

                else:
                    bans["ban" + str(i + 1) + color] = championDict[ str(ban["championId"]) ]

            bans.pop("bans" + color)

            matchInfoTeamDF = matchInfoTeamDF.append( bans, ignore_index=True)

        matchInfoTeamDF.to_csv( 'Data/' + region + '/matches/' + str(gameId) + '/team.csv', index=False, encoding="utf-8-sig")



