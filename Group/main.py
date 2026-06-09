# main.py
import os
import sys
import importlib
import inspect
import numpy as np
import warnings
import random
warnings.filterwarnings("ignore")


MAX_POVOLENE_DMG = 300  # Omezení pro útočné poškození
MAX_POVOLENE_HP = 1500  # Omezení pro životy

def objev_dostupne_postavy():
    """Automaticky prohledá složku a najde všechny naprogramované postavy."""
    postavy = []
    ignorovat = ["main.py", "dummy.py"]
    
    soubory = [f for f in os.listdir('.') if f.endswith('.py') and f not in ignorovat]
    
    for soubor in soubory:
        nazev_modulu = soubor[:-3]
        try:
            modul = importlib.import_module(nazev_modulu)
            for jmeno_tridy, objekt_tridy in inspect.getmembers(modul, inspect.isclass):
                if objekt_tridy.__module__ == nazev_modulu:
                    postavy.append({"modul": nazev_modulu, "trida": jmeno_tridy})
        except Exception:
            continue
    return postavy

def vyber_postavu(hrac_cislo, dostupne):
    print(f"\nDOSTUPNÍ HRDINOVÉ PRO HRÁČE {hrac_cislo}:")
    for i, p in enumerate(dostupne):
        print(f"{i + 1} - {p['trida']} (ze souboru {p['modul']}.py)")
    
    while True:
        vstup = input("Zvol číslo hrdiny: ")
        try:
            idx = int(vstup) - 1
            if idx < 0 or idx >= len(dostupne): raise ValueError
            
            modul = importlib.import_module(dostupne[idx]["modul"])
            trida = getattr(modul, dostupne[idx]["trida"])
            return trida()
        except ValueError:
            print("Chyba: Neplatná volba, zkus to znovu.")

def vykresli_statistiky(p1, p2):
    """Přehledná tabulka statistik po každém kole."""
    print("\n" + "="*45)
    print(f"{'POSTAVA':<25} | {'ZBYLÉ ŽIVOTY (HP)':<15}")
    print("-"*45)
    print(f"{p1.jmeno:<25} | {p1.zivoty:<15}")
    print(f"{p2.jmeno:<25} | {p2.zivoty:<15}")
    print("="*45 + "\n")

def zpracuj_tah(aktivni, pasivni):
    aktivni.vypis_schopnosti()
    
    # Výběr indexu schopnosti (AI nebo hráč)
    if hasattr(aktivni, "is_dummy") and aktivni.is_dummy:
        index = random.randint(0, len(aktivni.schopnosti) - 1)
    else:
        vstup = input(f"Zvol schopnost pro {aktivni.jmeno} (1-{len(aktivni.schopnosti)}): ")
        try:
            index = int(vstup) - 1
            if index < 0 or index >= len(aktivni.schopnosti): raise ValueError
        except ValueError:
            print(f"Pozor: {aktivni.jmeno} promarnil tah špatným zadáním.")
            return

    # Volání schopnosti, která nově VRACÍ data, místo aby měnila životy
    vysledek_akce = aktivni.použij_schopnost(index)
    
    # Pokud schopnost nic nevrátila (zapomněli return), tah končí bez efektu
    if not vysledek_akce:
        return
        
    typ_akce, hodnota = vysledek_akce
    
    if typ_akce == "heal":
        # Léčení aplikuje aktivní postava sama na sebe
        aktivni.zivoty += hodnota
        print(f"Léčení: {aktivni.jmeno} se vyléčil o {hodnota} HP.")
        
    elif typ_akce == "utok":
        # Hlídání maximálního útočného stropu
        skutecne_dmg = hodnota
        if hodnota > MAX_POVOLENE_DMG:
            print(f"Zásah rozhodčího: Poškození sníženo na povolené maximum ({MAX_POVOLENE_DMG} HP).")
            skutecne_dmg = MAX_POVOLENE_DMG
        
        
        # Poslání poškození do void/reakce obránce
        if hasattr(pasivni, "reakce"):
            try:
                # Obránce si poškození zpracuje ve své metodě reakce
                pasivni.reakce(aktivni, skutecne_dmg)
            except Exception as e:
                try:
                    # Záložní plán, pokud reakce spadne
                    pasivni.zivoty -= skutecne_dmg
                    print(f"Zásah: {aktivni.jmeno} zasáhl {pasivni.jmeno} za {skutecne_dmg} HP (reakce selhala: {e}).")
                except Exception:
                    print("Hmmmmm, stalo se něco zvláštního... nechme to být a pokračujeme dál bez udělení dmg...")        
        else:
            print("OK")
            try:
                # Pokud obránce vůbec nemá metodu reakce
                pasivni.zivoty -= skutecne_dmg
                print(f"Zásah: {aktivni.jmeno} zasáhl {pasivni.jmeno} za {skutecne_dmg} HP.")
            except Exception:
                print("Hmmmmm, stalo se něco zvláštního... nechme to být a pokračujeme dál bez udělení dmg...")        

# --- START ENGINGU ---
print("========================================")
print("----- VÍTEJTE V ARÉNĚ PROGRAMÁTORŮ -----")
print("========================================\n")

dostupne_postavy = objev_dostupne_postavy()

if not dostupne_postavy:
    print("Chyba: Ve složce nebyly nalezeny žádné moduly s postavami.")
    sys.exit()

print("Zvol režim hry:")
print("1 - Trénink (Tvůj hrdina vs Cvičný Dummy)")
print("2 - Zápas (Hrdina vs Hrdina)")
rezim = input("Napiš 1 nebo 2: ")

p1 = vyber_postavu(1, dostupne_postavy)

if rezim == "1":
    modul_dummy = importlib.import_module("dummy")
    p2 = modul_dummy.Dummy()
else:
    p2 = vyber_postavu(2, dostupne_postavy)

p1.zivoty = np.int32(p1.zivoty)
p2.zivoty = np.int32(p2.zivoty)

print(f"\nBITVA ZAČÍNÁ: {p1.jmeno} VS {p2.jmeno}\n")

# Hlavní herní smyčka
while p1.zivoty > 0 and p2.zivoty > 0:
    zpracuj_tah(p1, p2)
    if p2.zivoty <= 0: break
    vykresli_statistiky(p1, p2)

    zpracuj_tah(p2, p1)
    vykresli_statistiky(p1, p2)

print("\n=== KONEC BITVY ===")
if p1.zivoty <= 0:
    print(f"VÍTĚZEM SE STÁVÁ: {p2.jmeno}!")
else:
    print(f"VÍTĚZEM SE STÁVÁ: {p1.jmeno}!")