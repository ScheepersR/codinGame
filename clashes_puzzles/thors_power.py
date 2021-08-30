from itertools import repeat

# light_x: the X position of the light of power
# light_y: the Y position of the light of power
# initial_tx: Thor's starting X position
# initial_ty: Thor's starting Y position

# using N,NE,S ... walk thor to the target location

light_x, light_y, initial_tx, initial_ty = [int(i) for i in input().split()]

vert_dir = 'N' if light_y < initial_ty else 'S'
hz_dir = 'E' if light_x > initial_tx else 'W'

vert = repeat(vert_dir, abs(light_y - initial_ty))
hz = repeat(hz_dir, abs(light_x - initial_tx))
# game loop
while True:
    remaining_turns = int(input())
    print(f"{next(vert, '')}{next(hz, '')}")