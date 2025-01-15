from appdaemon.plugins.hass import hassapi as hass
from appdaemon import adapi
from datetime import time
from datetime import datetime
import pytz

#
# SetDesiredTemperature App
#
# Args:
#


class SetDesiredTemperature(hass.Hass):
    desiredTempId = "input_number.set_heater_temp"
    
    def initialize(self):
        self.log("SetDesiredTemperature started")
        self.run_every(self.main, "now", 5*60)
    
    def main(self, kwargs):
        try:
            desiredTempEntity = self.get_entity(self.desiredTempId)
            isTurnOn = self.get_state("switch.heater_switch") == "on"
            lowerTempOnTime = time(23, 0, 0)
            lowerTempOffTime = time(5, 0, 0)
            now = datetime.now(pytz.timezone('Europe/Warsaw')).time()
            #isTurnOn = True
            temp = 20.4
            self.log('now: ' + str(now))
            if isTurnOn and (now > lowerTempOnTime or now < lowerTempOffTime):
                temp = 19.8

            self.log('Desired temp: '+str(temp))

            if temp != float(desiredTempEntity.get_state()):
                desiredTempEntity.set_state(state=temp)
                self.log('Desired temp updated: '+str(temp))

        except Exception as e:
            self.log('Something went wrong.\n{}'.format(e))