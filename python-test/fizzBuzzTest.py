import unittest
import fizzBuzz

class FizzBuzzTest(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_normal(self):
        self.assertEqual(fizzBuzz.fizzbuzz(1), 1)

    def test_fizz(self):
        self.assertEqual(fizzBuzz.fizzbuzz(3), 'Fizz')

    def test_buzz(self):
        self.assertEqual(fizzBuzz.fizzbuzz(5), 'Buzz')

    def test_fizz_buzz(self):
        self.assertEqual(fizzBuzz.fizzbuzz(15), 'FzzBuzz')

if __name__ == '__main__':
    print(__name__)
    unittest.main()