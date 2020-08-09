from method import *

REGIONS = [ "ru", "br1", "eun1", "euw1", "jp1", "kr", "la1", "la2", "na1", "oc1", "tr1"]

riotAPI = riotAPI()


queue = "RANKED_SOLO_5x5"
tier = "Challengers"
division = None


for region in REGIONS:
    method().GetChallengers(region, "RANKED_SOLO_5x5", riotAPI)
    method().GetMatchIdListByTier(region, "Challengers", None , 4, riotAPI)
    df = pd.read_csv('Data/'+ region + '/matchList_Challengers.csv', index_col = False  )
    for i, matchId in enumerate( df['gameId'] ):
        method().GetMatchTimeline(region, matchId, riotAPI)
        method().GetMatchInfo(region, matchId, riotAPI)
        if( i == 50 ):
            break
    
    break

