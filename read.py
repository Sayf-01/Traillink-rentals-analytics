import pandas as pd

#Task 1
equipment_r = pd.read_csv('Tables/equipment.csv')
members_r   = pd.read_excel('Tables/members.xlsx', engine='openpyxl')
rentals_r   = pd.read_csv('Tables/rentals.txt')
for name, df in [('Equipment', equipment_r),('Members', members_r),('Rentals', rentals_r)]:
    print(f"\n---- {name} ----")
    print(df.head())
    df.info()

#Task 2

equipment = equipment_r.copy()
members = members_r.copy()
rentals = rentals_r.copy()

print("Initial counts:", len(equipment), len(members), len(rentals))

# step 1 removing rows with missing values
equipment_bfr1 = len(equipment)
members_bfr1 = len(members)
rentals_bfr1 = len(rentals)

equipment = equipment.dropna()
members = members.dropna()
rentals = rentals.dropna()

print(
    f"Equipment step 1 removed: {equipment_bfr1 - len(equipment)}\n"
    f"Members step 1 removed: {members_bfr1 - len(members)}\n"
    f"Rentals step 1 removed: {rentals_bfr1 - len(rentals)}"
)

# step 2 removing duplicates
equipment_bfr2 = len(equipment)
members_bfr2 = len(members)
rentals_bfr2 = len(rentals)

equipment = equipment.drop_duplicates()
members = members.drop_duplicates()
rentals = rentals.drop_duplicates()

print(
    f"Equipment step 2 removed: {equipment_bfr2 - len(equipment)}\n"
    f"Members step 2 removed: {members_bfr2 - len(members)}\n"
    f"Rentals step 2 removed: {rentals_bfr2 - len(rentals)}"
)

# step 3 validating numeric values

equipment_bfr3 = equipment.copy()

before = len(equipment)
for col in ['equipment_id', 'daily_rate', 'stock_quantity']:
    equipment[col] = pd.to_numeric(equipment[col], errors='coerce')
equipment = equipment.dropna(subset=['equipment_id', 'daily_rate', 'stock_quantity'])
equipment = equipment[
    (equipment['equipment_id'] > 0) & (equipment['equipment_id'] % 1 == 0) &
    (equipment['daily_rate'] >= 1) &
    (equipment['stock_quantity'] >= 0) & (equipment['stock_quantity'] % 1 == 0)
]
print(equipment_bfr3[~equipment_bfr3.index.isin(equipment.index)])
print(f"Equipment step 3 removed: {before - len(equipment)}")


before = len(members)
members['member_id'] = pd.to_numeric(members['member_id'], errors='coerce')
members = members.dropna(subset=['member_id'])
members = members[(members['member_id'] > 0) & (members['member_id'] % 1 == 0)]
print(f"Members step 3 removed: {before - len(members)}")


before = len(rentals)
rental_cols = ['rental_id', 'member_id', 'equipment_id', 'quantity', 'rental_days']
for col in rental_cols:
    rentals[col] = pd.to_numeric(rentals[col], errors='coerce')
rentals = rentals.dropna(subset=rental_cols)
for col in rental_cols:
    rentals = rentals[(rentals[col] > 0) & (rentals[col] % 1 == 0)]
rentals['quantity'] = rentals['quantity'].astype(int)
print(f"Rentals step 3 removed: {before - len(rentals)}")


#Step 4 removing invalid dates
# before step 4 & 5
equipment_bfr45 = len(equipment)
members_bfr45 = len(members)
#
before = len(rentals)
rentals_cols = ['rental_date']
rentals['rental_date'] = pd.to_datetime(rentals['rental_date'], format='%Y-%m-%d', errors='coerce')
rentals = rentals.dropna(subset=rentals_cols)
print(f"Rentals step 4 removed: {before - len(rentals)}")

#step 5

before = len(rentals)

Valid_PIDs = (
    rentals['member_id'].isin(members['member_id']) &
    rentals['equipment_id'].isin(equipment['equipment_id'])
)
rentals = rentals[Valid_PIDs]
print(f"Rentals step 5with missing parent records removed: {before - len(rentals)}")
print(f"Equipment step 4 removed: {equipment_bfr45 - len(equipment)} (no date column)")
print(f"Members step 4 removed: {members_bfr45 - len(members)} (no date column)")
print(f"Equipment step 5 removed: {equipment_bfr45 - len(equipment)} (parent table)")
print(f"Members step 5 removed: {members_bfr45 - len(members)} (parent table)")
#Step 6
print(
    "\nFinal row counts:\n"
    f"Equipment: {len(equipment)}\n"
    f"Members: {len(members)}\n"
    f"Rentals: {len(rentals)}"
)

print("\nPrimary key uniqueness:")
for name, df, key in [
    ("Equipment", equipment, "equipment_id"),
    ("Members", members, "member_id"),
    ("Rentals", rentals, "rental_id"),
]:
    print(f"{name} ({key}) unique: {df[key].is_unique}")

print(
    "\nJoin impact: Joins make analysis easier and more reliable, and unique "
    "primary keys help prevent duplicate rows after a join. Step 5 ensured "
    "that every rental has a matching member and equipment record, so joining "
    "the tables will not leave blank names, cities, or rates, and revenue can "
    "be calculated for every retained rental. The trade-off is that removing "
    "rentals means only verified data is reflected, which may understate "
    "reality."
)