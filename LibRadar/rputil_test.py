import unittest

from rputil import Util

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

    def test_comp1(self):
        d1 = dict()
        d1[14] = 212
        d1[35] = 68
        d1[2] = 42
        d2 = dict()
        d2[5] = 24
        d2[93] = 31
        d2[14] = 222
        str1 = Util.dict2str(d1)
        str2 = Util.dict2str(d2)
        print("Test comp : %f" % Util.comp_str(str1, str2))

    def test_comp_same(self):
        d1 = dict()
        d1[14] = 212
        d1[93] = 31
        d1[5] = 24
        d2 = dict()
        d2[5] = 24
        d2[93] = 31
        d2[14] = 212
        str1 = Util.dict2str(d1)
        str2 = Util.dict2str(d2)
        print("Just the same : %f" % Util.comp_str(str1, str2))

    def test_comp_totoal_diff(self):
        d1 = dict()
        d1[41] = 212
        d1[39] = 31
        d1[15] = 24
        d2 = dict()
        d2[5] = 24
        d2[93] = 31
        d2[14] = 212
        str1 = Util.dict2str(d1)
        str2 = Util.dict2str(d2)
        print("Total Different : %f" % Util.comp_str(str1, str2))

if __name__ == '__main__':
    unittest.main()