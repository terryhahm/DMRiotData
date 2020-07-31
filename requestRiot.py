import requests

class responseHandler:
    def __init__(self, err):
        self.err = err

    def handleHTTPError(self):
        print(self.err)
        return self.err

    def handleConnectionError(self):
        print(self.err)
        return self.err

    def handleTimeout(self):
        print(self.err)
        return self.err

    def handleRequestException(self):
        print(self.err)
        return self.err


class requestRiot:
    def __init__(self, url):
        self.url = url

    def request(self):
        try:
            response = requests.get( self.url )
            response.raise_for_status()

        except requests.exceptions.HTTPError as errh:
            responseHandler(errh).handleHTTPError()

        except requests.exceptions.ConnectionError as errc:
            responseHandler(errc).handleConnectionError()

        except requests.exceptions.Timeout as errt:
            responseHandler(errt).handleTimeout()

        except requests.exceptions.RequestException as err:
            responseHandler(err).handleRequestException()
            
        
        return response.json()