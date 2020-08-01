from summoner import *
from match import *
from league import *
import pandas as pd
import numpy as np

region = "kr"
api_key = "RGAPI-208ed4a8-a888-4aec-a53b-42ed32725b46"


def GetChallengers(region, queue, key):
    # Get Challenger League Entries
    ChallengerEntries = LeagueAPI(region, key).GetChallengers(queue)

    # Create empty dataframe with column names
    ChallengerDF = pd.DataFrame(columns = SummonerAPI(region, key).returnKey )
        
    # Get summonerDTO from all entries
    for entry in ChallengerEntries["entries"]:
        data = SummonerAPI(region, key).BySmmnrID(entry["summonerId"])
        ChallengerDF = ChallengerDF.append( data, ignore_index=True )

    ChallengerDF.to_csv('Challengers.csv', encoding="utf-8-sig")

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

    LeagueDF.to_csv( tier + "_" + division + '.csv', encoding="utf-8-sig")


def GetMatchId(region, key):

    # Get Account ID from csv file


    for account in accounts:
        MatchAPI(region, key).ByAccountId(account)["matches"]   


# GetUsers(region, api_key, "RANKED_SOLO_5x5", "DIAMOND", "I")

# GetChallengers(region, "RANKED_SOLO_5x5", api_key)

