import unittest

import numpy as np
from transceiver import utils


class test_utils(unittest.TestCase):
    def test_dtype_を_strで表して戻しても一致する(self):
        array = np.zeros(shape=[10**7], dtype=np.uint8)
        dtype_str = utils.dtype_to_str(array)
        self.assertEqual(utils.dtype_from_str(dtype_str), array.dtype)

    def test_length_to_bytesの長さがoffset_nbytesと一致する(self):
        test_num = 10**4  # literal data fieldの長さはこれくらいになっても良い
        bytes_data = utils.length_to_bytes(test_num)
        self.assertEqual(utils.offset_nbytes, len(bytes_data))

    def test_length_to_bytesで表して元に戻して一致する(self):
        test_num = 10**4
        bytes_data = utils.length_to_bytes(test_num)
        reverted_num = utils.length_from_bytes(bytes_data)
        self.assertEqual(test_num, reverted_num)


if __name__ == "__main__":
    unittest.main()
