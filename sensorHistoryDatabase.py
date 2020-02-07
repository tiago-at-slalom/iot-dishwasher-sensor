
from time import time, ctime

class SensorHistoryDatabase:

    def hasBeenRunningRecently(self):
        nowMinusABit = time()-60

        with open('logs.log', 'r') as f:
            logLines = f.readlines()
            logLines.reverse()
            # print(logLines)

            for line in logLines:
                lineBits = line.strip().split("|")

                lineTime = int(lineBits[0])
                if lineTime < nowMinusABit:
                    print("nowMinus")
                    return False
                
                if lineBits[2] == "ALERT_SENT":
                    return False

        # TODO: this logic is wrong
        print("It has been running recently")
        return True

    def logRunningEvent(self):

        self.logEvent("MACHINE_RUNNING")
        print("MACHINE_RUNNING")

    def logNotRunningEvent(self):
        self.logEvent("MACHINE_NOT_RUNNING")
        print("MACHINE_NOT_RUNNING")

    def logEvent(self, message):
        now = time()
        nowText = ctime(now)
        with open('logs.log', 'a') as f:
            f.write('%d|%s|%s\n' % (now, nowText, message))