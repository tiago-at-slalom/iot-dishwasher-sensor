
from msTeamsConnector import MsTeamsConnector
from powerSensor import PowerSensor
from sensorHistoryDatabase import SensorHistoryDatabase

teamsWebHook = "https://outlook.office.com/webhook/664a924c-d306-4a91-a953-c4b555c5484e@9ca75128-a244-4596-877b-f24828e476e2/IncomingWebhook/cfb87b236f254cbfb770f070a5e1b892/b5cacced-92a8-4dd0-b61c-328924fc32fb"
lookupTime = 600 # time in seconds that we will look back in the logs history for an event to alert.
raspberryInputPin = 14

powerSensor = PowerSensor(raspberryInputPin)

sensorHistory = SensorHistoryDatabase(lookupTime)

msTeamsConnector = MsTeamsConnector(teamsWebHook)

def checkDishwasherStatus():
    # do a sensor reading
    isMachineWorking = powerSensor.isMachineWorking()

    if not isMachineWorking:
        sensorHistory.logNotRunningEvent()
        
        # check sensor history
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
