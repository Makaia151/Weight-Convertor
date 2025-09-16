def round_ans(val):
    """
    Rounds temperature or weight to 1 decimal place
    :param val: Number to be rounded
    :return: Number rounded to 1 decimal place as a string
    """
    return "{:.1f}".format(round(val, 1))


def to_grams(to_convert):
    """
    Converts from Oz to G
    :param to_convert: Weight to be converted in Oz
    :return: Converted Weight in G
    """
    answer = (to_convert * 28.35)

    return round_ans(answer)


def to_ounces(to_convert):
    """
    Converts from G to Oz
    :param to_convert: Weight to be converted in G
    :return: Converted Weight in Oz
    """
    answer = (to_convert / 28.35)

    return round_ans(answer)

# Main routine / Testing starts here
# to_c_test = [0, 100, -459]
# to_f_test = [0, 100, 40, -273]

# for item in to_f_test:
#    ans = to_fahrenheit(item)
#    print(f"{item} C is {ans} F")

# print()

# for item in to_c_test:
#    ans = to_celsius(item)
#   print(f"{item} F is {ans} C")