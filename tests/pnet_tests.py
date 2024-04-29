import unittest
from petrinet import pnet

##  python -m unittest tests/pnet_tests.py  

pnet_dict={
  "places": {
    "A": 10,
    "B": 30,
    "C": 0,
    "D": 0
  },
  "transitions": [
    {
      "name": "A+2B->C",
      "consumes": {
        "A": 1,
        "B": 2
      },
      "produces": {
        "C": 1
      }
    },
    {
      "name": "B+C->2D",
      "consumes": {
        "B": 1,
        "C": 1
      },
      "produces": {
        "D": 2
      }
    }
  ]
}

class PNetTests(unittest.TestCase):
    def setUp(self) -> None:
        self.simple_ok_pnet=pnet_dict
        return super().setUp()

    def test_with_valid_input(self):
        OkPnet=pnet.PNet(self.simple_ok_pnet)
        self.assertEqual(OkPnet.dict_places['A'],10)
        self.assertEqual(OkPnet.dict_places['B'],30)
        self.assertEqual(OkPnet.dict_places['C'],0)
        self.assertEqual(OkPnet.dict_places['D'],0)
        #OkPnet.transitions_dict['A+2B->C']

        

if __name__ == '__main__':
    unittest.main()