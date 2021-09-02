"""
Batman will look for the hostages on a given building by jumping from one window to another using his grapnel gun.
Batman's goal is to jump to the window where the hostages are located in order to disarm the bombs.
Unfortunately he has a limited number of jumps before the bombs go off...
"""

# w: width of the building.
# h: height of the building.
w, h = [int(i) for i in input().split()]
n = int(input())  # maximum number of turns before game over.
bat_x, bat_y = [int(i) for i in input().split()]
min_x, max_x, min_y, max_y = 0, w-1, h-1, 0

# game loop
while True:
    bomb_dir = input()  # the direction of the bombs from batman's current location (U, UR, R, DR, D, DL, L or UL)

    min_x = bat_x + 1 if 'R' in bomb_dir else min_x 
    max_x = bat_x - 1 if 'L' in bomb_dir else max_x
    min_y = bat_y - 1 if 'U' in bomb_dir else min_y 
    max_y = bat_y + 1 if 'D' in bomb_dir else max_y 

    new_x = ((min_x + max_x) // 2) 
    new_y = ((min_y + max_y) // 2)

    bat_x, bat_y = (new_x, new_y)
    print(f"{new_x} {new_y}")
