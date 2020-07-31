from summoner import *
from match import *
from league import *

region = "kr"
api_key = "RGAPI-54760c75-01d3-44a0-b229-def53573fa71"

# Examples
a = SummonerAPI(region, api_key)\
    .BySmmnrName("치킨라맨")

b = MatchAPI(region, api_key)\
    .ByAccountId(a["accountId"], 0)

c = LeagueAPI(region, api_key)\
    .GetMasters("RANKED_SOLO_5x5")

print(a)
print(b)
print(c)
