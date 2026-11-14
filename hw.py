import pandas as pd

equip = pd.read_csv("equipment.csv")
memb = pd.read_excel("members.xlsx")
rent = pd.read_csv("rentals.txt", sep="\t")


print(equip.head())
print()
print(memb.head())
print()
print(rent.head())