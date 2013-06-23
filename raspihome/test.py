import unittest
from home.base import Zone,Facility,Device,ZONE_SCHEME
from home.test import TestSensor,TestActuator
from ui.sensors import ReadSensorPanel,UpdateActionPanel

class BaseTest(unittest.TestCase):
    def setUp(self):
        self.facility = Facility("my_facility","My Facility") 
        self.panels = {} 
        self._build_zones()
        self._build_panels()

    def _build_panels(self):
        p = ReadSensorPanel("read",{"sensor":"/home/living/#test_sensor"},self.facility)
        self.panels["read"] = p
        p1 = UpdateActionPanel("do",{"device":"/home/living/#test_actuator"},self.facility)
        self.panels["do"] = p1

    def _build_zones(self):
        z = Zone("home","Home")
        z1 = Zone("living","Living Room")
        sensor = TestSensor()
        sensor.initialize({"x":"y"})
        actuator = TestActuator()
        actuator.initialize({"test_actions":{"update":{"x":"an int"}}})
        z1.devices["test_sensor"] = sensor
        z1.devices["test_actuator"] = actuator
        z.insert_subzone(z1)
        self.facility.add_root_zone(z)

    def test_zone_uri(self):
        # Get Zone
        self.facility._print_zonetree()
        # Test Partial
        u = "/home/living/"
        z=self.facility.get(u)
        self.assertEqual(type(z),Zone)
        # Test Absolute
        u = "%s://%s%s"%(ZONE_SCHEME,self.facility.id,u)
        z=self.facility.get(u)
        self.assertEqual(type(z),Zone)

    def test_device_uri(self):
        # Get Zone
        self.facility._print_zonetree()
        # Test Partial
        u = "/home/living/#test_sensor"
        s=self.facility.get(u)
        self.assertEqual(type(s),TestSensor)
        # Test Absolute
        u = "%s://%s%s"%(ZONE_SCHEME,self.facility.id,u)
        s=self.facility.get(u)
        self.assertEqual(type(s),TestSensor)

    def test_sensor_read(self):
        u = "%s://%s/home/living/#test_sensor"%(ZONE_SCHEME,self.facility.id)
        s = self.facility.get(u)
        self.assertEqual(s.read()["cfg"]["x"],"y")

    def test_panel_read(self):
        d = self.panels["read"].get_data()
        v = self.facility.get(self.panels["read"].cfg["sensor"])
        self.assertEqual(d,v.read())

    def test_panel_do(self):
        # NOTE: test HTTP integration elsewhere
        p = self.panels["do"]
        actions = p.get_data()
        print "ACTIONS",actions
        self.assertTrue(p.do_update())

if __name__=="__main__":
    unittest.main()


