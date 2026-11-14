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
r = len(ren)
ren["rental_date"] = pd.to_datetime(ren["rental_date"], format="%Y-%m-%d", errors="coerce")
ren = ren.dropna()
print("4. Invalid dates:   Equipment = 0 | Members = 0 | Rentals =", r - len(ren))

#5. Remove rental rows whose member id or equipment id does not exist in the cleaned parent tables.

ren = pd.merge(ren, mem[["member_id"]], on="member_id", how="inner")
ren = pd.merge(ren, eq[["equipment_id"]], on="equipment_id", how="inner")
print("5. Orphan rentals:  Equipment = 0 | Members = 0 | Rentals =", r - len(ren))

#6. Report final row counts, demonstrate that retained primary keys are unique, and briefly explain the effect of cleaning on subsequent joins

print("Final rows:         Equipment =", len(eq), "| Members =", len(mem), "| Rentals =", len(ren))

print("\nPrimary keys unique?")
print("equipment_id:", len(eq["equipment_id"].drop_duplicates()) == len(eq))
print("member_id:   ", len(mem["member_id"].drop_duplicates()) == len(mem))
print("rental_id:   ", len(ren["rental_id"].drop_duplicates()) == len(ren))

print("\nEffect on joins:")
print("Every remaining rental matches exactly one member and one equipment item,")
print("so joins on member_id and equipment_id lose no rentals, create no duplicate")
print("rows, and revenue is never calculated from missing or invalid values.")

# Join validation: join rentals to members and equipment, before and after cleaning
raw_join = pd.merge(rent_df, memb_df, on="member_id", how="inner")
raw_join = pd.merge(raw_join, equip_df, on="equipment_id", how="inner")
clean_join = pd.merge(ren, mem, on="member_id", how="inner")
clean_join = pd.merge(clean_join, eq, on="equipment_id", how="inner")

print("\nJoin validation (rentals + members + equipment):")
print("Before cleaning: rentals =", len(rent_df), "| joined rows =", len(raw_join))
print("After cleaning:  rentals =", len(ren), "| joined rows =", len(clean_join))
print("Every clean rental joined once:", len(clean_join) == len(ren))

print("\nEffect on joins:")
print("Before cleaning, duplicate parent keys repeat rentals and orphan ids drop them,")
print("so the joined row count is wrong. After cleaning, every rental matches exactly")
print("one member and one equipment item, so joins on member_id and equipment_id keep")
print("each rental exactly once, and revenue is never calculated from missing or")
print("invalid values.")