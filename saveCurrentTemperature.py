from appdaemon.plugins.hass import hassapi as hass
from appdaemon import adapi
from datetime import datetime

#
# UpdateEffectiveTemperature App
# Args:
class SaveCurrentTemperature(hass.Hass):
    logFilePath = "/conf/apps-data/temperature.csv"
    TIME_FORMAT = "%Y-%m-%d, %H:%M:%S"
    effectiveTempId = "input_text.heater_last_effective_temperature"
    groundFloorTempId = "sensor.atc_110a_temperature"
    boysTempId = "sensor.atc_220f_temperature"
    hallwayTempId = "sensor.atc_be05_temperature"
    guestTempId = "sensor.atc_58fc_temperature"
    heaterSwitchId = "switch.heater_switch"
    guestFanSmartPlugSwitchId = "switch.smart_plug_1"
    
    groundFloorHumidityId = "sensor.atc_110a_humidity"
    boysHumidityId = "sensor.atc_220f_humidity"
    guestHumidityId = "sensor.atc_58fc_humidity"
    
    def initialize(self):
        self.log("SaveCurrentTemperature started")
        self.main(self)
        self.run_every(self.main, "now", 5*60)
    def main(self, kwargs):
        try:
            time = self.datetime()
            
            effectiveTemp = self.get_state(self.effectiveTempId)
            groundFloorTemp = self.get_state(self.groundFloorTempId)
            guestRoomTemp = self.get_state(self.guestTempId)
            boysRoomTemp = self.get_state(self.boysTempId)
            hallwayTemp = self.get_state(self.hallwayTempId)
            
            groundFloorHum = self.get_state(self.groundFloorHumidityId)
            boysRoomHum = self.get_state(self.boysHumidityId)
            guestRoomHum = self.get_state(self.guestHumidityId)
            
            isHeaterOn = self.get_state(self.heaterSwitchId)
            tempJson ={
                "effective": effectiveTemp,
                "boysRoomTemp": boysRoomTemp,
                "boysRoomHum": boysRoomHum,
                "hallway": hallwayTemp,
                "guestRoomTemp": guestRoomTemp,
                "guestRoomHum": guestRoomHum,
                "groundFloorTemp": groundFloorTemp,
                "groundFloorHum": groundFloorHum
            }
            logValues = [
                time.strftime(self.TIME_FORMAT),
                str(tempJson),
                isHeaterOn
            ]
            lineToSave = ','.join(logValues)+'\n'
            file = open(self.logFilePath, "a")
            file.writelines(lineToSave)
            file.close()
            
        except Exception as e:
            self.log('Something went wrong.\n{}'.format(e))