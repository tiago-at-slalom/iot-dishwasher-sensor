
from msTeamsConnector import MsTeamsConnector
from powerSensor import PowerSensor
from sensorHistoryDatabase import SensorHistoryDatabase
import config

powerSensor = PowerSensor(config.raspberryInputPin)

sensorHistory = SensorHistoryDatabase(config.lookupTime)

msTeamsConnector = MsTeamsConnector(config.teamsWebHook)

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
