import unittest
from modules.fizzBuzz import fizzBuzz

class FizzBuzzTest(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_normal(self):
        self.assertEqual(fizzBuzz(1), 1)

    def test_fizz(self):
        self.assertEqual(fizzBuzz(3), 'Fizz')

    def test_buzz(self):
        self.assertEqual(fizzBuzz(5), 'Buzz')

    def test_fizz_buzz(self):
        self.assertEqual(fizzBuzz(15), 'FizzBuzz')

if __name__ == '__main__':
    unittest.main()