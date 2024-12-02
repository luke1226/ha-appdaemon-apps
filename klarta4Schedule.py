from appdaemon.plugins.hass import hassapi as hass
from datetime import time

#
# Klarta4Schedule App
#
# Args:
#


class Klarta4Schedule(hass.Hass):
    klartaSwitchId = "switch.klartaf4_power"

    def initialize(self):
        self.log("Klarta4Schedule app started")
        powerOnTime = time(6, 0, 0)
        powerOffTime = time(9, 0, 0)
        self.run_daily(self.powerOn, powerOnTime)
        self.run_daily(self.powerOff, powerOffTime)
    
    def powerOn(self, kwargs):
        guestFanSmartPlugSwitch = self.get_entity(self.klartaSwitchId)
        guestFanSmartPlugSwitch.turn_on()

    def powerOff(self, kwargs):
        guestFanSmartPlugSwitch = self.get_entity(self.klartaSwitchId)
        guestFanSmartPlugSwitch.turn_off()