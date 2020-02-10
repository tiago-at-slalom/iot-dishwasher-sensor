from sensorHistoryDatabase import SensorHistoryDatabase
from mock import Mock

import mock
import unittest
import os
from callee import Regex
from time import time

class SensorHistoryDatabaseTestCase(unittest.TestCase):

    def test_whenARunningEventIsLogged(self):
        temp_mock = mock.mock_open()

        with mock.patch('sensorHistoryDatabase.open',
                    temp_mock,
                    create=True) as mock_open:
            shdb = SensorHistoryDatabase()
            shdb.logRunningEvent()
            
            mock_open().write.assert_called_once_with(Regex("[0-9]*[|]+.*[|]+MACHINE_RUNNING\\n"))

    def test_whenANotRunningEventIsLogged(self):
        temp_mock = mock.mock_open()

        with mock.patch('sensorHistoryDatabase.open',
                    temp_mock,
                    create=True) as mock_open:
            shdb = SensorHistoryDatabase()
            shdb.logNotRunningEvent()
            
            mock_open().write.assert_called_once_with(Regex("[0-9]*[|]+.*[|]+MACHINE_NOT_RUNNING\\n"))

    def test_whenAAlertSentEventIsLogged(self):
        temp_mock = mock.mock_open()

        with mock.patch('sensorHistoryDatabase.open',
                    temp_mock,
                    create=True) as mock_open:
            shdb = SensorHistoryDatabase()
            shdb.logAlertSentEvent()
            
            mock_open().write.assert_called_once_with(Regex("[0-9]*[|]+.*[|]+ALERT_SENT\\n"))

    #RUNNING, NOT_RUNNING and ALERT CASES

    def test_whenMachineNeverRun(self):
        now = time()
        data = ("%d|PrettyDate|MACHINE_NOT_RUNNING\n"
                "%d|PrettyDate|MACHINE_NOT_RUNNING\n"
                "%d|PrettyDate|MACHINE_NOT_RUNNING\n") % (now-100, now-20, now-10)
        temp_mock = mock.mock_open(read_data = data)

        with mock.patch('sensorHistoryDatabase.open',
                    temp_mock,
                    create=True) as mock_open:
            shdb = SensorHistoryDatabase()
            assert not shdb.hasBeenRunningRecently()

    def test_whenMachineNeverRunAndJustStarted(self):
        now = time()
        data = ("%d|PrettyDate|MACHINE_NOT_RUNNING\n"
                "%d|PrettyDate|MACHINE_NOT_RUNNING\n"
                "%d|PrettyDate|MACHINE_NOT_RUNNING\n") % (now-30, now-20, now-10)
        temp_mock = mock.mock_open(read_data = data)

        with mock.patch('sensorHistoryDatabase.open',
                    temp_mock,
                    create=True) as mock_open:
            shdb = SensorHistoryDatabase()
            assert not shdb.hasBeenRunningRecently()

    def test_whenMachineJustStartedRunning(self):
        now = time()
        data = ("%d|PrettyDate|MACHINE_NOT_RUNNING\n"
                "%d|PrettyDate|MACHINE_NOT_RUNNING\n"
                "%d|PrettyDate|MACHINE_RUNNING\n") % (now-100, now-20, now-10)
        temp_mock = mock.mock_open(read_data = data)

        with mock.patch('sensorHistoryDatabase.open',
                    temp_mock,
                    create=True) as mock_open:
            shdb = SensorHistoryDatabase()
            assert not shdb.hasBeenRunningRecently()

    def test_whenMachineIsRunning(self):
        now = time()
        data = ("%d|PrettyDate|MACHINE_NOT_RUNNING\n"
                "%d|PrettyDate|MACHINE_RUNNING\n"
                "%d|PrettyDate|MACHINE_RUNNING\n") % (now-100, now-20, now-10)
        temp_mock = mock.mock_open(read_data = data)

        with mock.patch('sensorHistoryDatabase.open',
                    temp_mock,
                    create=True) as mock_open:
            shdb = SensorHistoryDatabase()
            assert not shdb.hasBeenRunningRecently()

    def test_whenMachineIsNotRunningAfterBeingRunningAndAnAlertAsBeenSent(self):
        now = time()
        data = ("%d|PrettyDate|MACHINE_NOT_RUNNING\n"
                "%d|PrettyDate|MACHINE_RUNNING\n"
                "%d|PrettyDate|ALERT_SENT\n"
                "%d|PrettyDate|MACHINE_NOT_RUNNING\n") % (now-30, now-30, now-20, now-10)
        temp_mock = mock.mock_open(read_data = data)

        with mock.patch('sensorHistoryDatabase.open',
                    temp_mock,
                    create=True) as mock_open:
            shdb = SensorHistoryDatabase()
            assert not shdb.hasBeenRunningRecently()

    def test_whenMachineWasRunningAndAnAlertAsBeenSent(self):
        now = time()
        data = ("%d|PrettyDate|MACHINE_NOT_RUNNING\n"
                "%d|PrettyDate|MACHINE_NOT_RUNNING\n"
                "%d|PrettyDate|MACHINE_RUNNING\n"
                "%d|PrettyDate|ALERT_SENT\n") % (now-100, now-30, now-20, now-10)
        temp_mock = mock.mock_open(read_data = data)

        with mock.patch('sensorHistoryDatabase.open',
                    temp_mock,
                    create=True) as mock_open:
            shdb = SensorHistoryDatabase()
            assert not shdb.hasBeenRunningRecently()

    def test_whenMachineHasBeenRunning(self):
        now = time()
        data = ("%d|PrettyDate|MACHINE_RUNNING\n"
                "%d|PrettyDate|MACHINE_RUNNING\n"
                "%d|PrettyDate|MACHINE_RUNNING\n") % (now-100, now-20, now-10)
        temp_mock = mock.mock_open(read_data = data)

        with mock.patch('sensorHistoryDatabase.open',
                    temp_mock,
                    create=True) as mock_open:
            shdb = SensorHistoryDatabase()
            assert not shdb.hasBeenRunningRecently()

    def test_whenMachineIsNotRunningButWasRunningNotLongAgo(self):
        now = time()
        data = ("%d|PrettyDate|MACHINE_RUNNING\n"
                "%d|PrettyDate|MACHINE_RUNNING\n"
                "%d|PrettyDate|MACHINE_NOT_RUNNING\n") % (now-100, now-20, now-10)
        temp_mock = mock.mock_open(read_data = data)

        with mock.patch('sensorHistoryDatabase.open',
                    temp_mock,
                    create=True) as mock_open:
            shdb = SensorHistoryDatabase()
            assert shdb.hasBeenRunningRecently()

    def test_whenMachineIsNotRunningAndItRunAlreadySinceTheLastAlert(self):
        now = time()
        data = ("%d|PrettyDate|MACHINE_NOT_RUNNING\n"
                "%d|PrettyDate|ALERT_SENT\n"
                "%d|PrettyDate|MACHINE_RUNNING\n"
                "%d|PrettyDate|MACHINE_NOT_RUNNING\n") % (now-100, now-30, now-20, now-10)
        temp_mock = mock.mock_open(read_data = data)

        with mock.patch('sensorHistoryDatabase.open',
                    temp_mock,
                    create=True) as mock_open:
            shdb = SensorHistoryDatabase()
            assert shdb.hasBeenRunningRecently()

    def test_whenMachineIsNotRunningAndItRunAlreadySinceTheLastAlertWasSentSomeTimeAgo(self):
        now = time()
        data = ("%d|PrettyDate|ALERT_SENT\n"
                "%d|PrettyDate|MACHINE_RUNNING\n"
                "%d|PrettyDate|MACHINE_NOT_RUNNING\n") % (now-100, now-20, now-10)
        temp_mock = mock.mock_open(read_data = data)

        with mock.patch('sensorHistoryDatabase.open',
                    temp_mock,
                    create=True) as mock_open:
            shdb = SensorHistoryDatabase()
            assert shdb.hasBeenRunningRecently()

    def test_whenMachineIsNotRunningAndItRunSomeTimeAgo(self):
        now = time()
        data = ("%d|PrettyDate|MACHINE_RUNNING\n"
                "%d|PrettyDate|MACHINE_NOT_RUNNING\n"
                "%d|PrettyDate|MACHINE_NOT_RUNNING\n") % (now-100, now-20, now-10)
        temp_mock = mock.mock_open(read_data = data)

        with mock.patch('sensorHistoryDatabase.open',
                    temp_mock,
                    create=True) as mock_open:
            shdb = SensorHistoryDatabase()
            assert not shdb.hasBeenRunningRecently()
        

