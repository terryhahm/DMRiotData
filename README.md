# DMRiotData

## Get Riot Constant Data 
### 1. Champion Data (from "key" to "name")
```
with open('Constant/champion.json', encoding='UTF8') as f:
  championPool = json.load(f)

championDict = {}
for champ in championPool["data"]:
    championDict[ championPool["data"][champ]["key"] ] = championPool["data"][champ]["name"]
```    
### 2. Get API URL
```
with open('Constant/riotAPIurl.json') as f:
  riotAPIurl = json.load(f)
```

### 3. Get all platform ID to iterate
```
regions = ["br1", "eun1", "euw1", "jp1", "kr", "la1", "la2", "na1", "oc1", "tr1", "ru"]
```
### 4. Prepare more than one API Key to handle rate limit exceed exception
```
api_key_list = [
    "RGAPI-900446e2-89da-4baa-95cb-de6c38f90b2c",
    "RGAPI-aad918a1-468c-423c-aca8-7b15068e0534"
]
```

## Define API Class

### API REQUEST
```


```


### SUMMONER API
```
class SummonerAPI:
    # Method 1: Get a summoner by account ID
    def ByAccntID(self, region, accntId ):
        url = riotAPIurl['SUMMONER']['AccountId']
        formatted_url = url.format(region = region, accountId = accntId)
        data = requestRiot(formatted_url).request()
        return data

    # Method 2: Get a summoner by summoner name
    def BySmmnrName(self, region, smmnrName ):
        url = riotAPIurl['SUMMONER']['SummonerName']
        formatted_url = url.format(region = region, summonerName = smmnrName)
        data = requestRiot(formatted_url).request()
        return data

    # Method 3: Get a summoner by PUUID
    def ByPUUID(self, puuid ):
        url = riotAPIurl['SUMMONER']['PUUID']
        formatted_url = url.format(region = region, puuid = puuid)
        data = requestRiot(formatted_url).request()
        return data

    # Method 4: Get a summoner by summoner ID.
    def BySmmnrID(self, smmnrId ):
        url = riotAPIurl['SUMMONER']['SummonerId']
        formatted_url = url.format(region = region, summonerId = smmnrId)
        data = requestRiot(formatted_url).request()
        return data
```