import pandas as pd

# Load the CSV file
df = pd.read_csv("exceptions.csv")

def get_computer_name(row):
    if pd.notna(row.get('Computer Name', '')) and row['Computer Name'].strip():
        return f"CN:{row['Computer Name'].strip().upper()}"
    elif pd.notna(row.get('Hostname', '')) and row['Hostname'].strip():
        return f"HN:{row['Hostname'].strip().upper()}"
    elif pd.notna(row.get('Serial Number', '')) and row['Serial Number'].strip():
        return f"SN:{row['Serial Number'].strip().upper()}"
    elif pd.notna(row.get('Barcode', '')) and row['Barcode'].strip():
        return f"BC:{row['Barcode'].strip().upper()}"
    elif pd.notna(row.get('Model', '')) and row['Model'].strip():
        return f"MD:{row['Model'].strip().upper()}"
    elif pd.notna(row.get('Notes', '')) and row['Notes'].strip():
        return f"NT:{row['Notes'].strip().upper()}"
    else:
        return "UNKNOWN"


def get_owner(row):
    if pd.notna(row.get('Owner', '')) and row['Owner'].strip():
        return row['Owner'].strip()
    elif pd.notna(row.get('User Name', '')) and row['User Name'].strip():
        return row['User Name'].strip()
    elif pd.notna(row.get('Lab', '')) and row['Lab'].strip():
        return row['Lab'].strip()
    elif pd.notna(row.get('Location', '')) and row['Location'].strip():
        return row['Location'].strip()
    else:
        return "UNKNOWN"

def get_serial(row):
    return row.get('Serial Number') or row.get('SerialNumber') or ''

def get_mac(row):
    mac_parts = []
    mac_fields = {
        'Ethernet MAC': 'MAC',
        'MAC Address': 'MAC',
        'Wi-Fi MAC': 'wMAC',
        'Wireless MAC': 'wMAC',
        'Bluetooth MAC': 'bMAC',
        'Unknown MAC': 'uMAC',
        'MAC': 'uMAC'
    }
    for field, label in mac_fields.items():
        value = row.get(field)
        if pd.notna(value) and str(value).strip():
            mac_parts.append(f"{label}:{str(value).strip()}")
    return '; '.join(mac_parts)

def get_justification(row):
    for field in ['Justification', 'Business Justification']:
        value = row.get(field)
        if pd.notna(value) and str(value).strip():
            return str(value).strip()
    return ''

# Build the output DataFrame
output_df = pd.DataFrame({
    'Lab': df['Lab'].fillna('').str.upper(),
    'ComputerName': df.apply(get_computer_name, axis=1),
    'SerialNumber': df.apply(get_serial, axis=1),
    'MAC': df.apply(get_mac, axis=1),
    'Owner': df.apply(get_owner, axis=1),
    'BusinessJustification': df.apply(get_justification, axis=1)
})

# Save to output CSV file
output_df.to_csv("exceptions_cleaned.csv", index=False)
print("✅ Saved cleaned data to 'exceptions_cleaned.csv'")
