import unittest

import numpy as np
from transceiver.core import transceiver


class test_transceiver(unittest.TestCase):
    def test_transceiver_rw(self):
        name = "fuga"
        array = np.array([[1, 2], [3, 4]], dtype=np.uint8)
        shared_array_w = transceiver.write_numpy(name, array)
        shared_array_r = transceiver.read_numpy(name)
        print("# write\n", shared_array_w)
        print("# read\n", shared_array_r)
        print(transceiver.list_all_name())
        print(transceiver.list_managed_name())
        self.assertEqual(array.dtype, shared_array_w.dtype)
        self.assertEqual(array.shape, shared_array_w.shape)
        self.assertEqual(array.dtype, shared_array_r.dtype)
        self.assertEqual(array.shape, shared_array_r.shape)
        transceiver.release(name)


if __name__ == "__main__":
    unittest.main()
