def is_prime(number):
    """Return True if *number* is prime."""
    if number <= 1:
        return False

    return False if len([False for element in range(2, number) if number % element == 0]) > 0 else True
