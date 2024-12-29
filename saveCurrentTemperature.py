from appdaemon.plugins.hass import hassapi as hass
from appdaemon import adapi
from datetime import datetime

#
# UpdateEffectiveTemperature App
#
# Args:
#


class SaveCurrentTemperature(hass.Hass):
    logFilePath = "/conf/apps-data/temperature.csv"
    TIME_FORMAT = "%Y-%m-%d, %H:%M:%S"
    effectiveTempId = "input_text.heater_last_effective_temperature"
    boysTempId = "sensor.atc_220f_temperature"
    guestTempId = "sensor.atc_58fc_temperature"
    heaterSwitchId = "switch.heater_switch"
    guestFanSmartPlugSwitchId = "switch.smart_plug_1"
    
    def initialize(self):
        self.log("SaveCurrentTemperature started")
        self.run_every(self.main, "now", 5*60)
    
    def main(self, kwargs):
        try:
            time = self.datetime()
            effectiveTemp = self.get_state(self.effectiveTempId)
            boysRoomTemp = self.get_state(self.boysTempId)
            guestRoomTemp = self.get_state(self.guestTempId)
            isHeaterOn = self.get_state(self.heaterSwitchId)
            isFanOn = self.get_state(self.guestFanSmartPlugSwitchId)

            logValues = [
                time.strftime(self.TIME_FORMAT),
                effectiveTemp,
                boysRoomTemp,
                guestRoomTemp,
                isHeaterOn,
                isFanOn
            ]

            lineToSave = ','.join(logValues)+'\n'
            file = open(self.logFilePath, "a")
            file.writelines(lineToSave)
            file.close()
            
        except Exception as e:
            self.log('Something went wrong.\n{}'.format(e))