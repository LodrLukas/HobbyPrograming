# main.py
import importlib
import sys

def nacti_postavu(nazev_modulu, nazev_tridy):
    """Dynamicky načte modul z disku."""
    try:
        modul = importlib.import_module(nazev_modulu)
        trida = getattr(modul, nazev_tridy)
        return trida()
    except Exception as e:
        print(f"Nepodařilo se načíst postavu ze souboru {nazev_modulu}.py: {e}")
        sys.exit()

print("=========================================")
print("---VÍTEJTE V SUPERSOUBOJI PROGRAMÁTORŮ---")
print("=========================================\n")

print("Zvol režim hry:")
print("1 - Trénink (Tvůj hrdina vs Cvičný Dummy)")
print("2 - Zápas (Hrdina vs Hrdina)")
rezim = input("Napiš 1 nebo 2: ")

# Načtení první postavy (hráč 1)
soubor_p1 = input("\nZadej název souboru pro Hráče 1 (např. rytir): ")
trida_p1 = input("Zadej název Třídy pro Hráče 1 (např. Rytir): ")
p1 = nacti_postavu(soubor_p1, trida_p1)

# Načtení druhé postavy na základě režimu
if rezim == "1":
    # Automaticky importujeme dummy.py z lokální složky
    p2 = nacti_postavu("dummy", "Dummy")
else:
    soubor_p2 = input("\nZadej název souboru pro Hráče 2 (např. ninja): ")
    trida_p2 = input("Zadej název Třídy pro Hráče 2 (např. Ninja): ")
    p2 = nacti_postavu(soubor_p2, trida_p2)

print(f"\nARÉNA SE OTEVÍRÁ: {p1.jmeno} VS {p2.jmeno}\n")

# Herní smyčka souboje
while p1.zivoty > 0 and p2.zivoty > 0:
    # --- KOLO HRÁČE 1 ---
    print(f"\nSTAV: {p1.jmeno} ({p1.zivoty} HP) | {p2.jmeno} ({p2.zivoty} HP)")
    p1.vypis_schopnosti()
    
    vstup = input(f"{p1.jmeno}, zvol schopnost (1-3): ")
    try:
        index = int(vstup) - 1
        if index < 0 or index > 2: raise ValueError
        p1.použij_schopnost(index, p2)
    except ValueError:
        print(f"{p1.jmeno} zmateně zakopl a promarnil tah! (Špatný vstup)")

    if p2.zivoty <= 0: break

    # --- KOLO HRÁČE 2 (Monstrum / Druhý hráč / Dummy) ---
    print(f"\nSTAV: {p1.jmeno} ({p1.zivoty} HP) | {p2.jmeno} ({p2.zivoty} HP)")
    p2.vypis_schopnosti()
    
    # Pokud hraje Dummy, vybere si schopnost náhodně sám (počítač), abychom nemuseli nic mačkat
    if hasattr(p2, "is_dummy") and p2.is_dummy:
        import random
        index = random.randint(0, 2)
        print(f"Dummy (AI) automaticky volí schopnost číslo {index + 1}...")
        p2.použij_schopnost(index, p1)
    else:
        vstup = input(f"{p2.jmeno}, zvol schopnost (1-3): ")
        try:
            index = int(vstup) - 1
            if index < 0 or index > 2: raise ValueError
            p2.použij_schopnost(index, p1)
        except ValueError:
            print(f"{p2.jmeno} nezaostřil zrak a promarnil tah! (Špatný vstup)")

# Vyhodnocení
print("\n=== KONEC BITVY ===")
if p1.zivoty <= 0:
    print(f"VÍTĚZEM SE STÁVÁ: {p2.jmeno}!")
else:
    print(f"VÍTĚZEM SE STÁVÁ: {p1.jmeno}!")