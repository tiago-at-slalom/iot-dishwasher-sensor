import pymsteams

class MsTeamsConnector:
    # TODO: move this to the config file
    url = ""

    def __init__(self, url):
        self.url = url
    
    def sendMessage(self, message):
        myTeamsMessage = pymsteams.connectorcard(self.url)
        myTeamsMessage.text(message)
        myTeamsMessage.send()

