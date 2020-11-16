import unittest


class TestAssertMethod(unittest.TestCase):
    """ 様々な assert メソッドを試す """

    def setUp(self):
        print('\n===== START test =====')

    def tearDown(self):
        print('===== END test =====')

    def test_assertEqual(self):
        print('test assertEqual')
        self.assertEqual('hello', 'hello')


if __name__ == "__main__":
    unittest.main()
