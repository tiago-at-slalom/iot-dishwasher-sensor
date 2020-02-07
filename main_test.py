from main import checkDishwasherStatus

import mock
import unittest

class MainTestCase(unittest.TestCase):

    @mock.patch('main.powerSensor')
    @mock.patch('main.sensorHistory')
    @mock.patch('main.msTeamsConnector')
    def test_whenMachineIsRunning(self, mock_msTeams, mock_sensorHistory, mock_powerSensor):
        mock_powerSensor.isMachineWorking.return_value = True
        
        result = checkDishwasherStatus()
        
        assert not mock_msTeams.sendMessage.called
        assert mock_sensorHistory.logRunningEvent.called
        assert not result

    @mock.patch('main.powerSensor')
    @mock.patch('main.sensorHistory')
    @mock.patch('main.msTeamsConnector')
    def test_whenMachineIsNotRunningAndHasNotBeenWorking(self, mock_msTeams, mock_sensorHistory, mock_powerSensor):
        mock_powerSensor.isMachineWorking.return_value = False
        mock_sensorHistory.hasBeenRunningRecently.return_value = False
        
        result = checkDishwasherStatus()
        
        assert not mock_msTeams.sendMessage.called
        assert not mock_sensorHistory.logRunningEvent.called
        assert mock_sensorHistory.logNotRunningEvent.called
        assert not result

    @mock.patch('main.powerSensor')
    @mock.patch('main.sensorHistory')
    @mock.patch('main.msTeamsConnector')
    def test_whenMachineIsNotRunningButHasBeenWorking(self, mock_msTeams, mock_sensorHistory, mock_powerSensor):
        mock_powerSensor.isMachineWorking.return_value = False
        mock_sensorHistory.hasBeenRunningRecently.return_value = True
        
        result = checkDishwasherStatus()
        
        assert mock_powerSensor.isMachineWorking.was_called
        assert mock_msTeams.sendMessage.called
        assert not mock_sensorHistory.logRunningEvent.called
        assert mock_sensorHistory.logNotRunningEvent.called
        assert result