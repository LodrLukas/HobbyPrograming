# dummy.py
class Dummy:
    def __init__(self):
        self.jmeno = "Tréninkový Bot (Dummy)"
        self.zivoty = 2000
        self.luck = 1
        self.schopnosti = ["Slabé šťouchnutí", "Zrezivělý laser", "Nouzová oprava"]
        self.is_dummy = True

    def vypis_schopnosti(self):
        for i, schopnost in enumerate(self.schopnosti):
            print(f"{i + 1} - {schopnost}")

    def použij_schopnost(self, index):
        if index == 0:
            print(f"{self.jmeno} použil slabé šťouchnutí za 10 dmg!")
            return ("utok", 10)
        elif index == 1:
            print(f"{self.jmeno} použil zrezivělý laser za 25 dmg!")
            return ("utok", 25)
        elif index == 2:
            return ("heal", 40)

    def reakce(self, protivnik, dmg):
        # Dummy nemá žádný pokročilý štít, poškození se mu rovnou odečte
        self.zivoty -= dmg
        print(f"Reakce: {self.jmeno} přijal ránu od {protivnik.jmeno} za {dmg} HP.")