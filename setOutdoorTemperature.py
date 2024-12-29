from appdaemon.plugins.hass import hassapi as hass
from datetime import datetime

#
# SetOutdoorTemperature App
#
# Args:
#


class SetOutdoorTemperature(hass.Hass):
    def initialize(self):
        #forecast = self.get_entity("weather.forecast_home")
        #self.log(str(forecast.attributes))
        self.run_every(self.main, "now", 30*60)

    def main(self, kwargs):
        forecast = self.get_entity("weather.forecast_home")
        outdoorTemperature = self.get_entity("input_text.outdoor_temperature")
        outdoorTemperature.set_state(state=str(forecast.attributes["temperature"]))