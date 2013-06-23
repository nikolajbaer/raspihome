from base import Panel

class TestSensorPanel(Panel):
    def get_data(self):
        return {"Test":"OK"}

    def action_test(self,**kwargs):
        return {"Test":"OK","kwargs":kwargs}

class ReadSensor(Panel):
    def _get_sensor(self):
        return self.get_item_from_facility(self.cfg.get("sensor",None))
 
    def get_data(self):
        s = self._get_sensor()
        return s and s.read() or {} #CONSIDER return error object?

