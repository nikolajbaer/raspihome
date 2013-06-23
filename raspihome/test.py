import unittest
from home.base import Zone,Facility,Device,ZONE_SCHEME
from home.test import TestSensor,TestActuator

class BaseTest(unittest.TestCase):
    def setUp(self):
        self.facility = Facility("my_facility","My Facility") 
        self.build_zones()

    def build_zones(self):
        z = Zone("home","Home")
        z1 = Zone("living","Living Room")
        sensor = TestSensor()
        sensor.initialize({"x":"y"})
        actuator = TestActuator()
        actuator.initialize({"test_actions":{"do_something":{"x":"an int"}}})
        z1.devices["test_sensor"] = sensor
        z1.devices["test_actuator"] = actuator
        z.insert_subzone(z1)
        self.facility.add_root_zone(z)

    def test_zone_uri(self):
        # Get Zone
        self.facility._print_zonetree()
        u = "%s://%s/home/living/"%(ZONE_SCHEME,self.facility.id)
        z=self.facility.get(u)
        self.assertEqual(type(z),Zone)

    def test_device_uri(self):
        # Get Zone
        self.facility._print_zonetree()
        u = "%s://%s/home/living/#test_sensor"%(ZONE_SCHEME,self.facility.id)
        z=self.facility.get(u)
        self.assertEqual(type(z),TestSensor)
        

if __name__=="__main__":
    unittest.main()


