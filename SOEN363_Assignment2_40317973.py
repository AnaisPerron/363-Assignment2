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


print("\n =================================================Task 3: Pandas queries================================================\n")

# Show money with two decimal places
pd.set_option("display.float_format", "{:.2f}".format)

# Shared joined table: each rental with its member and equipment details
full = pd.merge(ren, mem, on="member_id", how="inner")
full = pd.merge(full, eq, on="equipment_id", how="inner")
full["revenue"] = full["quantity"] * full["rental_days"] * full["daily_rate"] # revenue per rental

# Total spending per member (only members with rentals)
spending = full.groupby(["member_id", "member_name", "city"])["revenue"].sum().reset_index()
spending = spending.rename(columns={"revenue": "total_spending"})


#1. List equipment id and equipment name for equipment with daily rate greater than CAD 40.
print("\nQ1. Equipment with daily rate greater than CAD 40")
expensive_equipment = eq[eq["daily_rate"] > 40][["equipment_id", "equipment_name"]] # filter, keep 2 columns
print(expensive_equipment.sort_values("equipment_id")) # sort by id

#2. Display member id and member name for members whose city is Montreal.
print("\nQ2. Members whose city is Montreal")
montreal_members = mem[mem["city"] == "Montreal"][["member_id", "member_name"]] # filter by city
print(montreal_members.sort_values("member_id").rename_axis("row"))  # sort by id

#3. Count the total number of members in the cleaned members table, including members with no rentals.
print("\nQ3. Total number of members")
print(mem["member_id"].count())  # count rows of the members table

#4. Count the rental id values for rentals with quantity greater than 5.
print("\nQ4. Rentals with quantity greater than 5")
print(ren[ren["quantity"] > 5]["rental_id"].count()) # filter, then count ids

#5. Calculate the average daily rate across all cleaned equipment records.
print("\nQ5. Average daily rate")
print(f"{eq['daily_rate'].mean():.2f}") # mean, rounded to 2 decimals

#6. Find the equipment item(s) with the highest daily rate. Display equipment id, equipment name, and daily rate.
print("\nQ6. Equipment with the highest daily rate")
top_rate_equipment = eq[eq["daily_rate"] == eq["daily_rate"].max()] # all rows equal to the max
print(top_rate_equipment[["equipment_id", "equipment_name", "daily_rate"]].sort_values("equipment_id").rename_axis("row"))

#7. Count equipment items in each category, including equipment that has never been rented. Display category and equipment count.
print("\nQ7. Equipment count per category")
category_counts = eq.groupby("category")["equipment_id"].count().reset_index() # group equipment, not rentals
print(category_counts.rename(columns={"equipment_id": "equipment_count"}).rename_axis("row"))

#8. Count rental id values for rentals starting strictly after September 15, 2026.
print("\nQ8. Rentals starting after September 15, 2026")
print(ren[ren["rental_date"] > "2026-09-15"]["rental_id"].count())  # strictly after

#9. Calculate total rental revenue for rentals with rental days greater than 3.

print("\nQ9. Total revenue for rentals with more than 3 rental days")
print(f"{full[full['rental_days'] > 3]['revenue'].sum():.2f}")  # filter, then sum revenue

#10. Find Halifax members who rented at least 4 units in a single rental. Display member id and member name.

print("\nQ10. Halifax members who rented at least 4 units in one rental")
halifax_big_renters = full[(full["city"] == "Halifax") & (full["quantity"] >= 4)]  # both conditions
print(halifax_big_renters[["member_id", "member_name"]].drop_duplicates().sort_values("member_id").rename_axis("row"))

#11. Find Montreal members with at least one rental starting in September 2026. Displaymember id and member name.
print("\nQ11. Montreal members with a rental in September 2026")
montreal_sept_members = full[(full["city"] == "Montreal")
           & (full["rental_date"] >= "2026-09-01") & (full["rental_date"] <= "2026-09-30")]  # date range
print(montreal_sept_members[["member_id", "member_name"]].drop_duplicates().sort_values("member_id").rename_axis("row"))


#12. Find Ottawa members with more than two rental transactions. Display member id,member name, and rental count.
print("\nQ12. Ottawa members with more than two rentals")
ottawa_rental_counts = full[full["city"] == "Ottawa"].groupby(["member_id", "member_name"])["rental_id"].count().reset_index()
ottawa_rental_counts = ottawa_rental_counts.rename(columns={"rental_id": "rental_count"})
print(ottawa_rental_counts[ottawa_rental_counts["rental_count"] > 2].sort_values("member_id").rename_axis("row"))  # keep counts > 2

#13. Find the top three equipment items by total units rented, using sum(quantity), not number of transactions. Display equipment id, equipment name, and total units. Return exactly three rows using equipment id ascending to break ties.
print("\nQ13. Top three equipment items by total units rented")
units_per_equipment = full.groupby(["equipment_id", "equipment_name"])["quantity"].sum().reset_index()  # units per item
units_per_equipment = units_per_equipment.rename(columns={"quantity": "total_units"})
print(units_per_equipment.sort_values(["total_units", "equipment_id"], ascending=[False, True]).head(3).rename_axis("row"))

#14. Find the member(s) with the highest total rental spending. Display member id, member name, and total spending.
print("\nQ14. Member(s) with the highest total spending")
top_spenders = spending[spending["total_spending"] == spending["total_spending"].max()]  # all rows equal to the max
top_spenders = top_spenders[["member_id", "member_name", "total_spending"]].sort_values("member_id")
print(top_spenders.rename_axis("row"))

#15. Find the city or cities with the largest number of rental transactions. Display city and rental count; use the member’s city.
print("\nQ15. City or cities with the most rentals")
city_rental_counts = full.groupby("city")["rental_id"].count().reset_index()  # rentals per member city
city_rental_counts = city_rental_counts.rename(columns={"rental_id": "rental_count"})
print(city_rental_counts[city_rental_counts["rental_count"] == city_rental_counts["rental_count"].max()].rename_axis("row"))

#16. List equipment id and equipment name for Camping equipment that has never been rented.
print("\nQ16. Camping equipment that has never been rented")
unrented_camping = pd.merge(eq[eq["category"] == "Camping"], ren, on="equipment_id", how="left")  # left join
unrented_camping = unrented_camping[unrented_camping["rental_id"].isna()]  # no matching rental
print(unrented_camping[["equipment_id", "equipment_name"]].sort_values("equipment_id").rename_axis("row"))

#17. Count the number of rental transactions starting in each month. Display the yearmonth and rental count, sorted chronologically.
print("\nQ17. Rentals per month")
ren_month = ren.copy()
ren_month["yearmonth"] = ren_month["rental_date"].apply(lambda d: d.strftime("%Y-%m"))  # For example: 2026-09
monthly_rentals = ren_month.groupby("yearmonth")["rental_id"].count().reset_index()  # sorted by month
print(monthly_rentals.rename(columns={"rental_id": "rental_count"}).rename_axis("row"))

#18. Label a rental High Value if its revenue exceeds CAD 500 OR both quantity is at least 4 and the member lives in Montreal. Otherwise label it Standard. List the unique member id and member name pairs with at least one High Value rental.


#19. Find the highest-spending member(s) in each city. Consider only members with at least one rental. Display city, member id, member name, and total spending; include ties and sort by city then member id.


#20. Identify member-equipment pairs appearing in more than one rental transaction. Display member id, equipment id, and rental count.
