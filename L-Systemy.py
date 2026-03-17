import turtle
import random
import time
"""
S - starting nonterminal 
f - forward terminal
b - backward terminal
rXXX - right turn by XXX angle where  0 <= XXX <= 180 (terminal)
lXXX - left turn by XXX angle where  0 <= XXX <= 180 (terminal)
[ push stack terminal
] pop stack terminal
{A .. Z, +, - .. } / S nonterminal building symbols 
"""
class L_system:
    distance = 7
    angle = 60  # 0 <= angle <= 180

    """
    First starting rule S ->  ..
    Basic rules in form A -> B+A ...  combination of angles and nonterminals
    Terminal rules aplied after last iteration A -> f / b / rXXX / lXXX 
    """
    expansion_rules = {}; # dict, left side key, right side rewritten rule
    terminal_rules = {}

    def __init__(self, distance, angle, expansion_rules, terminal_rules):
        self.distance = distance
        self.angle = angle
        self.expansion_rules = expansion_rules
        self.terminal_rules = terminal_rules
        # get str angle
        str_angle = str(self.angle)
        if self.angle < 10:
            str_angle = "00" + str_angle
        elif self.angle < 100:
            str_angle = "0" + str_angle
        self.str_angle = str_angle


    # helper so that I dont have to copy it into every test
    def add_basic_angles(self):
        self.terminal_rules['+'] = "r" + self.str_angle
        self.terminal_rules['-'] = "l" + self.str_angle

class L_builder:
    axiom = "S"

    def __init__(self, system):
        self.__system = system

    # todo for them
    def build_system(self, iterations = 4):
        for i in range(iterations):
            self.axiom = self.performIteration(self.axiom)
        self.axiom = self.replaceNonterminals(self.axiom)


    def performIteration(self, old_axiom):
        new_axiom = ""
        for nonterminal in old_axiom:
            match = self.__system.expansion_rules.get(nonterminal) # add nondeterminism
            if match is None:
                new_axiom += nonterminal
            elif type(match) == list:
                new_axiom += random.choice(match)
            else:
                new_axiom += match
        return new_axiom

    def replaceNonterminals(self, old_axiom):
        new_axiom = ""
        for nonterminal in old_axiom:
            match = self.__system.terminal_rules.get(nonterminal) # add nondeterminism
            if match is None:
                new_axiom += nonterminal
            else:
                new_axiom += match # add nondeterminism
        return new_axiom

    def get_axiom(self):
        return self.axiom

class L_drawer:
    speed = 0

    def __init__(self, axiom, distance, startPos, startAngle):
        self.__axiom = axiom
        self.__distance = distance
        self.startPos = startPos
        self.startAngle = startAngle



    def draw_L_system(self):
        wn = turtle.Screen()
        # Vyčistíme plochu pro nový obrazec
        turtle.resetscreen() 
        
        pen = turtle.Turtle()
        pen.speed(self.speed)
        pen.hideturtle() # Želva samotná nebude vidět, jen čára
        pen.up()
        pen.goto(self.startPos[0], self.startPos[1])
        pen.setheading(self.startAngle)
        pen.down()
        
        turtle.tracer(0, 0) 
        
        positionStack = []
        angleStack = []
        
        # Oprava iterace: i musíme kontrolovat ručně, protože přeskakujeme znaky u úhlů
        idx = 0
        while idx < len(self.__axiom):
            instruction = self.__axiom[idx]
            if instruction == "r":
                angle = int(self.__axiom[idx+1:idx+4])
                pen.right(angle)
                idx += 3
            elif instruction == "l":
                angle = int(self.__axiom[idx+1:idx+4])
                pen.left(angle)
                idx += 3
            elif instruction == "f":
                pen.forward(self.__distance)
            elif instruction == "b":
                pen.back(self.__distance)
            elif instruction == "[":
                positionStack.append(pen.pos())
                angleStack.append(pen.heading())
            elif instruction == "]":
                if positionStack:
                    newPos = positionStack.pop()
                    pen.up()
                    pen.goto(newPos[0], newPos[1])
                    newAngle = angleStack.pop()
                    pen.setheading(newAngle)
                    pen.down()
            idx += 1

        turtle.update()
        # mainloop() zde nesmí být, pokud chceme kreslit další věci

def test_line(depth):
    expansion_rules = {
    "S": "F",
    "F": "FF"
    }

    terminal_rules = {
    "F": "f"
    }

    system = L_system(10, 0, expansion_rules, terminal_rules)


    builder = L_builder(system)
    builder.build_system(depth)
    axiom = builder.get_axiom()

    drawer = L_drawer(axiom, system.distance, (-250,-200), 45)
    drawer.draw_L_system()
    return axiom



def test_koch(depth):
    expansion_rules = {
    "S": "F",
    "F": "F-F++F-F"
    }

    terminal_rules = {
    "F": "f",
    "S": "f",
    "+":"r045",
    "-":"l045"
    }
    system = L_system(3, 45, expansion_rules, terminal_rules)


    system.add_basic_angles()

    builder = L_builder(system)
    builder.build_system(depth)
    axiom = builder.get_axiom()

    drawer = L_drawer(axiom, system.distance, (-250,-200), 0)
    drawer.draw_L_system()
    return axiom

def test_sierpinsky_triangle(depth):

    expansion_rules = {
    "S": "F-G-G",
    "F": "F-G+F+G-F",
    "G": "GG"
    }

    terminal_rules = {
    "F": "f",
    "S": "f",
    "G": "f"
    }
    system = L_system(7, 120, expansion_rules, terminal_rules)


    system.add_basic_angles()

    builder = L_builder(system)
    builder.build_system(depth)
    axiom = builder.get_axiom()

    drawer = L_drawer(axiom, system.distance, (-300,-340), 0)
    drawer.draw_L_system()
    return axiom


def test_barley_deterministic(depth):

    expansion_rules = {
    "S": "X",
    "X": "F-[[X]+X]+F[+FX]-X",
    "F": "FF"
    }

    terminal_rules = {
    "F": "f",
    "S": "f",
    "X": "",
    "[": "[",
    "]": "]"
    }

    system = L_system(2, 25, expansion_rules, terminal_rules)

    system.add_basic_angles()

    builder = L_builder(system)
    builder.build_system(depth)
    axiom = builder.get_axiom()

    drawer = L_drawer(axiom, system.distance, (-300,-300), 45)
    drawer.draw_L_system()
    return axiom

# Only for enthusiasts || use function random.choice() to choose nonterminals from list
def test_barley_non_deterministic(depth, seed):
    random.seed(seed)
    expansion_rules = {
    "S": "[X]T[X]TX",
    "X": ["F-[[X]+X]+F[+FX]-X", "F+[[X]-X]-F[-FX]+X"],
    "F": 5*["FF"] + ["F"],
    "T": "uMFFLd"
    }

    terminal_rules = {
    "F": "f",
    "S": "f",
    "X": "",
    "[": "[",
    "]": "]",
    "M": "r090",
    "L": "l090",
    }
    system = L_system(4, 17.5, expansion_rules, terminal_rules)
    system.add_basic_angles()

    builder = L_builder(system)
    builder.build_system(depth)
    axiom = builder.get_axiom()

    drawer = L_drawer(axiom, system.distance, (-300,-340), 90)
    drawer.draw_L_system()

    return axiom

def test_barley_organic(depth):
    # Nepoužíváme random.seed(), takže Python vybere náhodné číslo sám
    
    expansion_rules = {
        "S": "X",
        # Tady dáváme Pythonu na výběr ze dvou variant růstu
        "X": [
            "F-[[X]+X]+F[+FX]-X", 
            "F+[[X]-X]-F[-FX]+X",
            "F-[X]+[X]F-X"
        ],
        "F": ["FF", "F", "FFF"] # Různá délka stonku
    }

    terminal_rules = {
        "F": "f", "S": "f", "X": "", "[": "[", "]": "]"
    }

    # Zkusíme mírně náhodný úhel pro každé vykreslení (např. 20 až 30 stupňů)
    nahodny_uhel = random.uniform(20, 30)
    
    system = L_system(5, nahodny_uhel, expansion_rules, terminal_rules)
    system.add_basic_angles()

    builder = L_builder(system)
    builder.build_system(depth)
    
    drawer = L_drawer(builder.get_axiom(), system.distance, (0, -300), 90)
    drawer.draw_L_system()

def test_harder_recursive(depth): # "Dragonfruit" barley

    expansion_rules = {
    "S": "X",
    "X": "F-[[X]+X]+F[+FX]-X[H]",
    "F": "FF",
    "H": "HLG",
    "G": "HRG"
    }

    terminal_rules = {
    "F": "fff",
    "G": "ff",
    "H": "ff",
    "S": "f",
    "X": "",
    "[": "[",
    "]": "]",
    "L": "l090",
    "R": "r090"
    }

    system = L_system(2, 25, expansion_rules, terminal_rules)

    system.add_basic_angles()

    builder = L_builder(system)
    builder.build_system(depth)
    axiom = builder.get_axiom()

    drawer = L_drawer(axiom, system.distance, (-300,-300), 45)
    drawer.draw_L_system()
    return axiom


#========================================
# Part with recursive functions
#========================================

# very basic prolonging line
def line_recursive(depth):
    if depth <= 1:
        return "f"
    s = line_recursive(depth - 1)
    s += line_recursive(depth - 1)
    return s

# !! Test drawing lines with this function but in the code bellow 
# create lines using "f" * {formula} // formula for line length !!

def koch_curve_recursive(depth):
    s = ""
    if depth <= 1:
        s += "f"
        return s

    s += koch_curve_recursive(depth - 1)
    s += "l045"
    s += koch_curve_recursive(depth - 1)
    s += "r045r045"
    s += koch_curve_recursive(depth - 1)
    s += "l045"
    s += koch_curve_recursive(depth - 1)
    return s

def sierpinsky_triangle_recursive(depth):
    length = 2 ** (depth - 1)
    s = sierpinsky_triangle_rec(depth - 1)
    s += "l120"
    s += "f"*length
    s += "l120"
    s += "f"*length
    return s

def sierpinsky_triangle_rec(depth):
    length = 2 ** (depth - 1)
    if depth <= 0:
        return "f"
    s = sierpinsky_triangle_rec(depth - 1)
    s += "l120" 
    s += "f"*length
    s += "r120"
    s += sierpinsky_triangle_rec(depth - 1)
    s += "r120" 
    s += "f"*length
    s += "l120"
    s += sierpinsky_triangle_rec(depth - 1)
    return s

def harder_recursive(depth):
    return X(depth - 1)

def X(depth):
    if depth <= 0:
        return ""
    length = 2 ** (depth - 1)
    s = "fff" * length
    s += "l025[["
    s += X(depth - 1)
    s += "]r025"
    s += X(depth - 1)
    s += "]r025" + "fff"*length + "[r025" + "fff"*length
    s += X(depth - 1)
    s += "]l025"
    s += X(depth - 1)
    s += "[" + H(depth - 1) + "]"
    return s

def H(depth):
    if depth <= 0:
        return "ff"
    s = H(depth - 1)
    s += "l090"
    s += G(depth - 1)
    return s

def G(depth):
    if depth <= 0:
        return "ff"
    s = H(depth - 1)
    s += "r090"
    s += G(depth - 1)
    return s

#========================================
# Part with grammar creation
#========================================

def forward_right(depth):
    if depth <= 0:
        return "f"
    s = (depth - 1) * "f" + "r010"
    s += forward_right(depth - 1)
    return s

def forward_left(depth):
    if depth <= 0:
        return "f"
    s = (depth - 1) * "f" + "l010"
    s += forward_left(depth - 1)
    return s

def branch(depth):
    if depth <= 0:
        return "f"
    s = (depth - 1) * "b" + "[l090"
    s += forward_left(depth - 1)
    s += "][r090"
    s += forward_right(depth - 1)
    s += "]"
    s += branch(depth - 1)
    return s

def branch_root(depth):
    if depth <= 0:
        return ""
    s = "[l090"
    s += forward_left(depth - 1)
    s += "][r090"
    s += forward_right(depth - 1)
    s += "]"
    s += branch(depth - 1)
    return s

def circle(depth):
    if depth <= 0:
        return ""
    branchString = branch_root(depth - 1)
    s = "[" + 3 * (depth - 1) * "f" + branchString + "]"
    helper = "r090" + "[" + 3 * (depth - 1) * "f" + branchString + "]"
    s += helper * 3
    return s

def distorted_plane(depth):
    if depth <= 0:
        return ""
    branchString = branch_root(depth - 1)
    s = "[" +  branchString + "]"
    helper = "r090" + "[" + branchString + "]"
    s += helper * 3
    return s

def chaos(depth):
    s = circle(depth - 1)
    s += distorted_plane(depth - 1)
    return s

def test_chaos(depth): # "chaos"

    expansion_rules = {
    "S": "XP",
    "P": "[M]R[M]R[M]R[M]", # distorted plane
    "X": "[UM]R[UM]R[UM]R[UM]", # circle
    "M": "[LG][RH]F", # branch_root
    "F": "D[LG][RH]F", # branch
    "D": "bD",
    "T": "fT",
    "U": "fffU",
    "G": "Tl010G", # fwleft
    "H": "Tr010H" # fwright
    }

    terminal_rules = {
    "F": "f",
    "G": "f",
    "H": "f",
    "S": "f",
    "T": "",
    "X": "",
    "P": "",
    "D": "",
    "U": "",
    "M": "",
    "[": "[",
    "]": "]",
    "L": "l090",
    "R": "r090"
    }

    system = L_system(1, 25, expansion_rules, terminal_rules)

    system.add_basic_angles()

    builder = L_builder(system)
    builder.build_system(depth)
    axiom = builder.get_axiom()

    drawer = L_drawer(axiom, system.distance, (0,0), 90)
    drawer.draw_L_system()
    return axiom, len(expansion_rules) + len(terminal_rules)


# Basic tests
# Don't forget to test edge cases
def basic_tests():
    # L system tasks
    assert test_line(6) == """ffffffffffffffffffffffffffffffff"""

    assert test_koch(3) == """fl045fr045r045fl045fl045fl045fr045r045fl045fr045r04
    5fl045fr045r045fl045fl045fl045fr045r045fl045f"""

    assert test_sierpinsky_triangle(3) == """fl120fr120fr120fl120fl120ffr120fl1
    20fr120fr120fl120fr120ffl120fl120fr120fr120fl120fl120ffffl120ffff"""

    assert test_barley_deterministic(3) == """ffl025[[fl025[[]r025]r025f[r025f]
    l025]r025fl025[[]r025]r025f[r025f]l025]r025ff[r025fffl025[[]r025]r025f[r025
    f]l025]l025fl025[[]r025]r025f[r025f]l025"""

    assert test_barley_non_deterministic(2, 5) == """[fr017.5[[]l017.5]l017.5f[
    l017.5f]r017.5]ur090ffl090d[fr017.5[[]l017.5]l017.5f[l017.5f]r017.5]ur090ff
    l090dfl017.5[[]r017.5]r017.5f[r017.5f]l017.5"""

    assert test_barley_non_deterministic(2, 190) == """[fl017.5[[]r017.5]r017.5
    f[r017.5f]l017.5]ur090ffl090d[fl017.5[[]r017.5]r017.5f[r017.5f]l017.5]ur090
    ffl090dfr017.5[[]l017.5]l017.5f[l017.5f]r017.5"""

    assert test_harder_recursive(3) == """ffffffl025[[fffl025[[]r025]r025fff[r0
    25fff]l025[ff]]r025fffl025[[]r025]r025fff[r025fff]l025[ff]]r025ffffff[r025f
    ffffffffl025[[]r025]r025fff[r025fff]l025[ff]]l025fffl025[[]r025]r025fff[r02
    5fff]l025[ff][ffl090ff]"""

    assert test_chaos(3)[0] == """[fff[l090f][r090f]f]r090[fff[l090f][r090f]f]r
    090[fff[l090f][r090f]f]r090[fff[l090f][r090f]f][[l090f][r090f]f]r090[[l090f
    ][r090f]f]r090[[l090f][r090f]f]r090[[l090f][r090f]f]"""

    # Recursion tasks
    assert line_recursive(6) == "ffffffffffffffffffffffffffffffff"

    assert koch_curve_recursive(3) == """fl045fr045r045fl045fl045fl045fr045r045
    fl045fr045r045fl045fr045r045fl045fl045fl045fr045r045fl045f"""

    assert sierpinsky_triangle_recursive(3) == """fl120fr120fr120fl120fl120ffr1
    20fl120fr120fr120fl120fr120ffl120fl120fr120fr120fl120fl120ffffl120ffff"""

    assert harder_recursive(3) == """ffffffl025[[fffl025[[]r025]r025fff[r025fff
    ]l025[ff]]r025fffl025[[]r025]r025fff[r025fff]l025[ff]]r025ffffff[r025ffffff
    fffl025[[]r025]r025fff[r025fff]l025[ff]]l025fffl025[[]r025]r025fff[r025fff]
    l025[ff][ffl090ff]"""


if __name__ == "__main__":
    # Seznam testů, které chceš spustit
    testy = [
        ("Čára", lambda: test_line(5)),
        ("Kochova křivka", lambda: test_koch(5)),
        ("Sierpinského trojúhelník", lambda: test_sierpinsky_triangle(7)),
        ("Deterministický ječmen", lambda: test_barley_deterministic(8)),
        ("Chaos", lambda: test_chaos(40))
    ]

    for jmeno, funkce in testy:
        print(f"Kreslím: {jmeno}... (pro pokračování zavři okno nebo stiskni Enter v konzoli)")
        funkce()
        # Počkáme 2 sekundy a pak jdeme na další, nebo můžeš použít input()
        time.sleep(2) 
    
    for i in range(9):
        test_barley_deterministic(i)
        # Počkáme 2 sekundy a pak jdeme na další, nebo můžeš použít input()
        time.sleep(1)
    for i in range(10):
        test_barley_organic(7)
        # Počkáme 2 sekundy a pak jdeme na další, nebo můžeš použít input()
        time.sleep(1)
        
    for i in range(35):
        test_chaos(i)
        # Počkáme 2 sekundy a pak jdeme na další, nebo můžeš použít input()
        time.sleep(0.2) 
        
    print("Všechny obrazce byly vykresleny.")
    turtle.done() # Konečné zastavení na posledním obrázku