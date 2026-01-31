import random

add_to = int(input("2 numbers must add to: "))
multiply_to = int(input("2 numbers must multiyply to: "))
solved = False

while solved == False:
    nums = random.sample(range(-100, 150), 2)

    if (nums[0] + nums[1] == add_to) and (nums[0] * nums[1] == multiply_to):
        print(nums)
        print('Solved')
        break