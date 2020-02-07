import pymsteams

class MsTeamsConnector:
    # TODO: move this to the config file
    url = "https://outlook.office.com/webhook/b07c187d-c2ad-49bd-a17d-39eba101d006@9ca75128-a244-4596-877b-f24828e476e2/IncomingWebhook/5a54226a4fc54de8a4b1fc626bb8c894/b5cacced-92a8-4dd0-b61c-328924fc32fb"

    def __init__(self, url):
        self.url = url
    
    def sendMessage(self, message):
        myTeamsMessage = pymsteams.connectorcard(self.url)
        myTeamsMessage.text(message)
        myTeamsMessage.send()

