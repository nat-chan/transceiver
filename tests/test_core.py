import unittest

import numpy as np
from transceiver.core import transceiver


class test_transceiver(unittest.TestCase):
    def test_transceiver_rw(self):
        print("=" * 30)
        name = ""
        array = np.array([[1, 2], [3, 4]], dtype=np.uint8)
        transceiver.write_numpy(name, array)
        shared_array_r = transceiver.read_numpy(name)
        print("# read\n", shared_array_r)
        self.assertEqual(array.dtype, shared_array_r.dtype)
        self.assertEqual(array.shape, shared_array_r.shape)


if __name__ == "__main__":
    unittest.main()
