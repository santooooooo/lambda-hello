def fizzbuzz(number):
        if number %15 == 0:
            return "FizzBuzz"
        if number % 5 == 0:
            return "Buzz"
        if number % 3 == 0:
            return "Fizz"

        return number

if __name__ == '__main__':
    for i in range(1, 101):
        print(fizzbuzz(i))