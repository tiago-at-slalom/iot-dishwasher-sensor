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

    def test_whenMachineHasBeenRunningRecently(self):
        now = time()
        data = ("%d|PrettyDate|MACHINE_RUNNING\n"
                "%d|PrettyDate|MACHINE_RUNNING\n") % (now-2000, now-1000)
        temp_mock = mock.mock_open(read_data = data)

        with mock.patch('sensorHistoryDatabase.open',
                    temp_mock,
                    create=True) as mock_open:
            shdb = SensorHistoryDatabase()
            assert shdb.hasBeenRunningRecently()

    def test_whenMachineHasNotBeenRunningRecently(self):
        now = time()
        data = ("%d|PrettyDate|MACHINE_RUNNING\n"
                "%d|PrettyDate|MACHINE_RUNNING\n") % (now-2000000, now-10000000)
        temp_mock = mock.mock_open(read_data = data)

        with mock.patch('sensorHistoryDatabase.open',
                    temp_mock,
                    create=True) as mock_open:
            shdb = SensorHistoryDatabase()
            assert not shdb.hasBeenRunningRecently()

    def test_whenMachineFinishHasBeenProcessedRecently(self):
        now = time()
        data = ("%d|PrettyDate|ALERT_SENT\n"
                "%d|PrettyDate|MACHINE_RUNNING\n") % (now-2000, now-1000)
        temp_mock = mock.mock_open(read_data = data)

        with mock.patch('sensorHistoryDatabase.open',
                    temp_mock,
                    create=True) as mock_open:
            shdb = SensorHistoryDatabase()
            assert not shdb.hasBeenRunningRecently()
        

