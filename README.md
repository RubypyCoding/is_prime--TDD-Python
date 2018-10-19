## Test Driven Development

#### Getting Started With unittest

To understand how `unittest` works let’s go over an example step-by-step.

We are going to write a simple application that finds prime numbers.

Our first step. It's neccesary to add two files for our folder. First file is for testing, it always has to have `test_` + `file name` + `.py`:

```
$ touch test_primes.py
```

Second, it is important to create the production file.

```
$ touch primes.py
``` 

We gonna to code. Let's begin with test file `test_primes.py`:

```python
import unittest

from primes import is_prime



if __name__ == '__main__':
    unittest.main()

```

The file imports `unittest` and imports the production file `primes.py`, particularly `is_prime` function for testing it.


```python

...

class PrimesTestCase(unittest.TestCase):
    """Tests for `primes.py`."""

    def test_is_five_prime(self):
        """Is five successfully determined to be prime?"""
        self.assertTrue(is_prime(5))

...

```

It creates the test class that inherits from `unitest.TestCase` and we can create a `unit test` with a sigle test case: `test_is_five_prime`.

When using `unittest` framework, any member function whose name begins with `test` in a class deriving from `unittest.TestCase` will be run and its assertion checked, when `unittest.main()` is called.

If we run the `spec` by running `test_primes.py` then we'll see the ouput:

```python
import unittest
from primes import is_prime

class PrimesTestCase(unittest.TestCase):
    """Tests for `primes.py`."""

    def test_is_five_prime(self):
        """Is five successfully determined to be prime?"""
        self.assertTrue(is_prime(5))

if __name__ == '__main__':
    unittest.main()
```

```
$ python test_primes.py
E
======================================================================
ERROR: test_is_five_prime (__main__.PrimesTestCase)
----------------------------------------------------------------------
Traceback (most recent call last):
File "test_primes.py", line 8, in test_is_five_prime
    self.assertTrue(is_prime(5))
File "/home/jknupp/code/github_code/blug_private/primes.py", line 4, in is_prime
    if number % element == 0:
ZeroDivisionError: integer division or modulo by zero

----------------------------------------------------------------------
Ran 1 test in 0.000s
```

The single "E" represents the results of our single test (if it was successful, a "." would have been printed).

## Why Testing?

- Testing makes sure your code works properly under a given set of conditions.

- Testing allows one to ensure that changes to the code did not break existing functionality (when refactoring).

- Testing forces one to think about the code under unusual conditions, possibly revealing logical errors.

- Good testing requires modular, decoupled code, which is a hallmark of good system design.

## Making Assertions

A unit test consists of one or more assertions (statements that assert that some property of the code being tested is true). The unittest.TestCase class contains a number of [assert methods](https://docs.python.org/3/library/unittest.html#assert-methods), so be sure to check the list and pick the appropriate methods for your tests.

In our test case, we use `self.assertTrue`, it is rather self explanatory, it asserts that the argument passed to it evaluates to True.

```python
self.assertTrue(is_prime(5))
```

## Exceptions

The current output of our `spec` is the following:

```
$ python test_primes.py
E
======================================================================
ERROR: test_is_five_prime (__main__.PrimesTestCase)
----------------------------------------------------------------------
Traceback (most recent call last):
File "test_primes.py", line 8, in test_is_five_prime
    self.assertTrue(is_prime(5))
File "/home/jknupp/code/github_code/blug_private/primes.py", line 4, in is_prime
    if number % element == 0:
ZeroDivisionError: integer division or modulo by zero

----------------------------------------------------------------------
Ran 1 test in 0.000s
```

- This output shows us that our single test resulted in failure due not to an assertion failing but rather because an un-caught exception was raised.

- In fact, the unittest framework didn't get a chance to properly run our test because it raised an exception before returning.

- We are preforming the modulo operation over a range of numbers that includes zero, which results in a division by zero being performed. To fix this, we simply change the range to begin at 2 rather than 0, noting that modulo by 0 would be an error and modulo by 1 will always be True (and a prime number is one wholly divisible only by itself and 1, so we needn't check for 1).

## Fixing Things

Once we fix the error, changing the line in `is_prime.py` to `for element in range(2, number):`, we get the following output:

```
$ python test_primes.py
.
----------------------------------------------------------------------
Ran 1 test in 0.000s
```

This one, it is only a single test. We've tested that the syntax of `is_prime` is valid and, at least in one case, it returns the proper result. Our goal is to build a suite (a logical grouping of unit tests) of tests that all pass, though some may fail at first.


## Unusual conditions

Let's make sure it works for non-primes as well. Add the following method to the `PrimesTestCase` class:

```python

...

def test_is_four_non_prime(self):
    """Is four correctly determined not to be prime?"""
    self.assertFalse(is_prime(4), msg='Four is not prime!')

...

```

We added the optional msg argument to the assert call. If this test had failed, our message would have been printed to the console, giving additional information to whoever ran the test.

#### Edge Cases

Let us now consider edge cases, or cases with unusual or unexpected input.

When testing a function that whose range is all positive integers, examples of edge cases include 0, 1, a negative number, and a very large number. Let's test some of these now.

Adding a test for zero is straightforward. We expect is_prime(0) to return False, since, by definition, prime numbers must be greater than one:

```python
...

def test_is_zero_not_prime(self):
    """Is zero correctly determined not to be prime?"""
    self.assertFalse(is_prime(0))

...

```

Our current spec looks like this:

```python
import unittest
from primes import is_prime

class PrimesTestCase(unittest.TestCase):
    """Tests for `primes.py`."""

    def test_is_five_prime(self):
        """Is five successfully determined to be prime?"""
        self.assertTrue(is_prime(5))

    def test_is_four_non_prime(self):
        """Is four correctly determined not to be prime?"""
        self.assertFalse(is_prime(4), msg='Four is not prime!')

    def test_is_zero_not_prime(self):
    	"""Is zero correctly determined not to be prime?"""
    	self.assertFalse(is_prime(0))
    	
if __name__ == '__main__':
    unittest.main()
```

The output is:

```
python test_primes.py
..F
======================================================================
FAIL: test_is_zero_not_prime (__main__.PrimesTestCase)
Is zero correctly determined not to be prime?
----------------------------------------------------------------------
Traceback (most recent call last):
File "test_primes.py", line 17, in test_is_zero_not_prime
    self.assertFalse(is_prime(0))
AssertionError: True is not false

----------------------------------------------------------------------
Ran 3 tests in 0.000s

FAILED (failures=1)
```

We can observe the following:

1) Zero is incorrectly determined to be prime. 
2) We forgot that we decided to skip checks of zero and one in our range.


#### Test in Green

Let's add changes to our code in the production file `primes.py`:

```python
def is_prime(number):
    """Return True if *number* is prime."""
    if number in (0, 1):
        return False

    for element in range(2, number):
        if number % element == 0:
            return False

    return True
```

And now, the output is:

```
...
----------------------------------------------------------------------
Ran 3 tests in 0.000s

OK

```

The test is now in GREEN.

#### How will our function handle a negative number? 

It's important to know before writing the test what the output should be. In this case, any negative number should return False. We'll add this spec to our unit test:

```python
...

def test_negative_number(self):
    """Is a negative number correctly determined not to be prime?"""
    for index in range(-1, -10, -1):
        self.assertFalse(is_prime(index))

...

```

In this spec we decide to check all numbers from -1 .. -9. Calling a test method in a loop is perfectly valid, as are multiple calls to assert methods in a single test.

The output will be...

```
python test_primes.py
...F
======================================================================
FAIL: test_negative_number (__main__.PrimesTestCase)
Is a negative number correctly determined not to be prime?
----------------------------------------------------------------------
Traceback (most recent call last):
File "test_primes.py", line 22, in test_negative_number
    self.assertFalse(is_prime(index))
AssertionError: True is not false

----------------------------------------------------------------------
Ran 4 tests in 0.000s

FAILED (failures=1)
```

The test failed, but on which negative number? 

Using the msg parameter to assertFalse is simply a matter of recognizing that we can use string formatting to solve our problem, we´ll add this code to our spec `test_negative_number`:

```python
...

def test_negative_number(self):
    """Is a negative number correctly determined not to be prime?"""
    for index in range(-1, -10, -1):
        self.assertFalse(is_prime(index), msg='{} should not be determined to be prime'.format(index))

...

```

The output will be...

```
python test_primes
...F
======================================================================
FAIL: test_negative_number (test_primes.PrimesTestCase)
Is a negative number correctly determined not to be prime?
----------------------------------------------------------------------
Traceback (most recent call last):
File "./test_primes.py", line 22, in test_negative_number
    self.assertFalse(is_prime(index), msg='{} should not be determined to be prime'.format(index))
AssertionError: True is not false : -1 should not be determined to be prime

----------------------------------------------------------------------
Ran 4 tests in 0.000s

FAILED (failures=1)
```

We can see the number that is failed.

## Fixing Code

- We see that the failing negative number was the first tested: -1. 
- When a test fails, take a step back and determine the best way to fix the issue. 
- In this case, a solution is adding an additional `if`.

We`ll add code to our file production `primes.py`.

```python
def is_prime(number):
    """Return True if *number* is prime."""
    if number < 0:
        return False

    if number in (0, 1):
        return False

    for element in range(2, number):
        if number % element == 0:
            return False

    return True
```

And voila... test in GREEN!


```
....
----------------------------------------------------------------------
Ran 4 tests in 0.001s

OK
```

## Test in Refactoring

We can refactor this code once we are sure that spec is GREEN. 

The two `if` statements can be merged into a single statement that returns False if the argument is less than 2.

```python
def is_prime(number):
    """Return True if *number* is prime."""
    if number <= 1:
        return False

    for element in range(2, number):
        if number % element == 0:
            return False

    return True
```

How to refactor the for loop through list comprehension?

## Exercise - Refactoring Stage

Please refactor the for loop through list comprehension, only one code line. The test should follow being in GREEN.

```python
def is_prime(number):
    """Return True if *number* is prime."""
    if number <= 1:
        return False
    
    """Here refactor for loop"""

```









