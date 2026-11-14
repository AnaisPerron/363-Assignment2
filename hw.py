import pandas as pd

equip_df = pd.read_csv("equipment.csv")
memb_df = pd.read_excel("members.xlsx")
rent_df = pd.read_csv("rentals.txt", sep=",")


print(equip.head())
print()
print(memb.head())
print()
print(rent.head())