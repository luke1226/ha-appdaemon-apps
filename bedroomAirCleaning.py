from appdaemon.plugins.hass import hassapi as hass
from datetime import time
import threading

#
# BedroomAirCleaning App
#
# Args:
#


class BedroomAirCleaning(hass.Hass):
    vestfrostSwitchId = "switch.vestfrost_power"
    vestfrostLockId = "switch.vestfrost_lock"
    vestfrostAnionId = "switch.vestfrost_anion"
    doorSensorId = "binary_sensor.contactsensor_opening"

    def initialize(self):
        self.log("BedroomAirCleaning app started")
        powerOnTime = time(19, 0, 0)
        powerOffTime = time(9, 0, 0)
        self.log("BedroomAirCleaning app started")
        #thread1 = threading.Thread(target=self.run_daily_powerOn)
        self.log("BedroomAirCleaning app started")

        #thread1.start()
        #thread2 = threading.Thread(target=self.run_daily(self.powerOff, powerOffTime))
        self.run_daily(self.powerOn, powerOnTime)
        self.run_daily(self.powerOff, powerOffTime)
        self.log("end of run daily")
        thread1 = threading.Thread(target=self.listen_doorOpened)
        thread2 = threading.Thread(target=self.listen_doorClosed)

        thread1.start()
        thread2.start()
        #self.listen_state(self.doorOpened, self.doorSensorId, "on")
        #self.listen_state(self.doorClosed, self.doorSensorId, "off")
        self.log("end of init")

    def listen_doorOpened(self):
        self.listen_state(self.doorOpened, self.doorSensorId, "on")

    def listen_doorClosed(self):
        self.listen_state(self.doorClosed, self.doorSensorId, "off")

    def powerOn(self, kwargs):
        vestfrostSwitch = self.get_entity(self.vestfrostSwitchId)
        vestfrostLock = self.get_entity(self.vestfrostLockId)
        vestfrostAnion = self.get_entity(self.vestfrostAnionId)
        vestfrostLock.turn_off()
        vestfrostSwitch.turn_on()
        vestfrostAnion.turn_on()
        vestfrostLock.turn_on()

    def powerOff(self, kwargs):
        vestfrostSwitch = self.get_entity(self.vestfrostSwitchId)
        vestfrostLock = self.get_entity(self.vestfrostLockId)
        vestfrostLock.turn_off()
        vestfrostSwitch.turn_off()

    def doorOpened(self, kwargs):
        self.log("door opened")

    def doorClosed(self, kwargs):
        self.log("door closed")