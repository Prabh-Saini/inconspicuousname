def stepback(number: int, maximum: int) -> int:
    """if number is higher than x return back to 0 and repeat.
    eg. if number = 7 and maximum = 2 the result is 1
    because 0 1 2  0 1 2  0 1  (it's starting at 0)"""
    iteration, result = 0, 0
    if number <= maximum:
        return number

    if number <= 0:
        return 0

    for _ in range(0, number):
        if result == maximum:
            result = 0
        else:
            result += 1

    return result


print(stepback(4, 2))

#used to make sure that each user agent will have correct size
