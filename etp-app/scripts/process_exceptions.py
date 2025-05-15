import pandas as pd

# Load the CSV file
df = pd.read_csv("exceptions.csv")

# Function to get the ComputerName field with priority and prefix
def get_computer_name(row):
    if pd.notna(row['Computer Name']) and row['Computer Name'].strip():
        return f"CN:{row['Computer Name'].strip().upper()}"
    elif pd.notna(row['Hostname']) and row['Hostname'].strip():
        return f"HN:{row['Hostname'].strip().upper()}"
    elif pd.notna(row['Serial Number']) and row['Serial Number'].strip():
        return f"SN:{row['Serial Number'].strip().upper()}"
    elif pd.notna(row['Barcode']) and row['Barcode'].strip():
        return f"BC:{row['Barcode'].strip().upper()}"
    elif pd.notna(row['Model']) and row['Model'].strip():
        return f"MD:{row['Model'].strip().upper()}"
    elif pd.notna(row['Notes']) and row['Notes'].strip():
        return f"NT:{row['Notes'].strip().upper()}"
    else:
        return "UNKNOWN"

# Function to get the Owner field with fallback logic and prefix
def get_owner(row):
    if pd.notna(row['Owner']) and row['Owner'].strip():
        return f"OWN:{row['Owner'].strip().upper()}"
    elif pd.notna(row['User Name']) and row['User Name'].strip():
        return f"USR:{row['User Name'].strip().upper()}"
    elif pd.notna(row['Lab']) and row['Lab'].strip():
        return f"LAB:{row['Lab'].strip().upper()}"
    elif pd.notna(row['Location']) and row['Location'].strip():
        return f"LOC:{row['Location'].strip().upper()}"
    else:
        return "UNKNOWN"

# Create new DataFrame with cleaned and formatted output
output_df = pd.DataFrame({
    "Lab": df["Lab"].str.upper(),
    "ComputerName": df.apply(get_computer_name, axis=1),
    "Owner": df.apply(get_owner, axis=1)
})

# Save to output CSV file
output_df.to_csv("exceptions_cleaned.csv", index=False)
print("✅ Saved cleaned data to 'exceptions_cleaned.csv'")
