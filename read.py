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

#  remove rows with missing values
before = len(equipment); equipment = equipment.dropna()
print(f"Equipment step 1 removed: {before - len(equipment)}")

before = len(members); members = members.dropna()
print(f"Members step 1 removed: {before - len(members)}")

before = len(rentals); rentals = rentals.dropna()
print(f"Rentals step 1 removed: {before - len(rentals)}")

# remove duplicates
before = len(equipment); equipment = equipment.drop_duplicates()
print(f"Equipment step 2 removed: {before - len(equipment)}")

before = len(members); members = members.drop_duplicates()
print(f"Members step 2 removed: {before - len(members)}")

before = len(rentals); rentals = rentals.drop_duplicates()
print(f"Rentals step 2 removed: {before - len(rentals)}")

# validating numeric values

equipment_before3 = equipment.copy()

before = len(equipment)
for col in ['equipment_id', 'daily_rate', 'stock_quantity']:
    equipment[col] = pd.to_numeric(equipment[col], errors='coerce')
equipment = equipment.dropna(subset=['equipment_id', 'daily_rate', 'stock_quantity'])
equipment = equipment[
    (equipment['equipment_id'] > 0) & (equipment['equipment_id'] % 1 == 0) &
    (equipment['daily_rate'] >= 1) &
    (equipment['stock_quantity'] >= 0) & (equipment['stock_quantity'] % 1 == 0)
]
print(equipment_before3[~equipment_before3.index.isin(equipment.index)])
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