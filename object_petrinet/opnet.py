from object_petrinet.opnet2pnet import ObjectPNet2PNetAdapter
from object_petrinet.opnet_validator import OPNetValidator
from petrinet.pnet import PNet
import copy

class ObjectPNet():
    def __init__(self, opnet_dict):
        OPNetValidator.validate_schema(opnet_dict)
        OPNetValidator.validate_integrity(opnet_dict)
        self.opnet_definition=opnet_dict
        self.adapter=ObjectPNet2PNetAdapter(opnet_dict)
        self.pnet_dict=self.adapter.get_pnet_json_dict()
#        print(self.pnet_dict)
        self.pnet=PNet(self.pnet_dict)

    def get_place_tokens(self,pnet_name,place_name):
        adapted_place_name=self.adapter.get_adapted_pnet_place_name(pnet_name,place_name)
        return self.pnet.get_tokens([adapted_place_name])
    
    def get_vanilla_pnet_def(self):
        return copy.deepcopy(self.pnet_dict)
        
    def simulate(self,num_steps:int,law:str='random',handler=False):
        self.pnet.simulate_petrinet(num_steps=num_steps,law=law,handler=handler)
        