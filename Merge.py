import pandas as pd

# Read in the data
rg_df = pd.read_csv("RezGasStations.csv")
fn_df = pd.read_csv("FirstNationsGasStations.csv")

print("Reformatting phone numbers...")
# Iterate through rg_df and reformat the phone numbers
for i, row in rg_df.iterrows():
    if type(row["Phone"]) == str and len(row["Phone"]) > 10:
        phone = ''.join(row["Phone"].split('-'))
        phone = f"({phone[0:3]}) {phone[3:6]}-{phone[6:]}"
        rg_df.at[i, "Phone"] = phone

# Merge the data
merged_df = pd.concat([fn_df, rg_df], ignore_index=True)

print("Checking for duplicate phone numbers...")
phones = {}
drop_list = []
for i, row in merged_df.iterrows():
    if type(row["Phone"]) == str and row["Phone"] != "-":
        if phones.get(row["Phone"]) is not None:
            first = phones[row["Phone"]]["Name"].lower().split(" ")
            second = row["Name"].lower().split(" ")
            count = 0
            for word in first:
                if word in second:
                    count += 1
            if count > 1:
                print('\033[91m' + f"Found duplicate phone number: {row['Phone']} | {row['Name']} | {phones[row['Phone']]['Name']}")
                #print(f"First instance: {phones[row['Phone']]}")
                #print(f"Second instance: {row}")
                drop_list.append(i)
        else:
            phones[row["Phone"]] = row
print('\033[37m' + f"Merging tables...")
merged_df.drop(merged_df.index[drop_list], inplace=True)

#print(merged_df.head())
print('\033[37m' + f"Found {len(merged_df.index)} unique stations")
print('\033[37m' + f"Exporting to csv...")
merged_df.to_csv("MergedStations.csv", index=False)
print('\033[92m' + f"Successfully export to csv!")