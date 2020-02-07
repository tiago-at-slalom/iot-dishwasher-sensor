import pymsteams

class MsTeamsConnector:
    # TODO: move this to the config file
    url = "https://outlook.office.com/webhook/664a924c-d306-4a91-a953-c4b555c5484e@9ca75128-a244-4596-877b-f24828e476e2/IncomingWebhook/cfb87b236f254cbfb770f070a5e1b892/b5cacced-92a8-4dd0-b61c-328924fc32fb"

    def __init__(self, url):
        self.url = url
    
    def sendMessage(self, message):
        myTeamsMessage = pymsteams.connectorcard(self.url)
        myTeamsMessage.text(message)
        myTeamsMessage.send()

