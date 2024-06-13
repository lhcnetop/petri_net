import unittest
import mrna.mrna2pnet as mrna
import petrinet.pnet_validator as pnet_validator

##  python -m unittest tests/mrna_tests.py -v

json_input={
    "chains":[
        {
            "name":"chainA",
            "sequence":["Gly","Ile","Val","Glu","Gln","Cys","Thr","Ser","Ile","Cys","Ser","Leu","Tyr","Gln","Leu","Glu","Asn","Tyr","Cys","Asn"],
            "polipeptide_name":"preprotoinsulin_A_chain"
        },
        {
            "name":"chainB",
            "sequence":["Phe","Val","Asn","Gln","His","Leu","Cys","Gly","Ser","His","Leu","Val","Glu","Ala","Leu","Tyr","Leu","Val","Cys","Gly","Glu","Arg","Gly","Phe","Phe","Tyr","Thr","Pro","Lys","Ala"],
            "polipeptide_name":"preprotoinsulin_B_chain"
        }
    ],
    "simulation_parameters":{
        "initial_chains_marking":120,
        "max_protein_output_goal":100,
        "excess_aminoacids_factor":1
    }
}

class mRNATests(unittest.TestCase):
    def setUp(self) -> None:
        self.mrna=mrna.mRNA2PNetAdapter(json_input)
        return super().setUp()
    
    def test_rejects_invalid_encoding(self):
        with self.assertRaises(mrna.InvalidmRNASequenceEncodingException):
            self.mrna.check_aminoacid_sequence_encoding(['as'])
        with self.assertRaises(mrna.InvalidmRNASequenceEncodingException):
            self.mrna.check_aminoacid_sequence_encoding([''])
        with self.assertRaises(mrna.InvalidmRNASequenceEncodingException):
            self.mrna.check_aminoacid_sequence_encoding(['asdfd'])

    def test_generates_valid_petrinet(self):
        pnet_json_dict=self.mrna.get_pnet_json_dict()
        pnet_validator.PNetValidator.validate_schema(pnet_json_dict)
        


if __name__ == '__main__':
    unittest.main()