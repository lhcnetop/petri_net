import unittest
import mrna.mRNAPNetBuilder as mRNAPNetBuilder

json_input={
    "chains":[
        {
            "name":"chainA",
            "sequence":["Gly","Ile","Val","Glu","Gln","Cys","Thr","Ser","Ile","Cys","Ser","Leu","Tyr","Gln","Leu","Glu","Asn","Tyr","Cys","Asn"],
            "polipeptide_name":"preprotoinsulin-A-chain"
        },
        {
            "name":"chainB",
            "sequence":["Phe","Val","Asn","Gln","His","Leu","Cys","Gly","Ser","His","Leu","Val","Glu","Ala","Leu","Tyr","Leu","Val","Cys","Gly","Glu","Arg","Gly","Phe","Phe","Tyr","Thr","Pro","Lys","Ala"],
            "polipeptide_name":"preprotoinsulin-B-chain"
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
        self.mrna=mRNAPNetBuilder.mRNA(json_input)
        return super().setUp()
    
    def checkInvalidInput(self):
        self.assertRaises(mRNAPNetBuilder.InvalidmRNASequenceEncoding,self.mrna.check_aminoacid_sequence_encoding,['as'])