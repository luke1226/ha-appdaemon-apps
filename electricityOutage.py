from appdaemon.plugins.hass import hassapi as hass
from datetime import datetime

#
# ElectricityOutage App
#
# Args:
#


class ElectricityOutage(hass.Hass):
    def initialize(self):
        a = 1
        handle = self.listen_log(self.a, 'WARNING')
        # self.main(kwargs=any)
        #self.log("ElectricityOutage app started")
        #self.log("listening for log")
        #self.main(kwargs=any)
        #self.run_every(self.main, "now", 1*60)
        # electricityWorksInput = self.get_entity("input_boolean.home_electricity_state")
        # electricityWorksInput.turn_on()

    def main(self, kwargs):
        # handle = self.listen_log(self.a, 'WARNING')
        electricityWorksInput = self.get_entity("input_boolean.home_electricity_state")
        try:
             button = self.get_entity("button.electricityoutagesensor_identify")
             button.call_service("press")
             electricityWorksInput.turn_on() 
             self.log("electricity works")
        except Exception as e:
            self.log('Something went wrong.\n{}'.format(e))
            electricityWorksInput.turn_off()
            self.log("no electricity")
        finally: 
            print('')
            
    def a(self, name, ts, level, type, message, kwargs):
        self.log("a")
        