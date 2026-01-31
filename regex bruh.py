import re

pattern = r'^(0*(?:1(\.0+)?|0\.\d+)|0*(\.\d+))%$'

def check_number_with_percentage(input_string):
    return re.match(pattern, input_string) is not None

# Test the regex pattern
test_cases = ["0%", "0.5%", "1%", "1.0%", "0.75%", "-0.5%", "1.5%"]
for test_case in test_cases:
    if check_number_with_percentage(test_case):
        print(f"{test_case} is a valid number between 0 and 1 with the percentage sign.")
    else:
        print(f"{test_case} is not a valid number between 0 and 1 with the percentage sign.")
