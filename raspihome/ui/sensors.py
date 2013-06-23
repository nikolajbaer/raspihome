from base import Panel

class ReadSensorPanel(Panel):
    verbose_name = "Read Sensor"
    verbose_desc = "Reads the current value from a sensor when called"

    def _get_sensor(self):
        return self.get_item_from_facility(self.cfg.get("sensor",None))
 
    def get_data(self):
        s = self._get_sensor()
        return s and s.read() or {} #CONSIDER return error object?

class UpdateActionPanel(Panel):
    verbose_name = "Run Action"

    def _get_device(self):
        return self.get_item_from_facility(self.cfg.get("device"))

    def get_data(self):
        return self._get_device().available_actions()

    def do_update(self):
        device = self._get_device()
        if "update" in device.available_actions():
            return device.do("update")
        return False

