import itertools
# https://www.codingame.com/training/hard/a-man-with-a-plan
# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

#  grassland 2 days
#  water 2 days
#  mountains 4 days
#  swamp 6 days
#  castle waste 1 day convincing ur not a thief 

#  one day shops, one day to verify ur usage 
#  blacksmith --> sword  (cant cross water)
#  horse --> twice as fast (cant cross mountain)

# wizard, teleports to nearest POI - 1 day recovery, manhatten distance
def wizardly_distance(a, b):
    return sum(abs(val1-val2) for val1, val2 in zip(a,b))

# 4days
# dragon: 
# treasure: 
# dungeon: princess

# Each piece of land is directly connected to its eight neighbors.
import itertools
def adj(a, b, w, h):
    adj_to_consider = itertools.product([a-1, a, a+1], [b-1, b, b+1])
    return (
        [
            (x,y) for x,y in adj_to_consider if all(
                [
                    (x, y) != (a, b), #self not adj to self
                    0 <= x < w, #check x borders
                    0 <= y < h, #check height borders
                ]
            )
        ]
    )

#consider self a knight when armor is gained, consider self mounted if on horse
map_traits = {
    'G': {'peasant': 2, 'knight': 2, 'mounted': 1, 'mounted_knight': 1},
    'W': {'peasant': 2, 'knight': None, 'mounted': 1, 'mounted_knight': None},
    'M': {'peasant': 4, 'knight': 4, 'mounted': None, 'mounted_knight': None},
    'S': {'peasant': 6, 'knight': 6, 'mounted': 3, 'mounted_knight': 3},
    'R': {'peasant': None, 'knight': None, 'mounted': None, 'mounted_knight': None},
}

poi_traits = {
    'PRINCESS': {'peasant': 4, 'knight': 2, 'mounted': 4, 'mounted_knight': 2, 'visited':1},
    'DRAGON': {'peasant': 4, 'knight': 2, 'mounted': 4, 'mounted_knight': 2, 'visited':1},
    'TREASURE': {'peasant': 4, 'knight': 2, 'mounted': 4, 'mounted_knight': 2, 'visited':1},
    'BLACKSMITH': {'peasant': 1, 'knight': 1, 'mounted': 1, 'mounted_knight': 1},
    'STABLE': {'peasant': 1, 'knight': 1, 'mounted': 1, 'mounted_knight': 1},
    'STABLE': {'peasant': 1, 'knight': 1, 'mounted': 1, 'mounted_knight': 1},
}

wizards = {}

width, height, n = [int(i) for i in input().split()]
objective = input()

kingdom = {}
wizard_targets = []
pois = {}
for y_coord in range(height):
    for x_coord, land_type in enumerate(input()):
        if land_type == 'I':
            wizard_targets.append(x_coord, y_coord)
        kingdom[(x_coord,y_coord)] = land_type, False

for _poi in range(n):
    poi, x, y = input().split()
    x,y = int(x), int(y)

    pois[(x,y)] = poi

    if poi == "HOUSE":
        start = (x, y)
    
    if poi == objective:
        objective = (x, y)

    if poi == "CASTLE":
        castle = (x, y)

    if poi == "WIZARD":
        wiz = (x, y)
        target = min(
            [target for target in wizard_targets if target != wiz],
            key=lambda x: wizardly_distance(x, wiz)
        )
        wizards[wiz] = {'closest_poi': target}


# Search for shortest path 

class journey():
    adjacent: list
    visited: list
    character_state: str #peasant, knight, 
    objective_achieved: bool
    journey_length: str

    def __init__(self, start):
        self.journey_length = 1 #good bye mum xoxo
        self.character_state = "peasant"
        self.objective_achieved = False
        self.visited = [start]
        self.adjacent = adj(*start, width, height) 








