from appdaemon.plugins.hass import hassapi as hass
from appdaemon import adapi

#
# UpdateEffectiveTemperature App
#
# Args:
#


class UpdateEffectiveTemperature(hass.Hass):
    desiredTempId = "input_number.set_heater_temp"
    
    def initialize(self):
        self.log("UpdateEffectiveTemperature started")
        self.run_every(self.main, "now", 60)
    
    def main(self, kwargs):
        try:
            boysRoomTemp = float(self.get_state("sensor.atc_220f_temperature"))
            guestRoomTemp = float(self.get_state("sensor.atc_58fc_temperature"))
            temp = self.calculate(boysRoomTemp, guestRoomTemp)
            self.log(temp)
            effectiveTempEntity = self.get_entity("input_text.heater_last_effective_temperature")
            effectiveTempEntity.set_state(state=temp)
        except Exception as e:
            self.log('Something went wrong.\n{}'.format(e))

    def calculate(self, boysRoomTemp: float, guestRoomTemp: float):
        desiredTemp = float(self.get_state(self.desiredTempId))
        guestTempConst = 0.7
        guestRoomMinTemp = desiredTemp - guestTempConst #default 19.8
        temp = -1
        if guestRoomTemp < guestRoomMinTemp:
            temp = (boysRoomTemp + guestRoomTemp + guestTempDiffConst)/2
        elif (guestRoomTemp - boysRoomTemp > 0.3) and (guestRoomTemp > 20.5):
            temp = boysRoomTemp
        else:
            temp = boysRoomTemp
        return temp