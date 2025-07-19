import unittest
import tempfile
import os
import polars as pl
from petri_net_core.petrinet.pnet import PNet
from petri_net_core.petrinet.pnet_simulation_helper import simulate_with_history_to_parquet

pnet_dict={
  "places": {
    "p_A": 10,
    "p_B": 30,
    "p_C": 0,
    "p_D": 0
  },
  "transitions":{
      "t_1":{
        "consume": {
          "p_A": 1,
          "p_B": 2
        },
        "produce": {
          "p_C": 1
        }
      },
      "t_2":{
        "consume": {
          "p_B": 1,
          "p_C": 1
        },
        "produce": {
          "p_D": 2
        }
      }
  }
}

class PNetSimulationHelperTests(unittest.TestCase):
    def setUp(self) -> None:
        self.simple_ok_pnet = pnet_dict
        return super().setUp()

    def test_simulation_history_to_parquet(self):
        OkPnet = PNet(self.simple_ok_pnet)
        with tempfile.TemporaryDirectory() as tmpdir:
            parquet_file = os.path.join(tmpdir, 'history.parquet')
            simulate_with_history_to_parquet(OkPnet, num_steps=5, parquet_file=parquet_file, flush_every=2)
            df = pl.read_parquet(parquet_file)
            # Check columns
            expected_columns = {'transition', 'step', 'p_A', 'p_B', 'p_C', 'p_D'}
            self.assertTrue(expected_columns.issubset(set(df.columns)))
            # Check number of rows (should be 6: 1 initial state + 5 simulation steps)
            self.assertEqual(df.shape[0], 6)
            # Check that step column is sequential (0 to 5)
            self.assertListEqual(list(df['step']), list(range(6)))
            # Check that the first row shows initial state (no transition fired yet)
            self.assertIsNone(df['transition'][0])
            # Check initial marking values
            self.assertEqual(df['p_A'][0], 10, "Initial marking for p_A should be 10")
            self.assertEqual(df['p_B'][0], 30, "Initial marking for p_B should be 30")
            self.assertEqual(df['p_C'][0], 0, "Initial marking for p_C should be 0")
            self.assertEqual(df['p_D'][0], 0, "Initial marking for p_D should be 0")
            # Check that place values are integers
            for place in ['p_A', 'p_B', 'p_C', 'p_D']:
                self.assertTrue(df[place].dtype in [pl.Int8, pl.Int16, pl.Int32, pl.Int64, pl.UInt8, pl.UInt16, pl.UInt32, pl.UInt64])

if __name__ == '__main__':
    unittest.main() 