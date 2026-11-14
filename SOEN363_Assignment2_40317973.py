import pandas as pd
# ==================================Task 1: Data loading==================================

#load files
equip_df = pd.read_csv("equipment.csv")
memb_df = pd.read_excel("members.xlsx")
rent_df = pd.read_csv("rentals.txt", sep=",")

print("\n-----------Display of the first five rows of each DataFrame-----------\n")

print("\nEquipment:\n")
print(equip_df.head())

print("\nMembers:\n")
print(memb_df.head())

print("\nRentals:\n")
print(rent_df.head())

print("\n-----------DataFrames' column names, non-null counts, and data types-----------\n")
print("\nEquipment:")
equip_df.info()
print("\nMembers:")
memb_df.info()
print("\nRentals:")
rent_df.info()


# ==================================Task 2: Data cleaning==================================
# Create copies
eq = equip_df.copy()
mem = memb_df.copy()
ren = rent_df.copy()

#1. Remove rows with any missing value. All columns are required for this exercise.


#2. Remove exact duplicate rows, retaining the first occurrence. Do not deduplicate on member id and equipment id: repeat rentals are valid

#3. Validate numeric values.

#4. Parse rental date 

#5. Remove rental rows whose member id or equipment id does not exist in the cleaned parent tables.

#6. Report final row counts, demonstrate that retained primary keys are unique, and briefly explain the effect of cleaning on subsequent joins


