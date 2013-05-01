import loggin
import datetime

class TestSensor(object):
    def initialize(self,cfg):
        self.cfg = cfg
        self.state = 0
        self.last_update = None

    def read(self):
        return {"cfg":self.cfg,"counter":self.state}

    def update(self):
        self.state += 1
        self.last_update = datetime.datetime.now()

    def get_last_update(self):
        return self.last_update
