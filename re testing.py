# import re
#
# pair = "BTC_2x"
#
# # Use regular expression to check if the string ends with _1-10X
# pattern = re.compile(r'_[1-9]X$|_10x$')
# match = re.search(pattern, pair)
#
# if match:
#     print(f"{pair} is a valid pair ending with {match.group()}")
# else:
#     print(f"{pair} is not a valid pair")

import re

# Input strings
string1 = "BTC"
string2 = "ETH"
string3 = "1INCHUSDT"

# Define the regular expression pattern
pattern = r'^\[("[A-Z0-9-_.]{1,20}"(,"[A-Z0-9-_.]{1,20}"){0,}){0,1}\]$'

# Use the search function to find the numeric part of the strings
result1 = re.search(pattern, string1)
result2 = re.search(pattern, string2)
result3 = re.search(pattern, string3)
# Extract the numbers
number1 = int(result1.group(1))
number2 = int(result2.group(1))
number3 = int(result3.group(1))

# Print the extracted numbers
print(number1)  # Output: 2
print(number2)  # Output: 10
print(number3)  # Output: 10
