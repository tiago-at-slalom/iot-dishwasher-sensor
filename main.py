# import pymsteams
from msTeamsConnector import MsTeamsConnector
from sensorAdaptor import SensorAdaptor
from powerSensor import PowerSensor
from databaseAdaptor import DatabaseAdaptor
from sensorHistoryDatabase import SensorHistoryDatabase

url = "https://outlook.office.com/webhook/b07c187d-c2ad-49bd-a17d-39eba101d006@9ca75128-a244-4596-877b-f24828e476e2/IncomingWebhook/5a54226a4fc54de8a4b1fc626bb8c894/b5cacced-92a8-4dd0-b61c-328924fc32fb"

sensorAdaptor = SensorAdaptor()
powerSensor = PowerSensor(sensorAdaptor)

databaseAdaptor = DatabaseAdaptor()
sensorHistory = SensorHistoryDatabase()#databaseAdaptor)

msTeamsConnector = MsTeamsConnector(url)

def checkDishwasherStatus():
    # do a sensor reading
    isMachineWorking = powerSensor.isMachineWorking()

    # check sensor history
    if not isMachineWorking:
        sensorHistory.logNotRunningEvent()
        
        hasBeenRunningRecently = sensorHistory.hasBeenRunningRecently()
        if hasBeenRunningRecently:
            msTeamsConnector.sendMessage("The machine just finished running")
            return 1
    else:
        sensorHistory.logRunningEvent()
    return 0

def main():
    messageWasSent = checkDishwasherStatus()
    if messageWasSent:
        print("Message was sent")
    else:
        print("No message was sent")


if __name__ == "__main__":
    main()