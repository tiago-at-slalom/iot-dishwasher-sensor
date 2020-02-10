
from time import time, ctime

class SensorHistoryDatabase:

    def hasBeenRunningRecently(self):
        nowMinusABit = time()-60 # TODO: make this value configurable without breaking the tests

        with open('logs.log', 'r') as f:
            logLines = f.readlines()
            logLines.reverse()
            # print(logLines)

            firstLine = logLines[0].strip().split("|")
            lineTime = int(firstLine[0])
            if firstLine[2] == "MACHINE_NOT_RUNNING":
                for line in logLines[1:]:
                    lineBits = line.strip().split("|")

                    lineTime = int(lineBits[0])
                    if lineTime < nowMinusABit:
                        print("nowMinus")
                        break
                    
                    if lineBits[2] == "ALERT_SENT":
                        break
                    
                    if lineBits[2] == "MACHINE_RUNNING":
                        print("It has been running recently")
                        return True

        return False

    def logRunningEvent(self):
        self.logEvent("MACHINE_RUNNING")

    def logNotRunningEvent(self):
        self.logEvent("MACHINE_NOT_RUNNING")

    def logAlertSentEvent(self):
        self.logEvent("ALERT_SENT")

    def logEvent(self, message):
        now = time()
        nowText = ctime(now)
        with open('logs.log', 'a') as f:
            f.write('%d|%s|%s\n' % (now, nowText, message))
        
        print(message)