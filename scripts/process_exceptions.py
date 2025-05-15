import pandas as pd

# Load the CSV file
df = pd.read_csv("exceptions.csv")

# Helper function to determine ComputerName with fallback
def get_computer_name(row):
    if pd.notna(row['Computer Name']) and row['Computer Name'].strip():
        return f"CN:{row['Computer Name'].strip().upper()}"
    elif pd.notna(row['Hostname']) and row['Hostname'].strip():
        return f"HN:{row['Hostname'].strip().upper()}"
    elif pd.notna(row['Serial Number']) and row['Serial Number'].strip():
        return f"SN:{row['Serial Number'].strip().upper()}"
    elif pd.notna(row['Barcode']) and row['Barcode'].strip():
        return f"BC:{row['Barcode'].strip().upper()}"
    else:
        return "UNKNOWN"

# Helper function to determine Owner with fallback
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

# Build output DataFrame
output_df = pd.DataFrame({
    "Lab": df["Lab"].str.upper(),
    "ComputerName": df.apply(get_computer_name, axis=1),
    "Owner": df.apply(get_owner, axis=1)
})

# Save result
output_df.to_csv("exceptions_cleaned.csv", index=False)
print("Saved to exceptions_cleaned.csv")

