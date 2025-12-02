#!/usr/bin/python3
#produkcni skript, ktery vyuziva modul prod_lib.py (knihovnu)

import prod_lib as pl  # importujeme náš modul prod_lib a pojmenujeme ho jako pl

def main():
    pl.better_name("miky", "novak")  # zavoláme funkci better_name z modulu prod_lib

    name = pl.better_name_return("jana", "svobodova")  # zavoláme funkci better_name_return z modulu prod_lib
    print(f"Returned name: {name}")  # vytiskneme návratovou hodnotu funkce better_name_return


if __name__ == "__main__":   # spuštění hlavní funkce
    main()
