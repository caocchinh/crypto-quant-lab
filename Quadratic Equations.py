import decimal
import math

while True:

    try:
        a = float(input("Enter A: "))
        b = float(input("Enter B: "))
        c = float(input("Enter C: "))
        answer1 = ((b*-1) + math.sqrt((b**2)-(4*a*c))) / (2*a)
        answer2 = ((b*-1) - math.sqrt((b**2)-(4*a*c))) / (2*a)
        print(f"x1: {decimal.Decimal(answer1)}, x2: {decimal.Decimal(answer2)}\n")
    except Exception as error:
        print(f"Something went wrong: {error}\n")