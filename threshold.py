def switch_case(value):
    switcher = {
        1: "One",
        2: "Two",
        3: "Three"
    }
    return switcher.get(value, "Other")

print(switch_case(2))  # Output: Two
