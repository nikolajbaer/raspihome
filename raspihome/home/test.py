import logging
from base import Sensor,Device

class TestActuator(Device):
    def available_actions(self):
        base = {"test":{}}
        base.update(self.cfg.get("test_actions",{}))
        return base

    def do(self,action,**kwargs):
        logging.info("Test Action %s: %s"%(action,kwargs))
        return True
        
class TestSensor(Sensor):
    def initialize(self,cfg):
        self.cfg = cfg
        self.state = 0
        self.last_update = None

    def read(self):
        return {"cfg":self.cfg,"counter":self.state}

    def do_update(self):
        self.state += 1
        self.last_update = datetime.datetime.now()
        return True

