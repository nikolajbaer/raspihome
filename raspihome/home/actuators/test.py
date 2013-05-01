import logging

class TestActuator(object):
    def initialize(self,cfg):
        self.cfg = cfg

    def available_actions(self):
        return ["test"] + self.cfg.get("test_actions",[])

    def do(self,action,**kwargs):
        logging.info("Test Action %s: %s"%(action,kwargs))

        
