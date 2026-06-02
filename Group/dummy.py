# dummy.py
import random

class Dummy:
    def __init__(self):
        self.jmeno = "Tréninkový Bot (Dummy)"
        self.zivoty = 300 # Obrovská hromada životů na testování
        self.schopnosti = ["Slabé šťouchnutí", "Zrezivělý laser", "Samooprava chyb"]
        self.is_dummy = True # Značka pro main.py, aby věděl, že má hrát počítač

    def vypis_schopnosti(self):
        """Zobrazí schopnosti robota (pro přehled v konzoli)."""
        for i, schopnost in enumerate(self.schopnosti):
            print(f"{i + 1} - {schopnost}")

    def použij_schopnost(self, index, protivnik):
        """Dummy útočí velmi slabě, slouží jako fackovací panák."""
        if index == 0:
            poskozeni = 2
            protivnik.zivoty -= poskozeni
            print(f"{self.jmeno} tě slabě šťouchl do ramene za {poskozeni} HP.")
            
        elif index == 1:
            poskozeni = 4
            protivnik.zivoty -= poskozeni
            print(f"{self.jmeno} vystřelil zrezivělý laser za {poskozeni} HP.")
            
        elif index == 2:
            leceni = 10
            self.zivoty += leceni
            print(f"{self.jmeno} spustil samoopravu a vyléčil se o {leceni} HP.")