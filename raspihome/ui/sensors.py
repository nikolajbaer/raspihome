from base import Panel

class TestSensorPanel(Panel):
    def get_data(self):
        return {"Test":"OK"}

    def action_test(self,**kwargs):
        return {"Test":"OK","kwargs":kwargs}


