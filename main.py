from object_petrinet.opnet import ObjectPNet
from object_petrinet.opnet_validator import OPNetValidator

json_input={
	"pnet1":{
	  "places": {
	    "m": {
	    	"pnet":"pnet2",
	    	"tokens":1
	    },
	    "p": 0
	  },
	  "transitions": 
	    {
	      "translation":{
		      "consume": {
		        "m": 1
		      },
		      "produce": {
		        "p": 1
		      }
	      }
	     }
	  
	},
	"pnet2":{
	  "places": {
	    "m0": 1,
	    "m1": 0,
	    "m2": 0,
	    "a":2
	  },
	  "transitions": 
	    {
	    	"elongation_step1":{
		      "consume": {
		        "m0": 1,
		        "a":1
		      },
		      "produce": {
		        "m1": 1
		      }
	      	},
	    	"elongation_step2":{
		      "consume": {
		        "m1": 1,
		        "a":1
		      },
		      "produce": {
		        "m2": 1
		      }
	      	},
	      	"translation":{
		      "consume": {
		        "m2": 1
		      },
		      "produce":{}
	    	}
		}
    }
}



OPNetValidator.validate_schema(json_input)
OPNetValidator.validate_integrity(json_input)

'''
opnet=ObjectPNet(json_input)

opnet.simulate(num_steps=1)

for pnet_name in json_input:
    pnet=json_input[pnet_name]
    places=pnet['places']
    for place_name in places:
        print(f'Tokens em PNet {pnet_name}/place {place_name}: {opnet.get_place_tokens(pnet_name=pnet_name,place_name=place_name)}')

opnet.simulate(num_steps=1)

for pnet_name in json_input:
    pnet=json_input[pnet_name]
    places=pnet['places']
    for place_name in places:
        print(f'Tokens em PNet {pnet_name}/place {place_name}: {opnet.get_place_tokens(pnet_name=pnet_name,place_name=place_name)}')
        
opnet.simulate(num_steps=1)

for pnet_name in json_input:
    pnet=json_input[pnet_name]
    places=pnet['places']
    for place_name in places:
        print(f'Tokens em PNet {pnet_name}/place {place_name}: {opnet.get_place_tokens(pnet_name=pnet_name,place_name=place_name)}')
'''