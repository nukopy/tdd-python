import unittest


class TestStringMethod(unittest.TestCase):
    """ 3 つの文字列をテストするスクリプト """

    def test_upper(self):
        self.assertEqual('foo'.upper(), 'FOO')

    def test_isupper(self):
        self.assertTrue('FOO'.isupper())
        self.assertFalse('Foo'.isupper())

    def test_split(self):
        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'world'])

        # check that s.split fails when the separator is not a string
        with self.assertRaises(TypeError):
            s.split(2)

    def test_wrong(self):
        # あえて絶対に落ちるテストケースを書く
        self.assertEqual('Hello', 'hello')


if __name__ == "__main__":
    unittest.main()
