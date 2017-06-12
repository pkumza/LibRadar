import unittest

from util import Util

class TestUtil(unittest.TestCase):

    def test_dict2str(self):
        self.d = dict()
        self.d[14] = 21
        self.d[35] = 6
        self.d[2] = 42
        self.feature = Util.dict2str(self.d)
        self.assertIsInstance(self.feature, str)

    def test_str2dict(self):
        d = dict()
        d[14] = 21257
        d[35] = 68
        d[2] = 42
        feature = Util.dict2str(d)
        kvd = Util.str2dict(feature)
        self.assertIsInstance(kvd, dict)
        self.assertEqual(d, kvd)

    def test_key_large(self):
        d = dict()
        d[14] = 21257
        d[35234234325325234] = 68
        d[2] = 42
        feature = Util.dict2str(d)
        kvd = Util.str2dict(feature)
        self.assertIsInstance(kvd, dict)
        self.assertEqual(d, kvd)

    def test_value_large(self):
        d = dict()
        d[14] = 21257323423235235
        d[35] = 68
        d[2] = 42
        feature = Util.dict2str(d)
        kvd = Util.str2dict(feature)
        self.assertIsInstance(kvd, dict)
        self.assertEqual(d, kvd)

if __name__ == '__main__':
    unittest.main()