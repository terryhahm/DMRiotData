import requests
import time

MAX_RETRY = 3

class responseHandler:
    def __init__(self, res):
        self.res = res
        self.status_code = res.status_code

    def handleHTTPError(self):
        if( self.status_code == 429 ):
            self.waitRateLimit()
            
        return 

    def handleConnectionError(self):
        return 
    def handleTimeout(self):
        return 

    def handleRequestException(self):
        return 

    def waitRateLimit(self):
        remain = self.res.headers['Retry-After']
        # while( remain > 0 ):
        #     print("API Rate Limit exceeded, wait for " + str(remain) + " second(s)", end = '   \r')
        #     remain -= 1
        print("Wait for " + str(remain) + " seconds")
        time.sleep( int(remain) )
        # print("                                                     ", end='\r')
        return

class requestRiot:
    def __init__(self, url):
        self.url = url

    def request(self):
        trial = 1
        while trial < MAX_RETRY:
            try:
                response = requests.get( self.url )
                response.raise_for_status()
                break

            except requests.exceptions.HTTPError as errh:
                print(errh)
                responseHandler(response).handleHTTPError()

            except requests.exceptions.ConnectionError as errc:
                print(errc)
                responseHandler(response).handleConnectionError()

            except requests.exceptions.Timeout as errt:
                print(errt)
                responseHandler(response).handleTimeout()

            except requests.exceptions.RequestException as err:
                print(err)
                responseHandler(response).handleRequestException()
            
            trial += 1

        if( response.status_code == 200 ):
            return response.json()
        else:
            return
