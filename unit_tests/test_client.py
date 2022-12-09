import unittest
import sys
import os
sys.path.append(os.path.join(os.getcwd(), '..'))
from common.variables import RESPONSE, USER, ACCOUNT_NAME, TIME, ACTION, PRESENCE
from client import create_presence, process_ans


class TestClass(unittest.TestCase):
    def test_def_presense(self):
        test = create_presence()
        test[TIME] = 1.1
        self.assertEqual(test, {ACTION: PRESENCE, TIME: 1.1, USER: {ACCOUNT_NAME: 'Guest'}})

    def test_correct_ans(self):
        self.assertEqual(process_ans({RESPONSE: 200}), '200 : OK')


if __name__ == '__main__':
    unittest.main()
