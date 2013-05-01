from raspihome.home import Sensor

class SNMPWifiClients(Sensor):
    def get_state(self):
        pass

    def initialize(self,cfg):
        super(SNMPWifiClients,self).__init__(cfg)
        self.clients = {}
        self.host = cfg["host"]

    def update(self):
        # TODO ping SNMP to grab all wifi clients
        # store by clients[MAC]={ip}
        pass

