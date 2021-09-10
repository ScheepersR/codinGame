import itertools
from functools import total_ordering

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
    'CASTLE': {'peasant': 1, 'knight': 1, 'mounted': 1, 'mounted_knight': 1},
    'HOUSE': {'peasant': 1, 'knight': 1, 'mounted': 1, 'mounted_knight': 1},
    'WIZARD': {'peasant': 1, 'knight': 1, 'mounted': 1, 'mounted_knight': 1},
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
            wizard_targets.append((x_coord, y_coord))
        kingdom[(x_coord,y_coord)] = land_type

for _poi in range(n):
    poi, x, y = input().split()
    x,y = int(x), int(y)

    pois[(x,y)] = poi

    if poi == "HOUSE":
        START = (x, y)
    
    if poi == objective:
        OBJECTIVE = (x, y)

    if poi == "CASTLE":
        CASTLE = (x, y)

    if poi == "WIZARD":
        wiz = (x, y)
        target = min(
            [target for target in wizard_targets if target != wiz],
            key=lambda x: wizardly_distance(x, wiz)
        )
        wizards[wiz] = {'closest_poi': target}


# Search for shortest path 
@total_ordering
class Journey():
    visited: list
    character_state: str #peasant, knight, 
    objective_achieved: bool
    journey_length: int
    pos: tuple

    def __init__(self, start):
        self.journey_length = 0 #good bye mum xoxo (not 1 because castle)
        self.character_state = "peasant"
        self.objective_achieved = False
        self.visited = [start]
        self.history = {(start, self.character_state, self.objective_achieved)}
        self.pos = start

    def priority(self):
        #basic heuristic to start with 
        dist_to_obj = wizardly_distance(self.pos, OBJECTIVE) if not self.objective_achieved else 0
        dist_to_castle = wizardly_distance(self.pos, CASTLE if self.objective_achieved else OBJECTIVE)

        return dist_to_obj + dist_to_castle

    def make_new_move(self, days, next_step):
        self.journey_length += days
        self.visited.append(next_step)
        self.pos = next_step
        if self.pos == OBJECTIVE:
            self.objective_achieved = True

        event = (self.pos, self.character_state, self.objective_achieved)
        if event in self.history:
            return False
        self.history.add(event)
        return True

    def get_horse(self):
        if self.character_state == "mounted": 
            return
        else:
            self.character_state = "mounted" if self.character_state == "peasant" else "mounted_knight"

    def get_sword(self):
        if self.character_state == "knight":
            return
        else:
            self.character_state = "knight" if self.character_state == "peasant" else "mounted_knight"

    def quest_complete(self):
        return self.objective_achieved and self.pos == CASTLE

    def __lt__(self, other):
        return self.priority() < other.priority()
        
    def __eq__(self, other):
          
        # Changing the functionality
        # of equality operator
        return self.priority() != other.priority()
          

from queue import PriorityQueue
from copy import deepcopy
q = PriorityQueue()

q.put(Journey(START))

shortest = None
while not q.empty():
    journey = q.get()

    if journey.quest_complete():
        shortest = shortest or journey.journey_length
        shortest = min(shortest, journey.journey_length)
        print(shortest)
        break
        
    if shortest and journey.journey_length >= shortest:
        continue

    for next_step in adj(*journey.pos, width, height):
        terrain = kingdom[next_step]

        next_j = deepcopy(journey)
        if terrain == "I":
            poi = pois[next_step]
            if next_step in next_j.visited:
                days = poi_traits[poi].get('visited') or poi_traits[poi][next_j.character_state]
            else:
                days = poi_traits[poi][next_j.character_state]
            if poi == 'WIZARD':
                next_step = wizards[wiz]['closest_poi']
            if poi == 'STABLE':
                next_j.get_horse()
            if poi == 'BLACKSMITH':
                next_j.get_sword()
        else:
            #print((terrain, next_j.character_state), file=sys.stderr, flush=True)
            days = map_traits[terrain][next_j.character_state] 
        
        if days is None:
            #IMA SCARED OF HEIGHTS
            continue

        if next_j.make_new_move(days, next_step):
            q.put(next_j)
