from object_petrinet.opnet2pnet import ObjectPNet2PNetAdapter
from petrinet.pnet import PNet

class ObjectPNet():
    def __init__(self, opnet_dict):
        self.opnet_definition=opnet_dict
        self.adapter=ObjectPNet2PNetAdapter(opnet_dict)
        self.pnet_dict=self.adapter.get_pnet_json_dict()
#        print(self.pnet_dict)
        self.pnet=PNet(self.pnet_dict)

    def get_place_tokens(self,pnet_name,place_name):
        adapted_place_name=self.adapter.get_adapted_pnet_place_name(pnet_name,place_name)
        return self.pnet.get_tokens([adapted_place_name])
        
    def simulate(self,num_steps:int,law:str='random',handler=False):
        self.pnet.simulate_petrinet(num_steps=num_steps,law=law,handler=handler)
        