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

    def initialize(self):
        self.log("ControlHeater app started")
        self.run_every(self.main, "now", 15*60)
    
    def main(self, kwargs):
        try:
            time = self.datetime()
            isTurnOn = self.get_state("switch.heater_switch") == "on"
            effectiveTemp = float(self.get_state("input_text.heater_last_effective_temperature"))
            desiredTemp = float(self.get_state("input_number.set_heater_temp"))
            desiredMinTemp = desiredTemp - 0.1
            desiredMaxTemp = desiredTemp + 0.2
            isAutoFanActive = self.get_state("input_boolean.heater_fan1_toggle") == "on"
            # self.turnOnHeater(time, effectiveTemp, isTurnOn=False, isAutoFanActive=False)
            # self.turnOffHeater(time, effectiveTemp, isTurnOn=True)
            # return

            if effectiveTemp < desiredMinTemp:
                self.turnOnHeater(time, effectiveTemp, isTurnOn=isTurnOn, isAutoFanActive=isAutoFanActive)
            elif effectiveTemp > desiredMaxTemp:
                self.turnOffHeater(time, effectiveTemp, isTurnOn=isTurnOn)
            else:
                self.log("temperature ok")
        except Exception as e:
            self.log('Something went wrong.\n{}'.format(e))

    def turnOnHeater(self, time: datetime, effectiveTemp: float, isTurnOn:bool, isAutoFanActive:bool):
        self.log("case1")
        guestFanSmartPlugSwitch = self.get_entity(self.guestFanSmartPlugSwitchId)
        if isTurnOn==False:
            self.log("heater is turning on")
            heaterSwitch = self.get_entity(self.heaterSwitchId)
            heaterSwitch.turn_on()
            if isAutoFanActive:
                guestFanSmartPlugSwitch.turn_on()
            
            lastTurnOnInput = self.get_entity("input_text.heater_last_turn_on")
            lastTurnOnInput.set_state(state=time.strftime(self.TIME_FORMAT))
            self.logStateToFile(time, effectiveTemp, True)

    def turnOffHeater(self, time: datetime, effectiveTemp: float, isTurnOn:bool):
        self.log("case2")
        if isTurnOn==True:
            self.log("heater is turning off")
            heaterSwitch = self.get_entity(self.heaterSwitchId)
            heaterSwitch.turn_off()
            lastTurnOffInput = self.get_entity("input_text.heater_last_turn_off")
            lastTurnOffInput.set_state(state=time.strftime(self.TIME_FORMAT))
            self.logStateToFile(time, effectiveTemp, False)
            self.run_in(self.turnOffFan, 10*60)

    def turnOffFan(self, kwargs):
        guestFanSmartPlugSwitch = self.get_entity(self.guestFanSmartPlugSwitchId)
        guestFanSmartPlugSwitch.turn_off()
        self.log("fan turned off")

    def logStateToFile(self, time: datetime, effectiveTemp: float, isTurnOn: bool):
        logFilePath = "/conf/apps-data/heater.csv"
        
        boysRoomTemp = float(self.get_state("sensor.atc_220f_temperature"))
        guestRoomTemp = float(self.get_state("sensor.atc_58fc_temperature"))

        tempJson ={
            "effective": effectiveTemp,
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