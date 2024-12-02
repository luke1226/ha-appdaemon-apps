from appdaemon.plugins.hass import hassapi as hass
from datetime import datetime
import time

#
# ElectricityOutage App
#
# Args:
#


class ElectricityOutage(hass.Hass):
    electricityStateId = "input_boolean.home_electricity_state"

    def initialize(self):
        a = 1
        #handle = self.listen_log(self.a, 'WARNING')
        # self.main(kwargs=any)
        #self.log("ElectricityOutage app started")
        #self.log("listening for log")
        #self.main(kwargs=any)
        self.run_every(self.main, "now", 1*60)
        # electricityWorksInput = self.get_entity("input_boolean.home_electricity_state")
        # electricityWorksInput.turn_on()

    def main(self, kwargs):
        try:
            electricityWorksInput = self.get_entity(self.electricityStateId)
            button = self.get_entity("button.electricityoutagesensor_identify")
            start_time = time.time()
            button.call_service("press", return_result=True)
            timeOfExecution = time.time() - start_time
            self.log("time:"+str(timeOfExecution))

            if timeOfExecution < 10:
                electricityWorksInput.turn_on()
                self.log("electricity works")
            else:
                electricityWorksInput.turn_off()
                self.log("no electricity")

        except Exception as e:
            self.log('Something went wrong.\n{}'.format(e))

        