import json
import requests
import pandas as pd
import numpy as np
import time
import os

from summoner import *
from league import *
from match import *
from dictionary import createConstantData
     
## 4. Prepare more than one API Key to handle rate limit exceed exception
API_KEY_LIST = [
    "RGAPI-2c818ce4-7164-4145-8e6c-66d70a4c148c", 
    "RGAPI-05d30bc0-be83-49e6-ad47-32d860d5625c",
    "RGAPI-7cb841d6-773e-430a-996d-5755aaa9703c"
]

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
        if (response.headers.get('Retry-After') is not None):
            remain = response.headers['Retry-After']
            print("Wait for " + str(remain) + " seconds")
            time.sleep( int(remain) )

        else:
            remain = 10
            print("Retry-After is not specified. Wait for 10 seconds.")
            time.sleep( 10 )
        
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


