import pandas as pd
print("\n =================================================Task 1: Data loading=================================================\n")

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


print("\n =================================================Task 2: Data Cleaning=================================================\n")
# Create copies
eq = equip_df.copy()
mem = memb_df.copy()
ren = rent_df.copy()

print("Initial rows:       Equipment =", len(eq), "| Members =", len(mem), "| Rentals =", len(ren))

#1. Remove rows with any missing value. All columns are required for this exercise.
e, m, r = len(eq), len(mem), len(ren)
eq = eq.dropna()
mem = mem.dropna()
ren = ren.dropna()
print("1. Missing values:  Equipment =", e - len(eq), "| Members =", m - len(mem), "| Rentals =", r - len(ren))

#2. Remove exact duplicate rows, retaining the first occurrence. Do not deduplicate on member id and equipment id: repeat rentals are valid

e, m, r = len(eq), len(mem), len(ren)
eq = eq.drop_duplicates()
mem = mem.drop_duplicates()
ren = ren.drop_duplicates()
print("2. Duplicates:      Equipment =", e - len(eq), "| Members =", m - len(mem), "| Rentals =", r - len(ren))

#3. Validate numeric values.
e, m, r = len(eq), len(mem), len(ren)

# Convert to numbers, failed conversions become missing and are removed
for col in ["equipment_id", "daily_rate", "stock_quantity"]:
    eq[col] = pd.to_numeric(eq[col], errors="coerce")
mem["member_id"] = pd.to_numeric(mem["member_id"], errors="coerce")
for col in ["rental_id", "member_id", "equipment_id", "quantity", "rental_days"]:
    ren[col] = pd.to_numeric(ren[col], errors="coerce")
eq = eq.dropna()
mem = mem.dropna()
ren = ren.dropna()

# Keep only valid values (x % 1 == 0 means x is a whole number)
eq = eq[(eq["equipment_id"] > 0) & (eq["equipment_id"] % 1 == 0)]
eq = eq[(eq["stock_quantity"] >= 0) & (eq["stock_quantity"] % 1 == 0)]
eq = eq[eq["daily_rate"] >= 1]
mem = mem[(mem["member_id"] > 0) & (mem["member_id"] % 1 == 0)]
for col in ["rental_id", "member_id", "equipment_id", "quantity", "rental_days"]:
    ren = ren[(ren[col] > 0) & (ren[col] % 1 == 0)]

# Store number columns as integers
eq = eq.astype({"equipment_id": int, "stock_quantity": int})
mem = mem.astype({"member_id": int})
ren = ren.astype({"rental_id": int, "member_id": int, "equipment_id": int,
                  "quantity": int, "rental_days": int})
print("3. Invalid numbers: Equipment =", e - len(eq), "| Members =", m - len(mem), "| Rentals =", r - len(ren))

#4. Parse rental date 

#5. Remove rental rows whose member id or equipment id does not exist in the cleaned parent tables.

#6. Report final row counts, demonstrate that retained primary keys are unique, and briefly explain the effect of cleaning on subsequent joins


