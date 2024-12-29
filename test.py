from appdaemon.plugins.hass import hassapi as hass
from datetime import datetime

#
# Test App
#
# Args:
#


class Test(hass.Hass):
    def initialize(self):
        forecast = self.get_entity("weather.forecast_home")
        outdoorTemperature = self.get_entity("input_text.outdoor_temperature")
        outdoorTemperature.set_state(state=str(forecast.attributes["temperature"]))