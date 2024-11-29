from appdaemon.plugins.hass import hassapi as hass
from datetime import datetime

#
# ControlHeater App
#
# Args:
#


class ControlHeater(hass.Hass):
    def initialize(self):
        self.log("ControlHeater app started")
        self.run_every(self.main, "now", 1*60)
    
    def main(self, kwargs):
        try:
            time = self.datetime()
            isTurnOn = self.get_state("switch.heater_switch") == "on"
            effectiveTemp = float(self.get_state("input_text.heater_last_effective_temperature"))
            desiredTemp = float(self.get_state("input_number.set_heater_temp"))
            desiredMinTemp = desiredTemp - 0.1
            desiredMaxTemp = desiredTemp + 0.2
    
            if effectiveTemp < desiredMinTemp:
                if isTurnOn==False:
                    self.log("heater is turning on")
            elif effectiveTemp > desiredMaxTemp:
                if isTurnOn==True:
                    self.log("heater is turning off")
            else:
                self.log("temperature ok")

            self.logStateToFile(time, effectiveTemp, isTurnOn)
        except Exception as e:
            self.log('Something went wrong.\n{}'.format(e))

    def logStateToFile(self, time: datetime, effectiveTemp: float, isTurnOff: bool):
        logFilePath = "/conf/apps-data/heater.csv"
        
        boysRoomTemp = float(self.get_state("sensor.atc_220f_temperature"))
        guestRoomTemp = float(self.get_state("sensor.atc_58fc_temperature"))

        tempJson ={
            "effective": effectiveTemp,
            "boysRoom": boysRoomTemp,
            "guestRoom": guestRoomTemp
        }
        isTurnOffStr = "on" if isTurnOff else "off"
        values = [
            time.strftime("%Y-%m-%d, %H:%M:%S"),
            str(tempJson),
            isTurnOffStr
            ]
        
        lineToSave = ','.join(values)+'\n'
        file = open(logFilePath, "a")
        file.writelines(lineToSave)
        file.close()