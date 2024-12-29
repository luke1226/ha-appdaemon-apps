from appdaemon.plugins.hass import hassapi as hass
from datetime import time
from time import sleep
from datetime import datetime

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
    powerOnHours = 19
    powerOffHours = 9
    doorStateChangeSeconds = 30

    def initialize(self):
        self.log("BedroomAirCleaning app started")
        # sensor = self.get_entity(self.doorSensorId)
        # self.log("sensor:"+sensor.get_state())
        powerOnTime = time(self.powerOnHours, 0, 0)
        powerOffTime = time(self.powerOffHours, 0, 0)
        self.run_daily(self.powerOn, powerOnTime)
        self.run_daily(self.powerOff, powerOffTime)

        self.listen_state(self.doorOpened, self.doorSensorId, new="on")
        self.listen_state(self.doorClosed, self.doorSensorId, new="off")
        self.log("end of init")

    def listen_doorOpened(self):
        self.listen_state(self.doorOpened, self.doorSensorId, "on")

    def listen_doorClosed(self):
        self.listen_state(self.doorClosed, self.doorSensorId, "off")

    def powerOn(self, kwargs):
        vestfrostSwitch = self.get_entity(self.vestfrostSwitchId)
        if vestfrostSwitch.get_state() == "off":
            vestfrostLock = self.get_entity(self.vestfrostLockId)
            vestfrostAnion = self.get_entity(self.vestfrostAnionId)
            vestfrostLock.turn_off()
            vestfrostSwitch.turn_on()
            vestfrostAnion.turn_on()
            vestfrostLock.turn_on()

    def powerOff(self, kwargs):
        vestfrostSwitch = self.get_entity(self.vestfrostSwitchId)
        if vestfrostSwitch.get_state() == "on":
            vestfrostLock = self.get_entity(self.vestfrostLockId)
            vestfrostLock.turn_off()
            vestfrostSwitch.turn_off()

    def doorOpened(self, entity, attribute, old, new, kwargs):
        self.log("door opened")
        now = datetime.now().time()
        self.log("now:"+str(now))
        if now > time(self.powerOffHours, 0, 0) and now < time(self.powerOnHours, 0, 0):
            return
        
        self.log("door opened condition passed")
        sleep(self.doorStateChangeSeconds)
        entityObj = self.get_entity(entity)
        if entityObj.get_state() == "on":
            self.powerOff(kwargs)

    def doorClosed(self, entity, attribute, old, new, kwargs):
        self.log("door closed")
        now = datetime.now().time()
        self.log("now:"+str(now))
        if now > time(self.powerOffHours, 0, 0) and now < time(self.powerOnHours, 0, 0):
            return
        
        self.log("door closed condition passed")
        sleep(self.doorStateChangeSeconds)
        entityObj = self.get_entity(entity)
        if entityObj.get_state() == "off":
            self.powerOn(kwargs)