# import pymsteams
from msTeamsConnector import MsTeamsConnector
from sensorAdaptor import SensorAdaptor
from powerSensor import PowerSensor
from databaseAdaptor import DatabaseAdaptor
from sensorHistoryDatabase import SensorHistoryDatabase

url = "https://outlook.office.com/webhook/664a924c-d306-4a91-a953-c4b555c5484e@9ca75128-a244-4596-877b-f24828e476e2/IncomingWebhook/cfb87b236f254cbfb770f070a5e1b892/b5cacced-92a8-4dd0-b61c-328924fc32fb"

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
            sensorHistory.logAlertSentEvent()
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
