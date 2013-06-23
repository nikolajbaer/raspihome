from home.base import Sensor
import os

# TODO: make this more secure and cross platform (e.g. bsd and linux)
class RaspihomeServer(Sensor):
    def read(self):
        return {"uptime":os.popen("uptime").read()}

