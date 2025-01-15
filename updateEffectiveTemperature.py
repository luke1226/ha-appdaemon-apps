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
    guestTempRatio = 1.1
    guestTempRatio20 = 1.4
    
    def initialize(self):
        self.log("UpdateEffectiveTemperature started")
        self.run_every(self.main, "now", 60)
    
    def main(self, kwargs):
        try:
            boysRoomTemp = float(self.get_state("sensor.atc_220f_temperature"))
            guestRoomTemp = float(self.get_state("sensor.atc_58fc_temperature"))
            hallwayTemp = float(self.get_state("sensor.atc_be05_temperature"))
            outdoorTemp = float(self.get_state("sensor.outdoor_temperature"))

            temp = self.calculate(boysRoomTemp, guestRoomTemp, hallwayTemp, outdoorTemp)
            self.log(temp)
            currentAverageTempEntity = self.get_entity(self.currentAverageTemperatureId)
            currentAverageTempEntity.set_state(state=temp)

            outdoorTempRatio = 0
            if outdoorTemp < 2.5: outdoorTempRatio = 0.1 + (2.5-outdoorTemp)*0.01
            effectiveTemp = temp-outdoorTempRatio
            effectiveTempEntity = self.get_entity(self.effectiveTemperatureId)
            effectiveTempEntity.set_state(state=effectiveTemp)

        except Exception as e:
            self.log('Something went wrong.\n{}'.format(e))

    def calculate(self, boysRoomTemp: float, guestRoomTemp: float, hallwayTemp: float, outdoorTemp: float):
        #desiredTemp = float(self.get_state(self.desiredTempId))
        effectiveGuestTempRatio = self.guestTempRatio
        temp = -1
        effectiveBoysRoomTemp = max([boysRoomTemp, hallwayTemp])

        #if effectiveBoysRoomTemp - guestRoomTemp > 0.8 and guestRoomTemp < 20.25:
        #    effectiveGuestTempRatio = 1.6
        #elif guestRoomTemp < 20.25:
        #    effectiveGuestTempRatio = self.guestTempRatio20
        
        if (guestRoomTemp - effectiveBoysRoomTemp > 0.3) and (guestRoomTemp > 20.5):
            effectiveGuestTempRatio = 0.9
        
        temp = (effectiveBoysRoomTemp*(2-effectiveGuestTempRatio) + guestRoomTemp*effectiveGuestTempRatio)/2

        return temp