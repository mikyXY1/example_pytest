#Hazeni minci
import random
side_coin=(random.randint(0,1))
if side_coin==0:
    print("hlava")
else:
    print("orel")

try:
    number = int(input("Zadej zkoumane cislo\n"))
    print(f"Zadane cislo je {number}")
except ValueError:
    print("Chybne zadany vstup")