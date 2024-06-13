import unittest
import object_petrinet.opnet2pnet as opnet
import petrinet.pnet_validator as pnet_validator

##  python -m unittest tests/mrna_tests.py -v

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

class OPNetTests(unittest.TestCase):
    def setUp(self) -> None:
        self.opnet=opnet.ObjectPNet2PNetAdapter(json_input)
        return super().setUp()
    
    '''
    def test_rejects_invalid_encoding(self):
        with self.assertRaises(mrna.InvalidmRNASequenceEncodingException):
            self.mrna.check_aminoacid_sequence_encoding(['as'])
        with self.assertRaises(mrna.InvalidmRNASequenceEncodingException):
            self.mrna.check_aminoacid_sequence_encoding([''])
        with self.assertRaises(mrna.InvalidmRNASequenceEncodingException):
            self.mrna.check_aminoacid_sequence_encoding(['asdfd'])
    '''

    def test_generates_valid_petrinet(self):
        pnet_json_dict=self.opnet.get_pnet_json_dict()
        pnet_validator.PNetValidator.validate_schema(pnet_json_dict)
        


if __name__ == '__main__':
    unittest.main()