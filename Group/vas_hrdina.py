# vas_hrdina.py
import random

class SomeRandomHrdina:
    def __init__(self):
        # Hodnoty atributů můžeš měnit, ale neměň jejich název (jmeno,zivoty,schopnosti tam musí zůstat)
        self.jmeno = "Nějaký pan hrdina"
        self.zivoty = 10
        self.schopnosti = ["Nějaké útoky", "Něco dalšího..."]
        
        # Semka klidně napiš další atributy, když bude potřeba:
        

    # NESAHAT na tuto metodu:
    def vypis_schopnosti(self):
        """Zobrazí schopnosti hrdiny (pro přehled v konzoli)."""
        for i, schopnost in enumerate(self.schopnosti):
            print(f"{i + 1} - {schopnost}")
            
    
    def použij_schopnost(self, index, protivnik):
        # Tělo metody klidně změň - to je implemetace tvých útoků:
        if index == 0:
            poskozeni = 2
            protivnik.zivoty -= poskozeni
            print(f"{self.jmeno} tě slabě šťouchl do ramene za {poskozeni} HP.")
            
        elif index == 1:
            poskozeni = 100
            protivnik.zivoty -= poskozeni
            print(f"{self.jmeno} tě mognul za {poskozeni} HP.")