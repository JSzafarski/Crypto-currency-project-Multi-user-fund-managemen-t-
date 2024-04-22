
def string_builder(multiplier):  # based on the multiplier it will build a string
    number_of_squares = int(multiplier)
    string = ""
    for i in range(1, number_of_squares):
        string += "🟪"
    return string
