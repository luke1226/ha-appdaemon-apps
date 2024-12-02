from appdaemon.plugins.hass import hassapi as hass
from datetime import datetime

#
# Test App
#
# Args:
#


class Test(hass.Hass):
    def initialize(self):
        self.log("Test app started")
        # heaterSwitch = self.get_entity("switch.heater_switch")
        # heaterSwitch.set_state(state=False)
        self.set_log_level("INFO")
        self.log("aaaa")

    #     self.listen_log(self.cb)

    # def cb(self, name, ts, level, message):
    #     msg = "{}: {}: {}: {}".format(ts, level, name, message)
    #     self.call_service("python_script/log",   message = msg)