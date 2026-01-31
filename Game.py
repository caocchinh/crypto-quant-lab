from random import randint

grid = [[[] for _ in range(5)] for _ in range(5)]
randomX, randomY = randint(0, 4), randint(0, 4)
grid[randomY][randomX].append("X")

current_x, current_y, moves_left = 0, 0, 10

print("Answer:")
for row in grid:
    print(row)

while moves_left > 0:
    print(f"\nYou are at position X: {current_x+1} and Y: {current_y+1}")
    user_input = input("Enter a move: left, right, up, or down: ")
    if user_input == "left" and current_x > 0:
        current_x -= 1
    elif user_input == "right" and current_x < 4:
        current_x += 1
    elif user_input == "up" and current_y > 0:
        current_y -= 1
    elif user_input == "down" and current_y < 4:
        current_y += 1
    else:
        print("Invalid input")
        continue
    moves_left -= 1
    if "X" in grid[current_y][current_x]:
        print("You won!")
        break

if moves_left == 0:
    print("You lost!")
