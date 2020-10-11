import random
import collections
import turtle
import math

#### GLOBAL VARS ####
map_size = 6
draw_size = 16
random_seed = "Selsky"
#### END GLOBAL VARS ####

class Lotus:
    '''
    Describes the hex flower transitions. See https://goblinshenchman.wordpress.com/2018/10/25/2d6-hex-power-flower/
    '''
    def __init__(self, name, transitions, colors):
        self.name = name
        assert(len(transitions) == 6)
        self.transitions = transitions
        self.colors = colors

    def transition(self, roll):
        direction = rollToDirection(roll)
        return self.transitions[direction]

_Hex = collections.namedtuple("Hex", ["q", "r", "s"])
def Hex(q, r, s):
    assert not (round (q + r + s) != 0), "q + r + s must be 0"
    return _Hex(q, r, s)

Point = collections.namedtuple("Point", ["x", "y"])

def flat_hex_corner(center, size, i):
    angle_deg = 60 * i
    angle_rad = math.pi / 180 * angle_deg
    return Point(center.x + size * math.cos(angle_rad),
                    center.y + size * math.sin(angle_rad))

def draw_hex(t, center, size):
    t.pu()
    points = [flat_hex_corner(center, size, i) for i in range(6)]
    t.goto(points[-1])
    t.pd()
    t.begin_fill()
    for i in points:
        t.goto(i)
    t.end_fill()
    t.pu()

def hex_to_pixel(h, size):
    M = [3.0 / 2.0, 0.0, math.sqrt(3.0) / 2.0, math.sqrt(3.0)]
    x = (M[0] * h.q + M[1] * h.r) * size
    y = (M[2] * h.q + M[3] * h.r) * size
    return Point(x, y)

def drawHex(h, hexes):
    size = draw_size
    center = hex_to_pixel(h, size)
    hex_type = hexes[h]
    lotus_type = lotus[hex_type]
    donny.color(lotus_type.colors[0])
    donny.fillcolor(lotus_type.colors[1])
    draw_hex(donny, center, size)
    donny.pu()
    donny.goto(center)
    donny.pd()
    donny.write(hex_type)
    donny.pu()

def roll2d6():
    roll = sum([random.randint(1, 6) for _ in range(2)])
    return roll

def rollToDirection(roll):
    if roll in [12]:
        return 0
    elif roll in [2, 3]:
        return 1
    elif roll in [4, 5]:
        return 2
    elif roll in [6, 7]:
        return 3
    elif roll in [8, 9]:
        return 4
    elif roll in [10, 11]:
        return 5
    else:
        raise ValueError("rollToDirection only takes ints from 2-12")

hex_directions = [
        Hex(+1, -1, 0),
        Hex(+1, 0, -1),
        Hex(0, +1, -1),
        Hex(-1, +1, 0),
        Hex(-1, 0, +1),
        Hex(-1, 0, +1),
        Hex(0, -1, +1)
    ]

def hex_add(a, b):
    return Hex(a.q + b.q, a.r + b.r, a.s + b.s)

def hex_neighbors(h):
    return [hex_add(h, a) for a in hex_directions]

def hex_distance(a, b):
    return max(abs(a.q - b.q), abs(a.r - b.r), abs(a.s - b.s))

def discoverSurroundingHexes(h, discovered_hexes):
    neighbors = hex_neighbors(h)
    neighbors = [n for n in neighbors if n not in discovered_hexes and hex_distance(Hex(0, 0, 0), h) <= map_size]
    if h not in discovered_hexes:
        a = 'H'
        discovered_hexes[h] = a
    else:
        a = discovered_hexes[h]
    random.shuffle(neighbors)
    for n in neighbors:
        if n in discovered_hexes:
            continue
        r = roll2d6()
        b = lotus[a].transition(r)
        if b == 'S' and a in ['A2', 'H2', 'F2', 'FP2', 'P4', 'AP2'] and random.randint(0, 10) < 3:
            b = 'L3'
        discovered_hexes[n] = b
        discovered_hexes = discoverSurroundingHexes(n, discovered_hexes)
    return discovered_hexes

lotus_hexes = [
            Lotus("S8", ["I", "O4", "O3", "O2", "O1", "S7"],  ("#2E4164", "#A6D8E8")),
            Lotus("S7", ["S3", "I", "S8", "O1", "S6", "S2"],  ("#2E4164", "#A6D8E8")),
            Lotus("S6", ["S2", "S7", "O1", "S1", "O6", "S1"], ("#2E4164", "#A6D8E8")),
            Lotus("S5", ["L3", "O6", "O5", "O4", "I", "S4"],  ("#2E4164", "#A6D8E8")),
            Lotus("S4", ['S', "L3", "S5", "I", "S3", "L2"],  ("#2E4164", "#A6D8E8")),
            Lotus("S3", ["L2", "S4", "I", "S7", "S2", "S1"],  ("#2E4164", "#A6D8E8")),
            Lotus("S2", ["S1", "S3", "S7", "S6", "L3", "O3"], ("#2E4164", "#A6D8E8")),
            Lotus("S1", ["S6", "L2", "S3", "S2", "S", "O7"], ("#2E4164", "#A6D8E8")),
            Lotus("S",  ["H2", "F2", "FP2", "P4", "AP2", "A2"], ("#6F9AD3", "#DEEEF3")),
            Lotus("P4", ["S", "FP2", "P3", "P2", "P1", "AP2"],  ("#FFFD5A", "#FFFED3")),
            Lotus("P3", ["FP2", "FP1", "A1", "H3", "P2", "P4"], ("#FFFD5A", "#FFFED3")),
            Lotus("P2", ["P4", "P3", "P3", "P4", "P1", "P1"],   ("#FFFD5A", "#FFFED3")),
            Lotus("P1", ["AP2", "P4", "P2", "H1", "F1", "AP1"], ("#FFFD5A", "#FFFED3")),
            Lotus("O7", ["O5","O2", "S1", "O6", "O3", "O4"],  ("#EFF269", "#43A1E2")),
            Lotus("O6", ["O7", "S6", "S", "O5", "S5", "L3"], ("#EFF269", "#43A1E2")),
            Lotus("O5", ["O6", "O1", "L2", "O7", "O4", "S5"], ("#EFF269", "#43A1E2")),
            Lotus("O4", ["S5", "O5", "O7", "O3", "S8", "I"],  ("#EFF269", "#43A1E2")),
            Lotus("O3", ["O4", "O7", "S2", "L3", "O2", "S8"], ("#EFF269", "#43A1E2")),
            Lotus("O2", ["S8", "O3", "O3", "S8", "O1", "O1"], ("#EFF269", "#43A1E2")),
            Lotus("O1", ["S7", "S8", "O2", "L2", "O5", "S6"], ("#EFF269", "#43A1E2")),
            Lotus("M",  ["M", "M", "H3", "H2", "H1", "M"],("#141412", "#A4A295")),
            Lotus("L3", ["O3", "S2", "O6", "S5", "S4", "S"], ("#EA974F", "#55AD58")),
            Lotus("L2", ["O1", "S", "S4", "S3", "S1", "O5"], ("#EA974F", "#55AD58")),
            Lotus("L1", ["S", "S", "L3", "S4", "L2", "S"],    ("#EA974F", "#55AD58")),
            Lotus("I",  ["S4", "S5", "O4", "S8", "S7", "S3"],  ("#6390D1", "#55AD58")),
            Lotus("H3", ["P3", "A1", "FH", "F2", "H2", "M"],("#969476", "#DFDCCB")),
            Lotus("H2", ["M", "H3", "F2", "S", "A2", "H1"],("#969476", "#DFDCCB")),
            Lotus("H1", ["P1", "M", "H2", "A2", "AH", "F1"],("#969476", "#DFDCCB")),
            Lotus("FP2", ["F2", "F1", "FP1", "P3", "P4", "S"],("#FFFD5A", "#CEE599")),
            Lotus("FP1", ["F1", "P2", "AH", "FH", "P3", "FP2"],("#FFFD5A", "#CEE599")),
            Lotus("FH", ["FP1", "AP1", "M", "F1", "F2", "H3"], ("#5BB669", "#C5CDA1")),
            Lotus("F2", ["H3", "FH", "F1", "FP2", "S", "H2"],("#5BB669", "#CEE5AD")),
            Lotus("F1", ["FH", "P1", "H1", "FP1", "FP2", "F2"], ("#5BB669", "#CEE5AD")),
            Lotus("AP2", ["A2", "S", "P4", "P1", "AP1", "A1"],("#FFFD5A", "#F8DFB5")),
            Lotus("AP1", ["A1", "AP2", "P1", "AH", "FH", "AH"],("#FFFD5A", "#F8DFB5")),
            Lotus("AH", ["AP1", "H1", "A2", "A1", "M", "FP1"],("#ECA263", "#DDCEB2")),
            Lotus("A2", ["H1", "H2", "S", "AP2", "A1", "AH"],("#ECA263", "#F8E0CA")),
            Lotus("A1", ["AH", "A2", "AP2", "AP1", "H3", "P3"], ("#ECA263", "#F8E0CA")),
            Lotus('H', ["H2", "F2", "FP2", "P4", "AP2", "A2"], ("#000000", "#FFFFFF")),
        ]

lotus = {h.name: h for h in lotus_hexes}   

if __name__ == "__main__":
    if random_seed:
        random.seed(random_seed)
    turtle.delay(0)
    donny = turtle.Turtle()
    donny.speed(0)
    donny.ht()
    hexes = discoverSurroundingHexes(Hex(6, -3, -3), dict())
    for hex in hexes:
        drawHex(hex, hexes)
    turtle.mainloop()