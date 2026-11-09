from appdaemon.plugins.hass import hassapi as hass
from appdaemon import adapi

#
# UpdateEffectiveTemperature App
#
# Args:
#


class UpdateEffectiveTemperature(hass.Hass):
    desiredTempId = "input_number.set_heater_temp"
    currentAverageTemperatureId = "input_text.heater_current_average_temperature"
    effectiveTemperatureId = "input_text.heater_last_effective_temperature"
    groundFloorTempRatio = 0.8
    groundFloorTempOver21Ratio = 0.2
    
    def initialize(self):
        self.log("UpdateEffectiveTemperature started")
        self.main(self)
        self.run_every(self.main, "now", 60)
        #self.main(self)
    
    def main(self, kwargs):
        try:
            self.log("calculating temperature")

            groundFloorTempStr = self.get_state("sensor.atc_110a_temperature")
            boysRoomTemp = float(self.get_state("sensor.atc_220f_temperature"))
            guestRoomTemp = float(self.get_state("sensor.atc_58fc_temperature"))
            hallwayTemp = float(self.get_state("sensor.atc_be05_temperature"))
            groundFloorTemp = float(groundFloorTempStr if groundFloorTempStr != 'unavailable' else -1)
            outdoorTemp = float(self.get_state("sensor.outdoor_temperature"))

            temp = self.calculate(boysRoomTemp, guestRoomTemp, hallwayTemp, groundFloorTemp, outdoorTemp)
            self.log('current temp='+format(temp, 'f'))
            currentAverageTempEntity = self.get_entity(self.currentAverageTemperatureId)
            currentAverageTempEntity.set_state(state=temp)

            outdoorTempRatio = 0
            if outdoorTemp < 2.5: outdoorTempRatio = 0.05 + (2.5-outdoorTemp)*0.01
            effectiveTemp = temp-outdoorTempRatio
            effectiveTempEntity = self.get_entity(self.effectiveTemperatureId)
            effectiveTempEntity.set_state(state=effectiveTemp)

        except Exception as e:
            self.log('Something went wrong.\n{}'.format(e))

    def calculate(self, boysRoomTemp: float, guestRoomTemp: float, hallwayTemp: float, groundFloorTemp: float, outdoorTemp: float):
        effectiveGroundFloorTempRatio = self.groundFloorTempRatio
        effectiveGuestRoomTempRatio = 0.8
        
        if groundFloorTemp > 21.0: effectiveGroundFloorTempRatio = self.groundFloorTempOver21Ratio
        elif groundFloorTemp < boysRoomTemp: effectiveGroundFloorTempRatio = 1.1
        elif groundFloorTemp == -1.0 : effectiveGroundFloorTempRatio = 0
        
        firstFloorRoomsTempRatio = (2 - effectiveGuestRoomTempRatio)/2.0
        self.log('firstFloorRoomsTempRatio='+format(firstFloorRoomsTempRatio, 'f'))
                    
        firstFloorTemp = ((boysRoomTemp*(2-effectiveGuestRoomTempRatio)) + (guestRoomTemp*effectiveGuestRoomTempRatio))/2
        temp = ((firstFloorTemp*(2-effectiveGroundFloorTempRatio)) + (groundFloorTemp*effectiveGroundFloorTempRatio))/2
        
        return temp