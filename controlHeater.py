from appdaemon.plugins.hass import hassapi as hass
from datetime import datetime

#
# ControlHeater App
#
# Args:
#


class ControlHeater(hass.Hass):
    TIME_FORMAT = "%Y-%m-%d, %H:%M:%S"
    heaterSwitchId = "switch.heater_switch"
    guestFanSmartPlugSwitchId = "switch.smart_plug_1"
    groundFloorFanSmartPlugSwitchId = "switch.electricityoutagesensor_switch"
    boysRoomFanPowerPlugId = "switch.powerplug3"

    def initialize(self):
        self.log("ControlHeater app started")
        self.run_every(self.main, "now", 15*60)
        self.main(self)
    
    def main(self, kwargs):
        try:
            time = self.datetime()
            isTurnOn = self.get_state("switch.heater_switch") == "on"
            isFanTurnOn = self.get_state("switch.smart_plug_1") == "on"
            isAutoFanActive = self.get_state("input_boolean.heater_fan1_toggle") == "on"

            heaterTurnOnNeeded = self.calculateIfNeeded(isTurnOn)
            if heaterTurnOnNeeded == True:
                self.log("turning on")
                self.turnOnHeater(time, isTurnOn=isTurnOn, isFanTurnOn=isFanTurnOn, isAutoFanActive=isAutoFanActive)
            else:
                self.log("turning off")
                self.turnOffHeater(time, isTurnOn=isTurnOn, isFanTurnOn=isFanTurnOn)
                
        except Exception as e:
            self.log('Something went wrong.\n{}'.format(e))

    def calculateIfNeeded(self, isTurnOn: bool):
        desiredMin = 0.1
        desiredMax = 0.2
        
        desiredGroundFloorTemp = 21.0
        desiredBoysRoomTemp = 20.7
        desiredGuestRoomTemp = 19.8
        
        groundFloorTemp = self.getTemp("sensor.termometer6_temperature")
        boysRoomTemp = self.getTemp("sensor.atc_220f_temperature")
        guestRoomTemp = self.getTemp("sensor.atc_58fc_temperature")
        
        if isTurnOn:
            if groundFloorTemp > (desiredGroundFloorTemp + desiredMax) and boysRoomTemp > (desiredBoysRoomTemp + desiredMax) and guestRoomTemp > (desiredGuestRoomTemp + desiredMax): return False
            return True
        else:
            if groundFloorTemp < (desiredGroundFloorTemp - desiredMin): return True
            elif boysRoomTemp < (desiredBoysRoomTemp - desiredMin): return True
            elif guestRoomTemp < (desiredGuestRoomTemp - desiredMin): return True
        
        return False
        
    def getTemp(self, entity_id):
        val = self.get_state(entity_id)
        if val in {None, 'unavailable', 'unknown', '', 'none', 'null'}:
            return 99.0
        try:
            return float(val)
        except (ValueError, TypeError):
            return 99.0

    def turnOnHeater(self, time: datetime, isTurnOn:bool, isFanTurnOn:bool, isAutoFanActive:bool):
        self.log("case1")
        if isTurnOn==False:
            self.log("heater is turning on")
            heaterSwitch = self.get_entity(self.heaterSwitchId)
            heaterSwitch.turn_on()
            
            lastTurnOnInput = self.get_entity("input_text.heater_last_turn_on")
            lastTurnOnInput.set_state(state=time.strftime(self.TIME_FORMAT))
            self.logStateToFile(time, True)

        if isFanTurnOn==False and isAutoFanActive:
            self.log("heater fans are turning on")
            self.run_in(self.turnOnFan, 5*60)
    
    def turnOnFan(self, kwargs):
        guestFanSmartPlugSwitch = self.get_entity(self.guestFanSmartPlugSwitchId)
        groundFloorFanSmartPlugSwitch = self.get_entity(self.groundFloorFanSmartPlugSwitchId)
        boysRoomFanPowerPlug = self.get_entity(self.boysRoomFanPowerPlugId)
        guestFanSmartPlugSwitch.turn_on()
        groundFloorFanSmartPlugSwitch.turn_on()
        boysRoomFanPowerPlug.turn_on()
        #guestFan2SmartPlugSwitch.turn_on()
        self.log("fan turned on")
        
    def turnOffHeater(self, time: datetime, isTurnOn:bool, isFanTurnOn:bool):
        self.log("case2")
        if isTurnOn==True:
            self.log("heater is turning off")
            heaterSwitch = self.get_entity(self.heaterSwitchId)
            heaterSwitch.turn_off()
            lastTurnOffInput = self.get_entity("input_text.heater_last_turn_off")
            lastTurnOffInput.set_state(state=time.strftime(self.TIME_FORMAT))
            self.logStateToFile(time, False)

        if isFanTurnOn==True:
            self.log("heater fans are turning off")
            self.run_in(self.turnOffFan, 15*60)

    def turnOffFan(self, kwargs):
        guestFanSmartPlugSwitch = self.get_entity(self.guestFanSmartPlugSwitchId)
        groundFloorFanSmartPlugSwitch = self.get_entity(self.groundFloorFanSmartPlugSwitchId)
        boysRoomFanPowerPlug = self.get_entity(self.boysRoomFanPowerPlugId)
        guestFanSmartPlugSwitch.turn_off()
        groundFloorFanSmartPlugSwitch.turn_off()
        boysRoomFanPowerPlug.turn_off()
        #guestFan2SmartPlugSwitch.turn_off()
        self.log("fan turned off")

    def logStateToFile(self, time: datetime, isTurnOn: bool):
        logFilePath = "/conf/apps-data/heater.csv"
        
        groundFloorTemp = self.getTemp("sensor.termometer6_temperature")
        boysRoomTemp = self.getTemp("sensor.atc_220f_temperature")
        guestRoomTemp = self.getTemp("sensor.atc_58fc_temperature")

        tempJson ={
            "groundFloor": groundFloorTemp,
            "boysRoom": boysRoomTemp,
            "guestRoom": guestRoomTemp
        }
        isTurnOnStr = "on" if isTurnOn else "off"
        values = [
            time.strftime(self.TIME_FORMAT),
            str(tempJson),
            isTurnOnStr
            ]
        
        lineToSave = ','.join(values)+'\n'
        file = open(logFilePath, "a")
        file.writelines(lineToSave)
        file.close()